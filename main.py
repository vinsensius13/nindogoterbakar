import os
import uuid
import jaconv
import tempfile
import speech_recognition as sr
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from googletrans import Translator
from sudachipy import dictionary, tokenizer
from gtts import gTTS

# ✅ Optional: buat Linux/Cloud Run
os.environ["SUDACHIDICT_DIR"] = "/usr/local/lib/python3.10/dist-packages/sudachidict_core"

app = FastAPI()
translator = Translator()
tokenizer_obj = dictionary.Dictionary().create()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "TransAPI is alive! 🔥"}

# 🧠 Model request
class TranslateRequest(BaseModel):
    text: str
    src: str = "id"
    dest: str = "ja"

# ✨ Convert hasil Japanese ke keigo (-masu form) dengan Sudachi
def force_teinei_form(japanese_text: str) -> str:
    tokens = tokenizer_obj.tokenize(japanese_text, tokenizer.Tokenizer.SplitMode.C)
    converted = []
    for token in tokens:
        surface = token.surface()
        pos = token.part_of_speech()
        if pos[0] == "動詞":  # Verb
            if surface.endswith("る"):
                surface = surface[:-1] + "ます"
            elif surface in ["する", "くる"]:
                surface = {"する": "します", "くる": "きます"}[surface]
        converted.append(surface)
    return "".join(converted)

# 🔧 Force string
def convert_to_string(text) -> str:
    return str(text) if not isinstance(text, str) else text

# 🧠 Cek numerik (buat filtering furigana/romaji)
def is_number(text):
    try:
        float(text.replace(",", "").replace("．", ".").replace("・", "."))  # handle 15.00 dan simbol aneh
        return True
    except ValueError:
        return False

@app.post("/translate_and_analyze")
async def translate_and_analyze(request: TranslateRequest):
    text = convert_to_string(request.text)
    src = request.src.lower()
    dest = request.dest.lower()

    if src == "ja":
        is_romaji = all(ord(c) < 128 and (c.isalnum() or c.isspace()) for c in text)
        if is_romaji:
            kana_text = jaconv.alphabet2kana(text)
        else:
            kana_text = text

        japanese_text = kana_text
        translated = translator.translate(japanese_text, src="ja", dest="id")
        final_translation = translated.text
    else:
        translated = translator.translate(text, src=src, dest="ja")
        japanese_text = translated.text
        japanese_text = force_teinei_form(japanese_text)

        if dest == "ja":
            final_translation = japanese_text
        else:
            result_back = translator.translate(japanese_text, src="ja", dest=dest)
            final_translation = result_back.text

    romaji_list = []
    breakdown = []

    for token in tokenizer_obj.tokenize(japanese_text, tokenizer.Tokenizer.SplitMode.C):
        surface = token.surface()
        if is_number(surface):
            breakdown.append({
                "surface": surface,
                "furigana": "",
                "romaji": ""
            })
            romaji_list.append(surface)
        else:
            reading = token.reading_form()
            hira = jaconv.kata2hira(reading)
            romaji = jaconv.kana2alphabet(hira)
            breakdown.append({
                "surface": surface,
                "furigana": hira,
                "romaji": romaji
            })
            romaji_list.append(romaji)

    romaji_output = " ".join(romaji_list)

    return JSONResponse(
        content={
            "translated_text": final_translation,
            "japanese_text": japanese_text,
            "romaji": romaji_output,
            "breakdown": breakdown
        },
        media_type="application/json; charset=utf-8"
    )

# 🔊 TTS
@app.post("/speak")
async def speak_text(request: TranslateRequest):
    text = convert_to_string(request.text)
    filename = f"{uuid.uuid4()}.mp3"
    tts = gTTS(text=text, lang=request.dest)
    tts.save(filename)
    return FileResponse(filename, media_type="audio/mpeg", filename="speak.mp3")

# 🗣️ STT (Speech to Text)
@app.post("/speech_to_text")
async def speech_to_text(audio: UploadFile = File(...)):
    recognizer = sr.Recognizer()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(await audio.read())
        tmp_path = tmp.name

    with sr.AudioFile(tmp_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language="ja-JP")
        except sr.UnknownValueError:
            text = "Tidak bisa dikenali."
        except sr.RequestError as e:
            text = f"Error dari API Google: {e}"

    os.remove(tmp_path)
    return {"recognized_text": text}
