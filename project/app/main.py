import boto3
from botocore.exceptions import NoCredentialsError
from fastapi import FastAPI, HTTPException, UploadFile
from pydantic import BaseModel
from pathlib import Path
import uuid
import os
from dotenv import load_dotenv

# 環境変数からAWSの設定を読み込み
load_dotenv()
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
S3_BUCKET = os.getenv("S3_BUCKET_NAME")
S3_REGION = os.getenv("AWS_REGION", "us-east-1")  # デフォルトリージョン

# S3クライアントを作成
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=S3_REGION,
)

app = FastAPI()


class SpeechRequest(BaseModel):
    text: str
    voice: str = "alloy"  # デフォルトの音声タイプ


async def upload_to_s3(file_path: str, bucket: str, object_name: str) -> str:
    """
    ファイルをS3にアップロードしてURLを返す
    """
    try:
        s3_client.upload_file(file_path, bucket, object_name)
        file_url = f"https://{bucket}.s3.{S3_REGION}.amazonaws.com/{object_name}"
        return file_url
    except FileNotFoundError:
        raise HTTPException(status_code=400, detail="File not found for upload")
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="AWS credentials not available")


@app.post("/generate-speech/")
async def generate_speech(request: SpeechRequest):
    try:
        # 音声ファイルを生成（ここでは仮のローカルファイルパス）
        file_id = str(uuid.uuid4())
        local_file_path = f"{file_id}.mp3"
        object_name = f"speech/{file_id}.mp3"

        # 実際のTTSロジックを挿入 (例: TTSサービスで音声生成)
        # ここではダミーデータでファイル作成
        with open(local_file_path, "wb") as f:
            f.write(b"This is a dummy TTS file.")

        # S3にアップロード
        file_url = await upload_to_s3(local_file_path, S3_BUCKET, object_name)

        # ローカルファイルを削除
        os.remove(local_file_path)

        return {"file_url": file_url}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating speech: {str(e)}"
        )
