from fastapi import Header, HTTPException, status
from jose import jwt, JWTError
import os
from dotenv import load_dotenv

load_dotenv()

# These come from your Supabase Dashboard -> Project Settings -> API
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")
ALGORITHM = "HS256"

async def verify_admin_token(authorization: str = Header(None)):
    """
    Dependency that validates the Supabase JWT token.
    Only allows the request if the token is valid.
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing",
        )

    try:
        # Standard format is "Bearer <token>"
        token = authorization.split(" ")[1]
        
        # Decode the token using Supabase's secret
        payload = jwt.decode(token, SUPABASE_JWT_SECRET, algorithms=[ALGORITHM], options={"verify_aud": False})
        
        # Optional: Check if the user ID matches your specific Admin UID
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")
            
        return payload # Returns user data if valid
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    except IndexError:
        raise HTTPException(status_code=401, detail="Bearer token malformed")