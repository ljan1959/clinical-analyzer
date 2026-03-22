from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import requests
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv("OPENAI_API_KEY")

@app.post("/analyze")
async def analyze(
    diagnosis: str = Form(""),
    symptoms: str = Form(""),
    spo2: str = Form(""),
    rr: str = Form(""),
    ventilator: str = Form(""),
    humidification: str = Form(""),
    suction: str = Form(""),
    other: str = Form(""),
    case_text: str = Form(""),
    images: list[UploadFile] = File([])
):

    full_input = f"""
DIAGNOSEN:
{diagnosis}

SYMPTOME:
{symptoms}

SpO2: {spo2}
RR: {rr}

BEATMUNGSGERÄT:
{ventilator}

AKTIVE BEFEUCHTUNG:
{humidification}

TRACHEALSEKRET:
{suction}

WEITERE PARAMETER:
{other}

FREITEXT:
{case_text}
"""

    prompt = f"""
Du bist ein klinisch-anatomisch-pathophysiologischer Analysespezialist.

Erstelle eine extrem detaillierte Analyse auf Deutsch.

WICHTIG:
- akademischer Stil
- Fokus auf Physik und Chemie
- keine Therapieanweisungen
- Geräteparameter analysieren
- Richtungsanalyse geben

STRUKTUR:
1. Ausgangsdaten
2. Analyse
3. Anatomie
4. Pathophysiologie
5. Physik
6. Geräteanalyse
7. Richtungsanalyse
8. Hypothesen
9. Limitationen

DATEN:
{full_input}
"""

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-5.3",
            "messages": [{"role": "user", "content": prompt}]
        }
    )

    result = response.json()
    return {"result": result["choices"][0]["message"]["content"]}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
