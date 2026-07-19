from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import replicate
import os
import shutil

app = FastAPI()

# Frontend aṭanga dâlna awm lova a lo biak theih nan
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Link (URL) dawn theihna tur model
class AudioURL(BaseModel):
    url: str

@app.get("/")
def read_root():
    return {"message": "MsVoice Backend chu a nung e! (URL dawng thei tawh)"}

# 1. Endpoint Hlui (File tawi atan - i la mamawh palh takin)
@app.post("/process-audio/")
async def process_audio(file: UploadFile = File(...)):
    file_location = f"temp_{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        with open(file_location, "rb") as audio_file:
            output = replicate.run(
                "cjwbw/demucs:25a173108cff36ef9f80f854c162d01df9e6528be175794b81158fa03836d953",
                input={"audio": audio_file}
            )
        os.remove(file_location)
        return {"status": "success", "clean_audio_url": output.get("vocals")}
        
    except Exception as e:
        if os.path.exists(file_location):
            os.remove(file_location)
        return {"error": str(e)}

# 2. ENDPOINT THAR: File lian pui pui atan (Link chauh a dawng ang)
@app.post("/process-url/")
async def process_url(req: AudioURL):
    try:
        # Replicate AI hian file rit pui pui kha URL (link) aṭangin direct-in a pawt lut thei!
        output = replicate.run(
            "cjwbw/demucs:25a173108cff36ef9f80f854c162d01df9e6528be175794b81158fa03836d953",
            input={"audio": req.url}
        )
        return {"status": "success", "clean_audio_url": output.get("vocals")}
    except Exception as e:
        return {"error": str(e)}
