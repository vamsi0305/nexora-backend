import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-8b-8192")

client = Groq(api_key=GROQ_API_KEY)

def generate_completion(prompt: str, system_message: str = "You are a helpful assistant."):
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        model=GROQ_MODEL,
        temperature=0.7,
        max_tokens=2048
    )
    return chat_completion.choices[0].message.content
