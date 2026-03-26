from fastapi import FastAPI, Depends, HTTPException, Header, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from app.agents.portfolio_brain import agent_executor
import json
import os

app = FastAPI(title="Sree Harshitha's AI Portfolio Backend")

# 1. CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Simple Security Logic (The "Secret Key" check)
async def verify_admin_key(x_admin_key: str = Header(None)):
    """Matches the key provided in headers against your environment variable"""
    ADMIN_SECRET = os.getenv("ADMIN_SECRET_KEY", "malla_reddy_2026") # Fallback for dev
    if x_admin_key != ADMIN_SECRET:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing Admin Security Key"
        )
    return x_admin_key

# 3. The Streaming Chat Endpoint
@app.post("/chat")
async def chat_endpoint(payload: dict[str, str], authorized=Depends(verify_admin_key)):
    user_input = payload.get("message")
    if not user_input:
        raise HTTPException(status_code=400, detail="No message provided")

    async def event_generator():
        try:
            # Using LangChain's astream to send chunks to the frontend
            async for chunk in agent_executor.astream({"input": user_input}):
                if "output" in chunk:
                    # Clean JSON chunk for the React frontend
                    yield f"data: {json.dumps({'content': chunk['output']})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.get("/health")
def health_check():
    return {
        "status": "online", 
        "system": "harshitha-v2",
        "architecture": "AMD64",
        "storage": "D-Drive Optimized"
    }