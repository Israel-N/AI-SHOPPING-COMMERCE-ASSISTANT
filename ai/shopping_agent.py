import os
import base64
from pathlib import Path

from groq import Groq

from inventory.products import products

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None



class ShoppingAgent:


    def __init__(self):

        # LOAD ENVIRONMENT VARIABLES

        project_root = Path(__file__).resolve().parents[1]

        env_files = [
            project_root / ".env",
            project_root / "example.env"
        ]


        if load_dotenv:

            for env_file in env_files:

                if env_file.exists():

                    load_dotenv(env_file)
                    break



        api_key = os.getenv(
            "GROQ_API_KEY"
        )


        if not api_key:

            raise RuntimeError(
                "GROQ_API_KEY is missing. Add it to your .env file."
            )



        # GROQ CLIENT

        self.client = Groq(
            api_key=api_key
        )


        self.text_model = os.getenv(
            "GROQ_TEXT_MODEL",
            "llama-3.3-70b-versatile"
        )


        self.vision_model = os.getenv(
            "GROQ_VISION_MODEL",
            "llama-3.2-11b-vision-preview"
        )



        # MEMORY

        self.history = [

            {
                "role": "system",
                "content": self.system_prompt()
            }

        ]



    # PRODUCT CATALOG

    def catalog_summary(self):

        catalog = []


        for name, info in products.items():

            catalog.append(
                f"""
                Product: {name}
                Price: ${info.get('price')}
                Stock: {info.get('stock')}
                """
            )


        return "\n".join(catalog)



    # SYSTEM PROMPT

    def system_prompt(self):

        return f"""

You are PINKS, an intelligent AI shopping assistant.

Your name is PINKS.

If someone asks about your name explain:

"My name PINKS was created from my boss EAZI and his girlfriend's names:
Paula, Israel, Nsobila, Kwaku and Serwaa."

Your responsibilities:

- Help customers find products.
- Recommend products.
- Compare products.
- Explain product differences.
- Help customers make buying decisions.
- Assist with orders.

Be friendly, helpful and concise.

Current product catalog:

{self.catalog_summary()}


When customers upload images:

- Identify the visible product.
- Compare it with available products.
- Explain price, stock and usefulness.
- Say when the image is unclear.

Never invent products that are not in the catalog.

"""



    def reset_history(self):
        self.history = [
            {
                "role": "system",
                "content": self.system_prompt()
            }
        ]


    # AI RESPONSE

    def reply(
        self,
        customer_message,
        image_bytes=None,
        image_mime_type=None,
        model=None,
        temperature=0.7
    ):


        selected_model = model
        if image_bytes and (not selected_model or "vision" not in selected_model.lower()):
            selected_model = self.vision_model
        elif not selected_model:
            selected_model = self.text_model


        user_content = customer_message



        # IMAGE REQUEST

        if image_bytes:


            model = self.vision_model


            mime = (
                image_mime_type
                or
                "image/png"
            )


            encoded = base64.b64encode(
                image_bytes
            ).decode(
                "utf-8"
            )


            user_content = [

                {
                    "type": "text",
                    "text": customer_message
                },


                {

                    "type": "image_url",

                    "image_url":
                    {
                        "url":
                        f"data:{mime};base64,{encoded}"
                    }

                }

            ]



        # ADD USER MESSAGE

        self.history.append(

            {
                "role": "user",
                "content": user_content
            }

        )



        try:


            response = self.client.chat.completions.create(

                model=selected_model,

                messages=self.history,

                temperature=temperature

            )



            answer = (
                response
                .choices[0]
                .message
                .content
            )



        except Exception as e:


            answer = (
                f"Sorry, I encountered an error: {e}"
            )



        # SAVE MEMORY

        self.history.append(

            {
                "role": "assistant",
                "content": answer
            }

        )



        return answer