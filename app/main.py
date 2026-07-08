import importlib.util
import sys
import time
from pathlib import Path

import streamlit as st

# Ensure the project root is on sys.path so imports like `voice.*` and `ai.*` resolve.
FILE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = FILE_DIR.parent

for p in (PROJECT_ROOT, FILE_DIR):
    sp = str(p)
    if sp not in sys.path:
        sys.path.insert(0, sp)

from voice.speech_to_text import VoiceRecognizer
from voice.text_to_speech import speak, stop_speaking

AGENT_FILE = PROJECT_ROOT / "ai" / "shopping_agent.py"


DEFAULT_MESSAGES = [
            {
                "role": "assistant",
                "content": "Hi, my name is PINKS. I can help you find products, compare options, and place orders.",
            }
]


st.set_page_config(
    page_title="PINKS",
    layout="centered",
)


def get_agent():
    module_name = f"shopping_agent_live_{time.time_ns()}"
    spec = importlib.util.spec_from_file_location(module_name, AGENT_FILE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    ShoppingAgent = module.ShoppingAgent

    return ShoppingAgent()


@st.cache_resource
def get_voice_recognizer():
    return VoiceRecognizer()


def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = DEFAULT_MESSAGES.copy()

    if "voice_enabled" not in st.session_state:
        st.session_state.voice_enabled = True


def add_message(role, content):
    st.session_state.messages.append(
        {
            "role": role,
            "content": content,
        }
    )


def ask_assistant(customer_message, image_bytes=None, image_mime_type=None, image_name=None):
    cleaned_message = customer_message.strip()

    if not cleaned_message:
        st.warning("I did not catch a message. Try typing, listening, or uploading an image again.")
        return

    if cleaned_message.lower() in {"exit", "quit", "stop"}:
        add_message("user", cleaned_message)
        add_message("assistant", "Session ended. Refresh the page when you want to start again.")
        return

    display_message = cleaned_message

    if image_name:
        display_message = f"{cleaned_message}\n\nUploaded image: {image_name}"

    add_message("user", display_message)

    with st.chat_message("user"):
        st.write(cleaned_message)
        if image_bytes:
            st.image(image_bytes, caption=image_name)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                answer = get_agent().reply(
                    cleaned_message,
                    image_bytes=image_bytes,
                    image_mime_type=image_mime_type,
                )
            except Exception as exc:
                st.error(f"Assistant error: {exc}")
                return

        st.write(answer)

    add_message("assistant", answer)

    if st.session_state.voice_enabled:
        try:
            speak(answer)
        except Exception as exc:
            st.warning(f"Could not play audio response: {exc}")


def listen_for_message():
    with st.spinner("Listening..."):
        try:
            return get_voice_recognizer().listen()
        except Exception as exc:
            st.error(f"Microphone error: {exc}")
            return None


initialize_session_state()

st.title("PINKS")
st.caption("Talk, type, or upload a product image to shop, compare, and get recommendations.")

with st.sidebar:
    st.header("Controls")
    st.session_state.voice_enabled = st.toggle(
        "Speak assistant replies",
        value=st.session_state.voice_enabled,
    )

    if st.button("Clear conversation", use_container_width=True):
        stop_speaking()
        st.cache_resource.clear()
        st.session_state.messages = DEFAULT_MESSAGES.copy()
        st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

voice_col, status_col = st.columns([1, 2])

with voice_col:
    listen_clicked = st.button("Listen once", use_container_width=True)

with status_col:
    st.write("Use the button for microphone input, or type below.")

uploaded_image = st.file_uploader(
    "Upload a product image",
    type=["png", "jpg", "jpeg", "webp"],
)

if uploaded_image:
    image_bytes = uploaded_image.getvalue()
    st.image(image_bytes, caption=uploaded_image.name, use_container_width=True)

    image_prompt = st.text_input(
        "Ask about this image",
        value="What product is this, and how does it compare to products in your catalog?",
    )

    if st.button("Analyze image", use_container_width=True):
        ask_assistant(
            image_prompt,
            image_bytes=image_bytes,
            image_mime_type=uploaded_image.type,
            image_name=uploaded_image.name,
        )

if listen_clicked:
    spoken_message = listen_for_message()

    if spoken_message:
        ask_assistant(spoken_message)
    else:
        st.warning("No speech was recognized. Please try again.")

typed_message = st.chat_input("Ask for a product, comparison, or order help")

if typed_message:
    ask_assistant(typed_message)
