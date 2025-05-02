FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies yang dibutuhkan sistem
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    libsndfile1 \
    ffmpeg \
 && rm -rf /var/lib/apt/lists/*

# Salin file dan install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua kode ke container
COPY . .

# Set env buat SudachiPy
ENV SUDACHIDICT_DIR=/usr/local/lib/python3.10/dist-packages/sudachidict_core

# Port yang dibuka
EXPOSE 8080

# Jalankan FastAPI pakai Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
