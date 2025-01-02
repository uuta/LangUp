from dotenv import load_dotenv
from openai import OpenAI

client = OpenAI()

# 環境変数の読み込み
load_dotenv()


async def generate_tts_audio(text: str) -> str:
    """
    OpenAI TTS APIを使用して音声ファイルを生成し、ローカルに保存する関数。
    See: https://platform.openai.com/docs/api-reference/audio/createSpeech#audio-createspeech-voice

    Args:
        text (str): 音声生成の元になるテキスト

    Returns:
        str: 保存された音声ファイルのローカルパス
    """
    try:
        # OpenAI TTS APIへのリクエスト
        response = client.audio.speech.create(
            model="tts-1", input=text, voice="onyx", speed=1.25
        )

        # ユニークなファイル名を生成
        file_name = f"{text}.mp3"
        file_path = f"/tmp/{file_name}"  # 一時ファイルディレクトリに保存

        response.stream_to_file(file_path)

        return file_path

    except Exception as e:
        raise Exception(f"Error generating TTS audio: {e}")
