from fastapi import FastAPI, Depends, HTTPException, Header, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import json
import os
import asyncio

# This matches your portfolio agent logic
from app.agents.portfolio_brain import portfolio_agent 

app = FastAPI(title="Project P: Harshitha's AI Portfolio")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def verify_admin_key(x_admin_key: str = Header(None)):
    # Make sure this matches your Frontend!
    ADMIN_SECRET = os.getenv("ADMIN_SECRET_KEY", "malla_reddy_2026")
    if x_admin_key != ADMIN_SECRET:
        print(f"Auth Failed: Received {x_admin_key}") # Debugging
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized access"
        )
    return x_admin_key

@app.post("/chat")
async def chat_endpoint(request: Request, authorized=Depends(verify_admin_key)):
    payload = await request.json()
    user_input = payload.get("message")
    
    if not user_input:
        raise HTTPException(status_code=400, detail="Empty message")

    async def event_generator():
        try:
            # We use run_stream from Pydantic AI
            async with portfolio_agent.run_stream(user_input) as result:
                async for message in result.stream_text():
                    # Ensure the JSON key is exactly 'content'
                    yield f"data: {json.dumps({'content': str(message)})}\n\n"
        except Exception as e:
            print(f"AI Error: {str(e)}")
            yield f"data: {json.dumps({'content': '⚠️ AI Error: Check your API Key in .env'})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.get("/health")
def health_check():
    return {"status": "online", "system": "Project-P-Core"}