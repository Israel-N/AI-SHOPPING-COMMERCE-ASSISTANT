from groq import Groq
import os
from pathlib import Path

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

    def reply(self, customer_message):

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": """
                    You are an AI sales assistant.

                    Help customers:
                    - find products
                    - compare products
                    - recommend products
                    - place orders
                    - answer questions

                    Be friendly and concise.
                    """
                },
                {
                    "role": "user",
                    "content": customer_message
                }
            ]
        )

        return response.choices[0].message.content