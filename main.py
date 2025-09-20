from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


# Replace this with your actual n8n webhook URL
N8N_WEBHOOK_URL = "https://uddinhafiz594.app.n8n.cloud/webhook/33d531a5-a62a-4504-865d-ea949b8efbd3"

# Input model
class ArticleRequest(BaseModel):
    email: str
    article_url: str

@app.post("/process-article")
def process_article(request: ArticleRequest):
    # Generate unique session_id
    session_id = str(uuid.uuid4())

    # Prepare payload
    payload = {
        "email": request.email,
        "article_url": request.article_url,
        "session_id": session_id
    }

    # Send data to n8n webhook
    try:
        response = requests.post(N8N_WEBHOOK_URL, json=payload)
        response.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to call n8n webhook: {str(e)}")

    return {
        "message": "Article sent to n8n successfully",
        "session_id": session_id
    }
