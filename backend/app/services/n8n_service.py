import httpx
import os
from dotenv import load_dotenv
from typing import Dict, Any

# Ensure environment variables are loaded
load_dotenv()

# n8n is the service name in your docker-compose, so we use 'automation' as the host
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "http://automation:5678/webhook/portfolio-update")

async def trigger_n8n_workflow(payload: Any, admin_id: str) -> Dict[str, Any]:
    """
    Sends validated data to n8n to start the Human-in-the-Loop 
    Approval process via WhatsApp.
    """
    async with httpx.AsyncClient() as client:
        # Convert the Pydantic model to a dictionary safely
        # model_dump is the modern Pydantic v2 way (replaces .dict())
        data = payload.model_dump(exclude_none=True)
        
        # Inject metadata for the n8n Approval node
        data["admin_id"] = admin_id
        data["source"] = "Project-P-Core-Agent"

        try:
            # We add a 10s timeout to ensure the AI doesn't wait forever
            response = await client.post(
                N8N_WEBHOOK_URL, 
                json=data, 
                timeout=10.0
            )
            response.raise_for_status()
            
            return {
                "status": "success", 
                "message": "Update request dispatched. Check WhatsApp for approval, Harshitha!"
            }
            
        except httpx.HTTPStatusError as e:
            return {
                "status": "error", 
                "message": f"n8n logic error: {e.response.status_code}"
            }
        except Exception as e:
            # Handle cases where n8n container might be down
            return {
                "status": "error", 
                "message": f"Nervous system offline: {str(e)}"
            }