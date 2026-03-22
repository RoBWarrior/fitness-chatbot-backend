import google.generativeai as genai
from app.core.config import GOOGLE_API_KEY
import os
import json

genai.configure(api_key=GOOGLE_API_KEY)

config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "persona.json")
try:
    with open(config_path, "r") as f:
        persona = json.load(f)
    sys_prompt = persona.get("system_prompt", "You are a helpful assistant.")
except FileNotFoundError:
    sys_prompt = "You are a helpful assistant."

model = genai.GenerativeModel(
    "gemini-2.5-flash",
    system_instruction=sys_prompt
)

from app.services.db_helpers import get_chat_history

def hydrate_session(session_id: int):
    # Fetch from DB: [(sender_type, content, timestamp), ...]
    db_history = get_chat_history(session_id)
    gemini_history = []
    for sender_type, content, _ in db_history:
        # map 'assistant' back to 'model' for gemini
        role = "model" if sender_type == "assistant" else "user"
        gemini_history.append({
            "role": role,
            "parts": [content]
        })
    return model.start_chat(history=gemini_history)

def format_history(session):
    """Convert Gemini session.history into a JSON-friendly list."""
    formatted = []
    for turn in session.history:
        role = "user" if turn.role == "user" else "assistant"
        formatted.append({
            "role": role,
            "content": turn.parts[0].text if turn.parts else ""
        })
    return formatted

def call_llm(chat_session, prompt: str) -> str:
    try:
        response = chat_session.send_message(prompt)
        return response.text
    except Exception as e:
        print(f"An error occurred while calling the LLM {e}")
        return ""
