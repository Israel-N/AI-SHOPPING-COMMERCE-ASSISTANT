import base64
from groq import Groq
import os
from pathlib import Path

from inventory.products import products

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

class ShoppingAgent:

    def __init__(self):
        project_root = Path(__file__).resolve().parents[1]
        env_files = [project_root / ".env", project_root / "example.env"]

        if load_dotenv:
            for env_file in env_files:
                if env_file.exists():
                    load_dotenv(env_file)
                    break

        api_key = os.getenv("GROQ_API_KEY")
        if not api_key or api_key == "your_api_key_here":
            raise RuntimeError(
                "GROQ_API_KEY is not configured. "
                "Set GROQ_API_KEY in your environment or .env file."
            )

        self.client = Groq(api_key=api_key)
        self.text_model = os.getenv("GROQ_TEXT_MODEL", "llama-3.3-70b-versatile")
        self.vision_model = os.getenv(
            "GROQ_VISION_MODEL",
            "meta-llama/llama-4-scout-17b-16e-instruct",
        )

    def _catalog_summary(self):
        lines = []

        for product_name, details in products.items():
            price = details.get("price", "unknown")
            stock = details.get("stock", "unknown")
            lines.append(f"- {product_name}: ${price}, stock {stock}")

        return "\n".join(lines)

    def _system_prompt(self):
        return f"""
        You are PINKS, an AI sales assistant.
        If a customer asks your name, say: "My name is PINKS."

        Help customers:
        - find products
        - compare products
        - recommend products
        - place orders
        - answer questions
        - understand uploaded product images

        Current product catalog:
        {self._catalog_summary()}

        When a customer uploads an image, identify the visible product or product type,
        compare it with relevant catalog products, and explain practical differences like
        price, likely use case, stock, and recommendation. If the image is unclear, say so.

        Be friendly and concise.
        """

    def reply(self, customer_message, image_bytes=None, image_mime_type=None):
        model = self.text_model
        user_content = customer_message

        if image_bytes:
            model = self.vision_model
            mime_type = image_mime_type or "image/png"
            encoded_image = base64.b64encode(image_bytes).decode("utf-8")
            user_content = [
                {
                    "type": "text",
                    "text": customer_message,
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{mime_type};base64,{encoded_image}",
                    },
                },
            ]

        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": self._system_prompt()
                },
                {
                    "role": "user",
                    "content": user_content
                }
            ]
        )

        return response.choices[0].message.content
