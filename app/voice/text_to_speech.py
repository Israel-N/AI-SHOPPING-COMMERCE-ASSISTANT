import tempfile
from pathlib import Path
from gtts import gTTS
import pygame

pygame.mixer.init()

is_speaking = False


def stop_speaking():
    global is_speaking

    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()

    is_speaking = False


def speak(text):
    global is_speaking

    stop_speaking()

    tts = gTTS(text=text, lang="en")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp:
        temp_path = Path(temp.name)

    tts.save(temp_path)

    pygame.mixer.music.load(temp_path)

    is_speaking = True

    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():

        if not is_speaking:
            break

        pygame.time.wait(50)

    is_speaking = False