import os
import tempfile
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
VOICE_ID = os.getenv("ELEVEN_VOICE_ID")

_current_audio = None


def speak(text: str):

    global _current_audio

    # Try ElevenLabs if configured
    if ELEVEN_API_KEY and VOICE_ID:
        try:
            from elevenlabs.client import ElevenLabs
            from elevenlabs import play

            client = ElevenLabs(api_key=ELEVEN_API_KEY)
            audio = client.text_to_speech.convert(
                voice_id=VOICE_ID,
                model_id="eleven_multilingual_v2",
                text=text
            )
            _current_audio = audio
            play(audio)
            return
        except Exception as e:
            print(f"ElevenLabs TTS failed: {e}. Falling back to gTTS...")

    # Fallback to gTTS & pygame
    try:
        from gtts import gTTS
        import pygame

        tts = gTTS(text=text, lang="en")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            temp_filename = fp.name
            tts.save(temp_filename)

        if not pygame.mixer.get_init():
            pygame.mixer.init()
        pygame.mixer.music.load(temp_filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.music.unload()
        try:
            os.remove(temp_filename)
        except Exception:
            pass
    except Exception as e:
        print(f"TTS output error: {e}")


def stop_speaking():

    global _current_audio
    _current_audio = None

    try:
        import pygame
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
    except Exception:
        pass