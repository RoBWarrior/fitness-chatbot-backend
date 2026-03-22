from fastapi import APIRouter, HTTPException
from app.services.retriever import query_similar
from app.services.llm import hydrate_session, format_history, call_llm
from app.services.search import search_serpai
from app.services.db_helpers import create_session, save_message, get_user_sessions

router = APIRouter()

@router.get("/sessions/{user_id}")
async def list_user_queries(user_id: int):
    sessions = get_user_sessions(user_id)
    return {"sessions": [{"query_id": s[0], "start_time": s[1], "end_time": s[2]} for s in sessions]}

@router.post("/")
async def initial_query(
    user_id: int, 
    query: str, 
    top_k: int = 3, 
    use_kb: bool = True, 
    use_web: bool = False
):
    try:
        # A query creates a new session (query_id)
        query_id = create_session(user_id)
        if not query_id:
            raise HTTPException(status_code=500, detail="Failed to create a new query session")

        # Get fresh session
        session = hydrate_session(query_id)
        

        context = ""
        if use_kb:
            # Pass user_id to query_similar
            results = query_similar(query, user_id=user_id, top_k=top_k)
            context += "\n".join(results)

        if use_web:
            web_results = search_serpai(query, num_results=3)
            context += "\nWeb Search Results:\n" + "\n".join(web_results)

        # Build message (Gemini will keep chat history)
        prompt_message = query
        if context:
            prompt_message = f"{query}\n\nRelevant context:\n{context}"

        # Call Gemini LLM
        answer = call_llm(session, prompt_message)

        # Save to DB
        save_message(query_id, "user", query)
        save_message(query_id, "assistant", answer)

        return {
            "query": query,
            "answer": answer,
            "query_id": query_id,
            "context_used": use_kb,
            "web_used": use_web,
            "chat_history": format_history(session)   # <- JSON-safe now
        }

    except Exception as e:
        print(f"❌ Error in query: {e}")
        return {"query": query, "answer": f"Error occurred: {str(e)}"}
