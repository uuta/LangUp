from enum import Enum
from typing import TypedDict

from pydantic import BaseModel, Field


class LanguageCode(str, Enum):
    """Supported language codes in BCP-47 format."""

    ENGLISH = "en-US"
    RUSSIAN = "ru-RU"
    CHINESE = "zh-CN"
    THAI = "th-TH"
    # Add more languages as needed
    # FRENCH = "fr-FR"
    # GERMAN = "de-DE"


class LanguageMetadata(TypedDict):
    """Type definition for language metadata."""

    name: str  # Human-readable language name
    voice_name: str  # TTS voice identifier


# Language metadata including voice names and other properties
LANGUAGE_METADATA: dict[LanguageCode, LanguageMetadata] = {
    LanguageCode.ENGLISH: {
        "name": "English (US)",
        "voice_name": "en-US-DavisNeural",
    },
    LanguageCode.RUSSIAN: {
        "name": "Russian",
        "voice_name": "ru-RU-DmitryNeural",
    },
    LanguageCode.CHINESE: {
        "name": "Chinese (Traditional)",
        "voice_name": "zh-HK-WanLungNeural",
    },
    LanguageCode.THAI: {
        "name": "Thai",
        "voice_name": "th-TH-NiwatNeural",
    },
}


class SpeechRequest(BaseModel):
    text: str
    lang_code: LanguageCode = Field(
        description="Language code in BCP-47 format (e.g., 'en-US', 'ja-JP')"
    )

    @property
    def voice_name(self) -> str:
        """Get the voice name for the selected language."""
        return LANGUAGE_METADATA[self.lang_code]["voice_name"]

    @property
    def language_name(self) -> str:
        """Get the human-readable language name."""
        return LANGUAGE_METADATA[self.lang_code]["name"]
