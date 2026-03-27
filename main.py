from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from routers import github_oauth, github_actions
from config import settings

app = FastAPI(
    title="GitHub Cloud Connector",
    description="A simple cloud connector to authenticate with GitHub and perform API actions.",
    version="1.0.0"
)

# Add Session Middleware to securely store the OAuth token in encrypted cookies
app.add_middleware(SessionMiddleware, secret_key=settings.SESSION_SECRET)

# Include our new OAuth routes
app.include_router(github_oauth.router)
app.include_router(github_actions.router)

@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "Welcome to the GitHub Cloud Connector! Go to http://localhost:8000/login to authenticate."
    }