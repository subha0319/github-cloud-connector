from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
import httpx

router = APIRouter(tags=["GitHub Actions"])

# Define what data we expect from the user when creating an issue
class IssueCreate(BaseModel):
    title: str
    body: str | None = None

# A helper function to grab the token and handle unauthorized users
def get_github_headers(request: Request):
    token = request.session.get("access_token")
    if not token:
        raise HTTPException(
            status_code=401, 
            detail="Not authenticated. Please go to /login first."
        )
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }

@router.get("/repos")
async def fetch_repositories(request: Request):
    """Fetches a list of repositories for the authenticated user."""
    headers = get_github_headers(request)
    
    async with httpx.AsyncClient() as client:
        # Make the real API call to GitHub
        response = await client.get("https://api.github.com/user/repos?sort=updated", headers=headers)
        
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch repositories from GitHub.")
        
    # Return a simplified list of repos (just names and URLs) so it's clean
    repos = response.json()
    return [{"name": repo["name"], "url": repo["html_url"], "private": repo["private"]} for repo in repos]

@router.post("/create-issue")
async def create_issue(request: Request, owner: str, repo: str, issue: IssueCreate):
    """Creates a new issue in a specific repository."""
    headers = get_github_headers(request)
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://api.github.com/repos/{owner}/{repo}/issues",
            headers=headers,
            json={"title": issue.title, "body": issue.body}
        )
        
    if response.status_code != 201:
        raise HTTPException(
            status_code=response.status_code, 
            detail=f"GitHub API Error: {response.json().get('message', 'Unknown error')}"
        )
        
    data = response.json()
    return {
        "status": "success", 
        "message": "Issue created successfully!",
        "issue_url": data.get("html_url")
    }