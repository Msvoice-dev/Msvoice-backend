from fastapi import FastAPI, UploadFile, File
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

@app.get("/")
def read_root():
    return {"message": "MsVoice Backend chu a nung e! (AI thluak nen)"}

@app.post("/process-audio/")
async def process_audio(file: UploadFile = File(...)):
    # 1. Aw (audio) file rawn thleng chu server-ah kan vawng ṭha lawk ang
    file_location = f"temp_{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        # 2. Chu aw chu Demucs (Replicate AI) hnenah tihfai turin kan thawn dawn a ni
        with open(file_location, "rb") as audio_file:
            output = replicate.run(
                "cjwbw/demucs:25a173108cff36ef9f80f854c162d01df9e6528be175794b81158fa03836d953",
                input={"audio": audio_file}
            )
        
        # 3. AI in a rawn tihfai hnuah, kan thil save chawp kha hmun a awh loh nan kan paih bo leh ang
        os.remove(file_location)
        
        # 4. AI in a thliar hrang a (music leh aw), a aw fai hlir (vocals) chu kan thawn kir ang
        return {
            "filename": file.filename, 
            "status": "Hlawhtling takin AI-in a tifai e!", 
            "clean_audio_url": output.get("vocals") 
        }
        
    except Exception as e:
        # Fello a awm palh pawhin file hnawk kan paih fai tho ang
        if os.path.exists(file_location):
            os.remove(file_location)
        return {"error": f"AI in a process thei lo: {str(e)}"}
