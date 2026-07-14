import importlib.util
import sys
import time
from pathlib import Path

import streamlit as st


# -----------------------------
# PATH CONFIGURATION
# -----------------------------

FILE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = FILE_DIR.parent

for path in [PROJECT_ROOT, FILE_DIR]:
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))


# -----------------------------
# IMPORTS
# -----------------------------

from voice.speech_to_text import VoiceRecognizer
from voice.text_to_speech import speak, stop_speaking


AGENT_FILE = PROJECT_ROOT / "ai" / "shopping_agent.py"



# -----------------------------
# PAGE SETTINGS
# -----------------------------

st.set_page_config(
    page_title="PINKS",
    layout="centered"
)



# -----------------------------
# DEFAULT CHAT
# -----------------------------

DEFAULT_MESSAGES = [
    {
        "role": "assistant",
        "content":
        "Hi, my name is PINKS. I can help you find products, compare options, and place orders."
    }
]



# -----------------------------
# LOAD AI AGENT
# -----------------------------

def get_agent():

    module_name = f"shopping_agent_{time.time_ns()}"

    spec = importlib.util.spec_from_file_location(
        module_name,
        AGENT_FILE
    )

    module = importlib.util.module_from_spec(spec)

    spec.loader.exec_module(module)

    return module.ShoppingAgent()



# -----------------------------
# VOICE INSTANCE
# -----------------------------

@st.cache_resource
def get_voice():

    return VoiceRecognizer()



# -----------------------------
# SESSION MEMORY
# -----------------------------

def initialize():

    if "messages" not in st.session_state:
        st.session_state.messages = DEFAULT_MESSAGES.copy()


    if "voice_enabled" not in st.session_state:
        st.session_state.voice_enabled = True



def add_message(role, text):

    st.session_state.messages.append(
        {
            "role": role,
            "content": text
        }
    )



# -----------------------------
# PROCESS USER MESSAGE
# -----------------------------

def ask_pinks(
        message,
        image_bytes=None,
        image_type=None,
        image_name=None
):

    if not message.strip():

        st.warning(
            "Please enter a message."
        )

        return



    add_message(
        "user",
        message
    )


    with st.chat_message("user"):

        st.write(message)

        if image_bytes:

            st.image(
                image_bytes,
                caption=image_name
            )



    with st.chat_message("assistant"):

        with st.spinner("PINKS is thinking..."):

            try:

                response = get_agent().reply(
                    message,
                    image_bytes=image_bytes,
                    image_mime_type=image_type
                )


            except Exception as e:

                response = f"Error: {e}"



        st.write(response)



    add_message(
        "assistant",
        response
    )



    # Voice reply

    if st.session_state.voice_enabled:

        try:

            speak(response)

        except Exception as e:

            st.warning(
                f"Voice error: {e}"
            )



# -----------------------------
# VOICE INPUT
# -----------------------------

def listen():

    try:

        with st.spinner(
            "Listening..."
        ):

            return get_voice().listen()


    except Exception as e:

        st.error(
            f"Microphone error: {e}"
        )

        return None



# -----------------------------
# START APP
# -----------------------------

initialize()



st.title("🛒 PINKS AI")

st.caption(
    "Your AI shopping assistant. Talk, type, or upload product images."
)



# -----------------------------
# SIDEBAR
# -----------------------------

with st.sidebar:

    st.header(
        "Settings"
    )


    st.session_state.voice_enabled = st.toggle(
        "Enable voice replies",
        value=st.session_state.voice_enabled
    )


    if st.button(
        "Clear chat",
        use_container_width=True
    ):

        stop_speaking()

        st.session_state.messages = (
            DEFAULT_MESSAGES.copy()
        )

        st.rerun()



# -----------------------------
# SHOW CHAT HISTORY
# -----------------------------

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.write(
            message["content"]
        )



# -----------------------------
# IMAGE UPLOAD
# -----------------------------

uploaded_image = st.file_uploader(
    "Upload product image",
    type=[
        "png",
        "jpg",
        "jpeg",
        "webp"
    ]
)


image_bytes = None
image_type = None
image_name = None


if uploaded_image:

    image_bytes = uploaded_image.getvalue()

    image_type = uploaded_image.type

    image_name = uploaded_image.name


    st.image(
        image_bytes,
        caption=image_name
    )



# -----------------------------
# VOICE BUTTON
# -----------------------------

if st.button(
    "🎤 Talk to PINKS",
    use_container_width=True
):

    user_voice = listen()


    if user_voice:

        ask_pinks(
            user_voice,
            image_bytes,
            image_type,
            image_name
        )


    else:

        st.warning(
            "I could not understand you."
        )



# -----------------------------
# TEXT INPUT
# -----------------------------

text = st.chat_input(
    "Ask PINKS about products..."
)


if text:

    ask_pinks(
        text,
        image_bytes,
        image_type,
        image_name
    )