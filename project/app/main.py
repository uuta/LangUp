from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
import uuid
import os
from openai import OpenAI
from dotenv import load_dotenv

# OpenAI APIキーを環境変数から取得
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# APIキーが設定されているか確認
if not OPENAI_API_KEY:
    raise RuntimeError(
        "OpenAI API Key is not set. Please set it as an environment variable."
    )

# OpenAIクライアントを初期化
client = OpenAI(api_key=OPENAI_API_KEY)

# FastAPIアプリを初期化
app = FastAPI()


# リクエストスキーマ
class SpeechRequest(BaseModel):
    text: str
    voice: str = "alloy"  # デフォルトの音声タイプ


# 音声生成エンドポイント
@app.post("/generate-speech")
async def generate_speech(request: SpeechRequest):
    try:
        # ユニークなファイル名を生成
        file_id = uuid.uuid4()
        speech_file_path = Path(__file__).parent / f"{file_id}.mp3"

        # OpenAI TTS APIを呼び出して音声生成
        response = client.audio.speech.create(
            model="tts-1", voice=request.voice, input=request.text
        )

        # 音声ファイルを保存
        response.stream_to_file(speech_file_path)

        return {"file_path": str(speech_file_path)}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating speech: {str(e)}"
        )
