import os

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from models.speech_request import SpeechRequest
from services.s3 import upload_to_s3
from services.tts import generate_tts_audio

router = APIRouter()


@router.post("/generate-speech/")
async def generate_speech(request: SpeechRequest):
    try:
        # TTS音声生成
        local_audio_path = await generate_tts_audio(request.text)

        # S3にアップロード
        s3_url = await upload_to_s3(local_audio_path, "speech/")

        # ローカルファイルを削除
        os.remove(local_audio_path)

        return {"file_url": s3_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/privacy-policy", response_class=HTMLResponse)
async def privacy_policy():
    try:
        with open("static/privacy_policy.html", "r", encoding="utf-8") as file:
            content = file.read()
        return HTMLResponse(content=content)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Privacy Policy not found")
