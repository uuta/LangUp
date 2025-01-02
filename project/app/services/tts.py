import os

import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()


async def generate_tts_audio(text: str) -> str:
    """
    Microsoft Azure Speech SDKを使用して音声ファイルを生成し、ローカルに保存する関数。

    Args:
        text (str): 音声生成の元になるテキスト

    Returns:
        str: 保存された音声ファイルのローカルパス
    """
    try:
        # Azure Speech Key & Region
        speech_key = os.getenv("AZURE_SPEECH_KEY")
        service_region = os.getenv("AZURE_REGION")

        # Azure Speech Config
        speech_config = speechsdk.SpeechConfig(
            subscription=speech_key, region=service_region
        )
        speech_config.speech_synthesis_voice_name = "en-US-DavisNeural"  # voice name

        # tmp file
        normalized_text = text.replace(" ", "_")
        file_name = f"{normalized_text}.mp3"
        file_path = f"/tmp/{file_name}"

        # Generate audio
        audio_config = speechsdk.audio.AudioOutputConfig(filename=file_path)
        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config, audio_config=audio_config
        )

        # Execute TTS
        result = synthesizer.speak_text_async(text).get()

        if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
            raise Exception(f"Speech synthesis failed: {result.reason}")

        return file_path

    except Exception as e:
        raise Exception(f"Error generating TTS audio: {e}")
