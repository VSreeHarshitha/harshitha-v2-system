import httpx
import os
from dotenv import load_dotenv
from app.schemas.portfolio_models import PortfolioUpdate

load_dotenv()

N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")

async def trigger_n8n_workflow(payload: PortfolioUpdate, admin_id: str):
    """
    Sends validated data to n8n to start the automation (Supabase update + Deploy).
    """
    async with httpx.AsyncClient() as client:
        # Convert the Pydantic model to a dictionary
        data = payload.dict(exclude_none=True)
        
        # Add metadata for n8n to use in the Approval step
        data["admin_id"] = admin_id
        
        try:
            response = await client.post(N8N_WEBHOOK_URL, json=data)
            response.raise_for_status()
            return {"status": "success", "message": "Workflow triggered! Check your phone for approval."}
        except httpx.HTTPStatusError as e:
            return {"status": "error", "message": f"n8n connection failed: {e.response.status_code}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}