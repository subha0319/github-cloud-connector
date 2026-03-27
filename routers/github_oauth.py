from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
import httpx
from config import settings

router = APIRouter(tags=["Authentication"])

GITHUB_AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
GITHUB_ACCESS_TOKEN_URL = "https://github.com/login/oauth/access_token"

@router.get("/login")
async def login_via_github():
    # We ask for the 'repo' scope so we have permission to read/write repositories and issues
    url = f"{GITHUB_AUTHORIZE_URL}?client_id={settings.GITHUB_CLIENT_ID}&scope=repo"
    return RedirectResponse(url)

@router.get("/callback")
async def github_callback(request: Request, code: str):
    if not code:
        raise HTTPException(status_code=400, detail="Authorization code not provided")
    
    # Exchange the temporary code for an access token
    async with httpx.AsyncClient() as client:
        response = await client.post(
            GITHUB_ACCESS_TOKEN_URL,
            headers={"Accept": "application/json"},
            data={
                "client_id": settings.GITHUB_CLIENT_ID,
                "client_secret": settings.GITHUB_CLIENT_SECRET,
                "code": code
            }
        )
        
    data = response.json()
    access_token = data.get("access_token")
    
    if not access_token:
        error_desc = data.get("error_description", "Unknown error")
        raise HTTPException(status_code=400, detail=f"Failed to retrieve token: {error_desc}")
    
    # Securely store the token in the user's session cookie
    request.session["access_token"] = access_token
    
    return {
        "status": "success", 
        "message": "Successfully authenticated with GitHub!",
        "note": "Your access token is now securely stored in your session."
    }