# Voice-Commerce-Bot
Shopping bot to assist customers needs of a product using groq 
# Voice Shopping Assistant

A Python-powered AI voice assistant that allows customers to interact with an online store using natural speech.

The assistant listens to customer requests through a microphone, converts speech into text, sends the request to an AI model, generates an intelligent response, and speaks the response back to the customer.

---

# Features

Voice Recognition

* Captures customer speech using a microphone
* Converts speech into text
* Handles ambient noise adjustment

AI Customer Assistant

* Understands customer questions
* Recommends products
* Answers shopping-related queries
* Simulates a virtual sales representative

Product Inventory

* Local product catalog
* Product lookup functionality
* Stock and price information

Order Management

* Add products to cart
* View cart contents
* Checkout functionality

Voice Responses

* Converts AI responses to speech
* Reads responses aloud to customers

---

# Project Structure

```text
voice-commerce-bot/

├── main.py
│
├── app/voice/
│   ├── speech_to_text.py
│   └── text_to_speech.py
│
├── ai/
│   └── shopping_agent.py
│
├── inventory/
│   └── products.py
│
├── orders/
│   └── order_manager.py
│
└── database/
    └── db.py
```

---

# How It Works

```text
Customer Speaks
       │
       ▼
speech_to_text.py
       │
       ▼
Text Generated
       │
       ▼
shopping_agent.py
       │
       ▼
Groq AI Model
       │
       ▼
AI Response
       │
       ▼
text_to_speech.py
       │
       ▼
Customer Hears Reply
```

---

# Application Flow

```text
┌──────────────┐
│   Customer   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Microphone   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Speech To    │
│ Text Module  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Shopping AI  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Groq LLM     │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Response     │
│ Generated    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Text To      │
│ Speech       │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Customer     │
└──────────────┘
```

---

# Components

## speech_to_text.py

Responsible for:

* Listening through the microphone
* Adjusting for background noise
* Converting speech to text

Main Class:

```python
VoiceRecognizer
```

Main Method:

```python
listen()
```

---

## shopping_agent.py

Responsible for:

* Sending customer messages to Groq
* Generating AI-powered responses
* Acting as a virtual shopping assistant

Main Class:

```python
ShoppingAgent
```

Main Method:

```python
reply()
```

---

## text_to_speech.py

Responsible for:

* Converting text responses into speech
* Playing audio through the system speaker

Main Function:

```python
speak()
```

---

## products.py

Contains:

* Product inventory
* Product prices
* Product stock levels

Example:

```python
products = {
    "iphone 15": {
        "price": 1200,
        "stock": 12
    }
}
```

---

## order_manager.py

Handles:

* Cart management
* Adding products
* Viewing cart contents
* Checkout process

Main Class:

```python
OrderManager
```

Methods:

```python
add_to_cart()
view_cart()
checkout()
```

---

## db.py

Database connection layer.

Provides:

```python
get_db()
```

Used for connecting to PostgreSQL using SQLAlchemy.

---

## main.py

Application entry point.

Responsible for:

* Starting the assistant
* Listening continuously
* Sending customer messages to AI
* Speaking responses

Execution loop:

```python
while True:
    customer_message = voice.listen()

    answer = agent.reply(customer_message)

    speak(answer)
```

---

# Installation

## Clone Repository

```bash
git clone <repository-url>

cd voice_shop
```

## Create Virtual Environment

Windows

```bash
python -m venv venv

venv\Scripts\activate
```

Linux / macOS

```bash
python -m venv venv

source venv/bin/activate
```

---

# Install Dependencies

```bash
pip install fastapi
pip install groq
pip install speechrecognition
pip install pyaudio
pip install gtts
pip install pygame
pip install sqlalchemy
pip install psycopg2-binary
pip install python-dotenv
```

Or:

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a file named:

```text
.env
```

Add:

```env
GROQ_API_KEY=your_groq_api_key

DATABASE_URL=postgresql://user:password@localhost:5432/shopdb
```

---

# Running The Application

Start the assistant:

```bash
python main.py
```

Expected output:

```text
Voice Shopping Assistant Started

Listening...
```

Speak into your microphone.

Example:

```text
Do you have Samsung phones?
```

Assistant:

```text
Yes, we currently have the Samsung S24 available for $950.
```

---

# Example Session

```text
Customer:
Hello

Assistant:
Welcome to our store.
How can I help you today?

Customer:
Do you have Samsung phones?

Assistant:
Yes. We currently have the Samsung S24 available.

Customer:
Add one to my cart.

Assistant:
Samsung S24 has been added to your cart.

Customer:SHOPPING ASSISTANT ARCHITECTURE.png

Exit
```

---

# Current Limitations

* Inventory stored locally in Python
* No real payment integration
* No user authentication
* No order persistence
* No conversation memory
* Single-user operation
