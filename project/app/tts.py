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

    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

    payload = {"text": text, "voice": "en-US-Wavenet-D"}  # 適宜選択

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

    return f"http://localhost:10000/static/{file_name}"
