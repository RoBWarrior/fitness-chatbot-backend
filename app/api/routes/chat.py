from fastapi import APIRouter, HTTPException
from app.services.llm import hydrate_session, call_llm, format_history
from app.services.search import search_serpai
from app.services.retriever import query_similar
from app.services.db_helpers import create_session, get_user_sessions, save_message, get_chat_history, delete_session

router = APIRouter()

@router.get("/{session_id}/history")
async def get_history(session_id: int):
    # db_history is [(sender_type, content, timestamp), ...]
    db_history = get_chat_history(session_id)
    history_list = [
        {"sender_type": row[0], "content": row[1], "timestamp": row[2]} 
        for row in db_history
    ]
    return {"history": history_list}

@router.post("/{session_id}")
async def chat_with_bot(user_id: int, session_id: int, message: str, use_kb: bool = True, use_web: bool = False, top_k: int = 3):

    session = hydrate_session(session_id)
    
    context = ""
    if use_kb:
        # Pass user_id to isolate documents
        results = query_similar(message, user_id=user_id, top_k=top_k) 
        context += "\n".join(results)

    if use_web:
        web_results = search_serpai(message, num_results=3)
        context += "\nWeb results:\n" + "\n".join(web_results)

    prompt_message = message
    if context:
        prompt_message = f"{message}\n\nRelevant context:\n{context}"

    # Call Gemini LLM using contextual message
    answer = call_llm(session, prompt_message)

    # Save to Database using original message and response
    save_message(session_id, "user", message)
    save_message(session_id, "assistant", answer)

    return {"answer": answer, "session_id": session_id, "chat_history": format_history(session)}

@router.delete("/{session_id}")
async def remove_session(session_id: int):
    success = delete_session(session_id)
    if success:
        return {"status": "success", "message": "Chat session deleted"}
    else:
        raise HTTPException(status_code=500, detail="Failed to delete chat session")
