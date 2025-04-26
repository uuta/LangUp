import os

import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

from models.speech_request import LANGUAGE_METADATA, LanguageCode

# 環境変数の読み込み
load_dotenv()


async def generate_tts_audio(text: str, lang_code: LanguageCode) -> str:
    """
    Microsoft Azure Speech SDKを使用して音声ファイルを生成し、ローカルに保存する関数。

    Args:
        text (str): 音声生成の元になるテキスト
        lang_code (LanguageCode): 音声生成に使用する言語コード

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
        # voice name
        speech_config.speech_synthesis_voice_name = LANGUAGE_METADATA[lang_code][
            "voice_name"
        ]
        # Enhance the quality of the audio
        speech_config.set_speech_synthesis_output_format(
            speechsdk.SpeechSynthesisOutputFormat.Audio24Khz160KBitRateMonoMp3
        )

        # tmp file
        import hashlib

        # テキストをハッシュ化してファイル名を生成（SHA-256を使用）
        text_hash = hashlib.sha256(text.encode()).hexdigest()
        file_name = f"{text_hash}.mp3"
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
