#!/bin/bash

# Create project directories and files
mkdir -p project/app
cd project

# Create main.py
cat > app/main.py <<EOL
from fastapi import FastAPI, HTTPException
from app.tts import get_tts

app = FastAPI()

@app.post("/tts")
async def generate_tts(text: str):
    """
    Accepts text input and returns the TTS audio file URL.
    """
    try:
        audio_url = await get_tts(text)
        return {"audio_url": audio_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
EOL

# Create tts.py
cat > app/tts.py <<EOL
import aiohttp
import uuid
import os

TTS_API_URL = "https://api.openai.com/v1/tts"  # 適切なTTSエンドポイントを使用

API_KEY = os.getenv("OPENAI_API_KEY")

async def get_tts(text: str) -> str:
    """
    Sends a request to the TTS service and returns the audio URL.
    """
    if not API_KEY:
        raise ValueError("API key for TTS is not set.")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "text": text,
        "voice": "en-US-Wavenet-D"  # 適宜選択
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(TTS_API_URL, headers=headers, json=payload) as response:
            if response.status != 200:
                raise Exception(f"TTS API failed with status {response.status}")
            data = await response.json()

    # Save audio file locally or return URL
    file_name = f"{uuid.uuid4()}.mp3"
    file_path = f"static/{file_name}"

    with open(file_path, "wb") as f:
        f.write(data["audio_content"].encode("latin1"))  # 適宜エンコード調整

    return f"http://localhost:8000/static/{file_name}"
EOL

# Create requirements.txt
cat > app/requirements.txt <<EOL
fastapi
aiohttp
uvicorn
EOL

# Create Dockerfile
cat > Dockerfile <<EOL
# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the application files into the container
COPY ./app /usr/src/app

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8400
EXPOSE 8400

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8400", "--reload"]
EOL

# Create docker-compose.yml
cat > docker-compose.yml <<EOL
version: "3.9"
services:
  app:
    build: .
    ports:
      - "8400:8400"
    volumes:
      - ./app:/usr/src/app
    environment:
      - OPENAI_API_KEY=your_openai_api_key
EOL

echo "Setup complete. Run 'docker-compose up --build' to start the service."

