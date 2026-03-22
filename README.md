# Chatbot Backend

This is the FastAPI backend for the specialized chatbot application. It handles user authentication, session chat history, LLM integrations (Gemini), and document uploads via ChromaDB.

## Requirements
- Python 3.8+
- PostgreSQL (if configured for psycopg2, or SQLite fallback)
- Gemini API Key

## Setup & Running

1. **Navigate to the backend directory**
   ```bash
   cd backend
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**
   Make sure you have a `.env` file in the `backend/` folder with your required keys:
   ```env
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

5. **Start the Server**
   ```bash
   uvicorn app.main:app --reload
   ```
   The backend will now be running on `http://127.0.0.1:8000`.

## Configuration
To change the chatbot's identity and system directions, modify `persona.json`. The frontend fetches this configuration to adjust the UI dynamically.
