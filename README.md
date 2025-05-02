📘 TransAPI - API Terjemahan Indonesia ⇄ Jepang

API ini menyediakan fitur lengkap untuk menerjemahkan teks antara Bahasa Indonesia dan Bahasa Jepang dengan tambahan fitur NLP seperti:

* Translasi dua arah (Indonesia ⇄ Jepang)
* Konversi romaji → kana otomatis
* Format keigo (-masu form)
* Breakdown token (Kanji, Furigana, Romaji)
* Text-to-Speech (TTS)
* Speech-to-Text (STT) untuk audio Jepang

---

## 🚀 Cara Menjalankan

1. Pastikan Python 3.10+ sudah terinstal
2. Install dependensi:

   ```bash
   pip install -r requirements.txt
   ```
3. Jalankan server:

   ```bash
   uvicorn main:app --reload
   ```

---

## 🔗 Endpoint

### \[GET] `/`

Cek status API

```json
{ "message": "TransAPI is alive! 🔥" }
```

### \[POST] `/translate_and_analyze`

Terjemahkan teks dan tampilkan hasil analisis linguistik.

**Body:**

```json
{
  "text": "saya ingin pergi ke pantai",
  "src": "id",
  "dest": "ja"
}
```

**Respons:**

```json
{
  "translated_text": "海に行きます",
  "japanese_text": "海に行きます",
  "romaji": "umi ni ikimasu",
  "breakdown": [
    { "surface": "海", "furigana": "うみ", "romaji": "umi" },
    { "surface": "に", "furigana": "に", "romaji": "ni" },
    { "surface": "行きます", "furigana": "いきます", "romaji": "ikimasu" }
  ]
}
```

### \[POST] `/speak`

Text-to-speech (TTS) untuk Bahasa Indonesia atau Jepang.

**Body:**

```json
{
  "text": "おはようございます",
  "src": "ja",
  "dest": "ja"
}
```

**Response:**
File .mp3 audio

### \[POST] `/speech_to_text`

Speech-to-text untuk audio Jepang (.wav)

**Form:** multipart/form-data

**Respons:**

```json
{ "recognized_text": "おはようございます" }
```

---

## 🇯🇵 日本語バージョン

このAPIは、インドネシア語と日本語の間で双方向翻訳を提供し、さらに以下の機能も備えています：

* 敬語（丁寧形）への変換
* ローマ字から仮名への自動変換
* トークンの分解（表層形、ふりがな、ローマ字）
* 音声合成（TTS）
* 音声認識（STT）

### 実行方法

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

### エンドポイント

#### \[GET] `/`

APIの起動確認

```json
{ "message": "TransAPI is alive! 🔥" }
```

#### \[POST] `/translate_and_analyze`

翻訳と形態素解析を行います。

#### \[POST] `/speak`

テキスト音声変換（日本語/インドネシア語）

#### \[POST] `/speech_to_text`

音声→テキスト変換（日本語音声対応）

---

## 🎯 Cocok untuk / 適用対象

* Aplikasi edukasi bahasa Jepang
* Translator berbasis NLP
* Asisten suara AI (TTS/STT)

---

## 🔗 API Online

✅ URL: [https://nindogoterbakar.onrender.com](https://nindogoterbakar.onrender.com)  
🧪 Swagger Docs: [https://nindogoterbakar.onrender.com/docs](https://nindogoterbakar.onrender.com/docs)


Selamat belajar & ngoding! ご利用ありがとうございます 🙇‍♀️
