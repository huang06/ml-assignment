from __future__ import annotations

from fastapi import FastAPI

app = FastAPI()


@app.post("/translation")
def translation(src_text: str, target_lang: str) -> dict:
    return {"result": "The target."}
