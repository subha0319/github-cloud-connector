import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class Settings:
    # GitHub OAuth Credentials
    GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
    GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
    
    # We will need a secret key to securely sign our session cookies later
    SESSION_SECRET = os.getenv("SESSION_SECRET", "a-very-secret-string-for-local-dev")

# Create an instance of the settings to import elsewhere
settings = Settings()