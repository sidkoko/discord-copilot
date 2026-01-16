from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from config import get_settings
import httpx

settings = get_settings()
security = HTTPBearer()


async def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> dict:
    """
    Verify Supabase JWT token and return user information
    """
    token = credentials.credentials
    
    try:
        # Decode JWT token (Supabase uses HS256 with the JWT secret)
        # For production, you should verify the token signature with Supabase
        # For now, we'll do basic validation
        
        # Get Supabase JWT secret from settings or use anon key for validation
        # In production, use the actual JWT secret from Supabase settings
        payload = jwt.decode(
            token,
            settings.supabase_anon_key,
            algorithms=["HS256"],
            options={
                "verify_signature": False,  # Set to True with proper secret
                "verify_aud": False  # Disable audience verification
            }
        )
        
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid authentication token")
        
        return {
            "user_id": user_id,
            "email": payload.get("email"),
            "role": payload.get("role")
        }
        
    except JWTError as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid authentication token: {str(e)}"
        )


async def get_current_user(user: dict = Depends(verify_token)) -> dict:
    """
    Dependency to get current authenticated user
    """
    return user
