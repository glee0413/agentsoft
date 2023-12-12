from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
import uvicorn
import time
import os

app = FastAPI()

class PostRequest(BaseModel):
    challenge: str
    token: str
    type: str

class ResponseResult(BaseModel):
    challenge: str

class WebStatus():
    def __init__(self) -> None:
        self.ping_count = 0
        self.stage = 'test'

class AppCredential():
    def __init__(self) -> None:
        credential = {
            'test':{
                'APP_ID': os.getenv("APP_ID"),
                'APP_SECRET': os.getenv("APP_SECRET"),
                'VERIFICATION_TOKEN':os.getenv("VERIFICATION_TOKEN"),
                'ENCRYPT_KEY':os.getenv("ENCRYPT_KEY"),
                'LARK_HOST':os.getenv("LARK_HOST")
            }
        }
    def getAppCredential(self, stage: str):
        if stage in self.credential:
            return self.credential[stage]
        else:
            return {}

app_credential = AppCredential()

web_status = WebStatus()

@app.post("/url_verification")
async def url_verification(request: PostRequest):
    web_status.ping_count += 1
    try:
        print(time.strftime("%Y-%m-%d %H:%M:%S"), f"{web_status.ping_count}: {request.challenge}")
        if request.type == "url_verification":
            return ResponseResult(challenge=request.challenge)
        else:
            raise HTTPException(status_code=400, detail="Invalid request type")
    except Exception as e:
        print(f"Error processing POST request: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")




if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8264)
