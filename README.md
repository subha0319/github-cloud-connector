# GitHub Cloud Connector

A backend service built with Python and FastAPI that acts as a connector to the GitHub API. This project demonstrates secure integration with external APIs using the OAuth 2.0 web application flow.

## Features
* **Secure Authentication:** Implements GitHub OAuth 2.0 (Web Application Flow) to securely authenticate users without handling their raw credentials.
* **Session Management:** Utilizes encrypted browser cookies to manage user sessions.
* **API Integration:** * Fetches and lists all repositories for the authenticated user.
  * Creates new issues in specified repositories.
* **Modern Tech Stack:** Built with FastAPI for high performance and automatic interactive API documentation.

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/subha0319/github-cloud-connector.git
   cd "Cloud Connector"
   ```

2. **Create and activate a virtual environment:**
   * **Windows:**
     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```
   * **macOS/Linux:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   * Create a GitHub OAuth App in your GitHub Developer Settings.
   * Set the Homepage URL to `http://localhost:8000`.
   * Set the Authorization callback URL to `http://localhost:8000/callback`.
   * Create a `.env` file in the root directory and add the following:
     ```env
     GITHUB_CLIENT_ID=your_client_id_here
     GITHUB_CLIENT_SECRET=your_client_secret_here
     SESSION_SECRET=a_random_secure_string_for_cookies
     ```

## How to Run the Project

Start the FastAPI server using Uvicorn:
```bash
uvicorn main:app --reload
```
The server will start at `http://localhost:8000`. 

## API Endpoints

Once the server is running, you can visit `http://localhost:8000/docs` to view and test the interactive Swagger UI documentation.

### Authentication
* `GET /login` - Redirects the user to GitHub to authorize the application.
* `GET /callback` - Handles the OAuth redirect, exchanges the code for an access token, and stores it in a secure session cookie.

### GitHub Actions
* `GET /repos` - Fetches a list of repositories (names, URLs, and privacy status) for the authenticated user.
* `POST /create-issue` - Creates a new issue in a specific repository. 
  * **Query Parameters:** `owner` (string), `repo` (string)
  * **Body:** `title` (string), `body` (string, optional)
