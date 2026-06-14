import os
import tempfile
from pathlib import Path
from gtts import gTTS
import pygame


def stop_speaking():
    try:
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
    except pygame.error:
        pass


def speak(text):

    tts = gTTS(
        text=text,
        lang="en"
    )

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp:
        temp_path = Path(temp.name)

    tts.save(str(temp_path))

    pygame.mixer.init()

    pygame.mixer.music.load(
        str(temp_path)
    )

    pygame.mixer.music.play()
