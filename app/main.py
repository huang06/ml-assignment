from __future__ import annotations

from fastapi import FastAPI

app = FastAPI()


@app.post("/translation")
def translation(text: str, source_language: str, target_language: str) -> dict:
    return {"result": "人生はチョコレートの箱のようなものだ。"}
