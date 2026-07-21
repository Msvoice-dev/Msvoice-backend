from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import replicate
import os
from supabase import create_client, Client

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SUPABASE KEYS (Environment Variable aṭanga lak chhuah)
SUPABASE_URL = "https://nflzngxhrdtabooefhsk.supabase.co"
# Render-a i thuhruk tak kha a pawt chhuak dawn a ni
SUPABASE_KEY = os.environ.get("SUPABASE_SECRET_KEY") 
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class AudioURL(BaseModel):
    url: str
    file_id: str 

@app.get("/")
def read_root():
    return {"message": "MsVoice Backend (Supabase Enabled) chu a nung e!"}

@app.post("/process-url/")
async def process_url(req: AudioURL):
    try:
        supabase.table("upload_queue").update({"status": "processing"}).eq("id", req.file_id).execute()

        output = replicate.run(
            "cjwbw/demucs:25a173108cff36ef9f80f854c162d01df9e6528be175794b81158fa03836d953",
            input={"audio": req.url}
        )
        clean_url = output.get("vocals")

        supabase.table("upload_queue").update({"status": "completed"}).eq("id", req.file_id).execute()

        return {"status": "success", "clean_audio_url": clean_url}

    except Exception as e:
        supabase.table("upload_queue").update({"status": "failed"}).eq("id", req.file_id).execute()
        return {"error": str(e)}
