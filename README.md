# Crop Doctor 🌿

AI-based crop leaf disease screening system for the SIH trial project.

## What works now

- Farmer-facing React/Vite interface for leaf photo upload
- JPG, PNG and WebP validation (10 MB limit)
- FastAPI `/api/predict` endpoint
- ONNX Runtime CPU inference
- Automatic first-run download of the 15-class ConCaPlant PlantVillage model
- Top prediction + confidence + top alternatives
- Health endpoint at `/api/health`
- Clear limitation warning for field photos

The model is the lightweight **ConCaPlant / PlantVillage** classifier published by `imaflower/plantvillage-mobilenetv3`. Its model card reports a 15-class classifier and high test/validation accuracy on PlantVillage, but also warns that PlantVillage images are curated and that performance can drop on real field photos. This application therefore treats the output as screening, not a definitive diagnosis.

## Architecture

```text
Farmer phone / browser
        │
        ▼
React + Vite frontend
        │  multipart image upload
        ▼
FastAPI backend
        │
        ▼
ONNX Runtime
        │
        ▼
ConCaPlant / PlantVillage model
        │
        ▼
Disease + crop + confidence + alternatives
```

## Run locally

### Prerequisites

- Node.js LTS
- Python 3.11+
- Git

### Backend

From the repository root:

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

On the **first prediction**, the backend downloads the model and label file from Hugging Face into `backend/models/`. The model files are intentionally not committed to Git because binary weights should not live in this source repository.

API docs: `http://127.0.0.1:8000/docs`

### Frontend

Open a second terminal:

```powershell
cd frontend
npm.cmd install
npm.cmd run dev
```

Open the Vite URL shown in the terminal, normally `http://localhost:5173`.

For a deployed backend, set:

```text
VITE_API_URL=https://your-api.example.com
```

## API

`POST /api/predict`

Form field:

- `file`: JPG, PNG or WebP leaf image

Example response:

```json
{
  "crop": "Tomato",
  "disease": "Early blight",
  "confidence": 91.42,
  "predictions": [
    {"label": "Tomato___Early_blight", "crop": "Tomato", "disease": "Early blight", "confidence": 91.42}
  ]
}
```

## Important limitation

PlantVillage is a curated research dataset. A model that performs well on PlantVillage can still fail on photographs from farms because of lighting, background, cultivar differences, multiple diseases, occlusion, insects, nutrient deficiencies and symptoms that are visually similar. The current MVP should **not** prescribe pesticides or claim a confirmed diagnosis.

For an SIH-ready production version, the next essential upgrades are field-image validation, India-specific crop/disease data, confidence calibration, expert-reviewed recommendations, multilingual voice guidance, and offline/low-bandwidth support.

## Attribution

- Disease model: `imaflower/plantvillage-mobilenetv3` (MIT license), Hugging Face.
- Training dataset: PlantVillage, originally described by Mohanty, Hughes & Salathé (2016).
