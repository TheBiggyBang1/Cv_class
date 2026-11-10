"""
Interface web de Cv_class : API FastAPI + page statique.

    uvicorn app:app --reload      # puis http://localhost:8000
"""

import os
import tempfile
from pathlib import Path

import anthropic
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

import cv_screener as cs

FORMATS = {".pdf", ".docx", ".txt"}
TAILLE_MAX = 10 * 1024 * 1024  # 10 Mo par CV
FRONT = Path(__file__).parent / "front"

app = FastAPI(title="Cv_class")
_client = None


def client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        if not os.getenv("ANTHROPIC_API_KEY"):
            raise HTTPException(
                500,
                "Clé API absente : copiez .env.example en .env, "
                "renseignez ANTHROPIC_API_KEY, puis relancez le serveur.",
            )
        _client = anthropic.Anthropic()
    return _client


@app.get("/")
def page() -> FileResponse:
    return FileResponse(FRONT / "index.html")


@app.get("/api/config")
def config() -> dict:
    return {
        "ecoles": cs.ECOLES_PRIORITAIRES,
        "ecole_eliminatoire": cs.ECOLE_ELIMINATOIRE,
    }


@app.post("/api/evaluer")
def evaluer(fichier: UploadFile = File(...)) -> dict:
    """Évalue un CV. Le fichier est supprimé dès la réponse envoyée."""
    nom = Path(fichier.filename or "cv").name
    if Path(nom).suffix.lower() not in FORMATS:
        raise HTTPException(415, "Format non pris en charge : utilisez PDF, Word (.docx) ou texte.")

    contenu = fichier.file.read(TAILLE_MAX + 1)
    if len(contenu) > TAILLE_MAX:
        raise HTTPException(413, "Fichier trop lourd : 10 Mo maximum.")

    api = client()
    with tempfile.TemporaryDirectory() as tmp:
        chemin = Path(tmp) / nom
        chemin.write_bytes(contenu)
        return cs.evaluer(api, chemin)
