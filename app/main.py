import sys
from pathlib import Path

import streamlit as st


# --------------------------------
# PATH CONFIGURATION
# --------------------------------

FILE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = FILE_DIR.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(FILE_DIR) not in sys.path:
    sys.path.insert(0, str(FILE_DIR))


# IMPORTS

from ai.shopping_agent import ShoppingAgent
from app.voice.speech_to_text import VoiceRecognizer
from app.voice.text_to_speech import speak, stop_speaking



# PAGE SETTINGS

st.set_page_config(
    page_title="PINKS AI",
    layout="centered"
)



# --------------------------------
# DEFAULT CHAT
# --------------------------------

DEFAULT_MESSAGES = [
    {
        "role": "assistant",
        "content":
        "Hi, my name is PINKS. I can help you find products, compare options, and place orders."
    }
]



# --------------------------------
# AI AGENT
# --------------------------------

@st.cache_resource
def get_agent():

    return ShoppingAgent()



# --------------------------------
# VOICE
# --------------------------------

@st.cache_resource
def get_voice():

    return VoiceRecognizer()



# --------------------------------
# MEMORY
# --------------------------------

def initialize():

    if "messages" not in st.session_state:

        st.session_state.messages = DEFAULT_MESSAGES.copy()


    if "voice_enabled" not in st.session_state:

        st.session_state.voice_enabled = True



def add_message(role, content):

    st.session_state.messages.append(
        {
            "role": role,
            "content": content
        }
    )



# --------------------------------
# PROCESS MESSAGE
# --------------------------------

def ask_pinks(
        message,
        model,
        temperature,
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

        with st.spinner(
            "PINKS is thinking..."
        ):

            try:

                response = get_agent().reply(

                    customer_message=message,

                    image_bytes=image_bytes,

                    image_mime_type=image_type,

                    model=model,

                    temperature=temperature
                )


            except Exception as e:

                response = f"Error: {e}"



        st.write(response)



    add_message(
        "assistant",
        response
    )



    # Voice output

    if st.session_state.voice_enabled:

        try:

            speak(response)

        except Exception as e:

            st.warning(
                f"Voice error: {e}"
            )



# --------------------------------
# LISTEN
# --------------------------------

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



# --------------------------------
# START APP
# --------------------------------

initialize()


st.title(
    "🛒 PINKS AI"
)

st.caption(
    "Your AI shopping assistant. Talk, type, or upload product images."
)



# --------------------------------
# SIDEBAR
# --------------------------------

with st.sidebar:

    st.header(
        "Settings"
    )


    st.session_state.voice_enabled = st.toggle(
        "Enable voice replies",
        value=st.session_state.voice_enabled
    )


    model = st.selectbox(

        "Choose AI Model",

        [
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "llama-3.2-11b-vision-preview",
            "gemma2-9b-it",
            "mixtral-8x7b-32768"
        ]
    )


    temperature = st.slider(

        "Temperature",

        min_value=0.0,

        max_value=1.0,

        value=0.7,

        step=0.1
    )


    if st.button(
        "Clear Chat",
        use_container_width=True
    ):

        stop_speaking()

        get_agent().reset_history()

        st.session_state.messages = (
            DEFAULT_MESSAGES.copy()
        )

        st.rerun()



# --------------------------------
# CHAT HISTORY
# --------------------------------

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.write(
            message["content"]
        )



# --------------------------------
# IMAGE UPLOAD
# --------------------------------

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



# --------------------------------
# VOICE BUTTON
# --------------------------------

if st.button(
    "🎤 Talk to PINKS",
    use_container_width=True
):

    user_voice = listen()


    if user_voice:

        ask_pinks(

            user_voice,

            model,

            temperature,

            image_bytes,

            image_type,

            image_name
        )



# --------------------------------
# TEXT CHAT
# --------------------------------

text = st.chat_input(
    "Ask PINKS about products..."
)


if text:

    ask_pinks(

        text,

        model,

        temperature,

        image_bytes,

        image_type,

        image_name
    )