from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from deepface import DeepFace
import tempfile

app = FastAPI()

# Allow CORS for your Expo app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" to your app URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "DeepFace API is running"}

@app.post("/detect-mood")
async def detect_mood(file: UploadFile = File(...)):
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        analysis = DeepFace.analyze(tmp_path, actions=["emotion"], enforce_detection=False)
        return {
            "dominant_emotion": analysis[0]['dominant_emotion'],
            "details": analysis[0]['emotion']
        }
    except Exception as e:
        return {"error": str(e)}
