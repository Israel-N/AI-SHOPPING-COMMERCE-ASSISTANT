import sys
from pathlib import Path

# Ensure the project root is on sys.path so imports like `voice.*` and `ai.*` resolve
FILE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = FILE_DIR.parent
# Ensure both the project root and the app directory are on sys.path so
# imports like `voice.*` and `ai.*` resolve whether packages live in the
# project root or inside the app/ directory.
for p in (PROJECT_ROOT, FILE_DIR):
    sp = str(p)
    if sp not in sys.path:
        sys.path.insert(0, sp)

from voice.speech_to_text import VoiceRecognizer
from voice.text_to_speech import speak
from ai.shopping_agent import ShoppingAgent

voice = VoiceRecognizer()

agent = ShoppingAgent()

print("Voice Shopping Assistant Started")

while True:

    customer_message = voice.listen()

    if not customer_message:
        continue

    if customer_message.lower() == "exit":
        break

    answer = agent.reply(
        customer_message
    )

    print(
        f"Assistant: {answer}"
    )

    speak(answer)