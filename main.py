from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

app = FastAPI()

# Netlify aṭanga i app in a rawn biak theih nan
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "MsVoice Backend chu a nung e!"}

@app.post("/process-audio/")
async def process_audio(file: UploadFile = File(...)):
    # File rawn thawn chu a lo dawng ang
    file_location = f"temp_{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Hetah hian AI model (Demucs) a lo thawk dawn a ni
    # Tunah rih chuan file a lo dawng thei em tih kan test phawt ang
    
    os.remove(file_location)
    return {"filename": file.filename, "status": "Audio tluang takin ka lo dawng e! AI in a process mek..."}
