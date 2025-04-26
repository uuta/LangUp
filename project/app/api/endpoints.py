import os

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from models.speech_request import SpeechRequest
from services.s3 import upload_to_s3
from services.tts import generate_tts_audio
from models.speech_request import LanguageCode
from pydantic import BaseModel, Field

router = APIRouter()


class SpeechResponse(BaseModel):
    file_url: str = Field(
        description="URL of the generated speech audio file",
        examples=["https://langup-bucket.s3.amazonaws.com/speech/abcdef1234567890.mp3"],
    )


@router.post("/generate-speech/", response_model=SpeechResponse)
async def generate_speech(request: SpeechRequest) -> SpeechResponse:
    try:
        # TTS音声生成
        local_audio_path = await generate_tts_audio(
            request.text, LanguageCode(request.lang_code)
        )

        # S3にアップロード
        s3_url = await upload_to_s3(local_audio_path, "speech/")

        # ローカルファイルを削除
        os.remove(local_audio_path)

        return SpeechResponse(file_url=s3_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/privacy-policy", response_class=HTMLResponse)
async def privacy_policy() -> HTMLResponse:
    try:
        with open("static/privacy_policy.html", encoding="utf-8") as file:
            content = file.read()
        return HTMLResponse(content=content)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Privacy Policy not found")
