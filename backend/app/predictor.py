"""Plant leaf disease inference using the ConCaPlant PlantVillage ONNX model."""

from __future__ import annotations

import json
import os
import urllib.request
from pathlib import Path

import numpy as np
import onnxruntime as ort
from PIL import Image

MODEL_DIR = Path(os.getenv("MODEL_DIR", Path(__file__).resolve().parent.parent / "models"))
MODEL_PATH = MODEL_DIR / "plantvillage.onnx"
LABELS_PATH = MODEL_DIR / "class_names.json"
MODEL_URL = "https://huggingface.co/imaflower/plantvillage-mobilenetv3/resolve/main/model.onnx?download=true"
LABELS_URL = "https://huggingface.co/imaflower/plantvillage-mobilenetv3/resolve/main/class_names.json?download=true"

_MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
_STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)
_SESSION: ort.InferenceSession | None = None
_LABELS: list[str] | None = None


def _download(url: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".part")
    urllib.request.urlretrieve(url, temporary)
    temporary.replace(destination)


def _ensure_model() -> None:
    if not MODEL_PATH.exists():
        _download(MODEL_URL, MODEL_PATH)
    if not LABELS_PATH.exists():
        _download(LABELS_URL, LABELS_PATH)


def _load() -> tuple[ort.InferenceSession, list[str]]:
    global _SESSION, _LABELS
    if _SESSION is None or _LABELS is None:
        _ensure_model()
        _SESSION = ort.InferenceSession(str(MODEL_PATH), providers=["CPUExecutionProvider"])
        _LABELS = json.loads(LABELS_PATH.read_text(encoding="utf-8"))
    return _SESSION, _LABELS


def _preprocess(image: Image.Image) -> np.ndarray:
    image = image.convert("RGB")
    image.thumbnail((256, 256), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (256, 256))
    left = (256 - image.width) // 2
    top = (256 - image.height) // 2
    canvas.paste(image, (left, top))
    array = np.asarray(canvas, dtype=np.float32) / 255.0
    array = (array - _MEAN) / _STD
    return np.transpose(array, (2, 0, 1))[None, ...].astype(np.float32)


def _humanize(label: str) -> tuple[str, str]:
    parts = label.split("___", 1)
    crop = parts[0].replace("_", " ") if parts else "Unknown"
    disease = parts[1].replace("_", " ") if len(parts) == 2 else label
    disease = disease.replace("  ", " ")
    return crop, disease


def predict(image: Image.Image, top_k: int = 3) -> dict:
    session, labels = _load()
    tensor = _preprocess(image)
    input_name = session.get_inputs()[0].name
    logits = session.run(None, {input_name: tensor})[0][0]
    logits = logits.astype(np.float64)
    logits -= np.max(logits)
    probabilities = np.exp(logits) / np.exp(logits).sum()
    indices = np.argsort(probabilities)[::-1][:top_k]

    predictions = []
    for index in indices:
        label = labels[int(index)]
        crop, disease = _humanize(label)
        predictions.append(
            {
                "label": label,
                "crop": crop,
                "disease": disease,
                "confidence": round(float(probabilities[int(index)]) * 100, 2),
            }
        )

    best = predictions[0]
    return {
        "crop": best["crop"],
        "disease": best["disease"],
        "label": best["label"],
        "confidence": best["confidence"],
        "predictions": predictions,
        "model": "ConCaPlant / PlantVillage (15-class ONNX)",
        "warning": "Screening aid only. Field photos can produce lower accuracy than curated PlantVillage images; confirm important diagnoses with a qualified agronomist.",
    }
