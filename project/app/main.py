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
