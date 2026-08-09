"""The FastAPI entry point for Crop Doctor.

This starter API only proves that the frontend can communicate with the
backend. Prediction, uploads, and database code are added in later steps.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Crop Doctor API", version="0.1.0")

# Vite's development server uses port 5173. Limit browser access to that
# local address during development instead of allowing every website.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=[],
)


@app.get("/api/health")
def health_check() -> dict[str, str]:
    """Return a simple response confirming the backend is available."""
    return {"status": "ok", "service": "crop-doctor-api"}
