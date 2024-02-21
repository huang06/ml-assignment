from __future__ import annotations

import logging
import os

from fastapi import FastAPI
from pydantic import BaseModel
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

LOGLEVEL = os.environ.get("LOGLEVEL", "INFO")
log = logging.getLogger(__name__)
log.setLevel(LOGLEVEL)


class Record(BaseModel):
    id: str
    text: str


class TranslationPayload(BaseModel):
    fromLang: str
    records: list[Record]
    toLang: str


class RequestModel(BaseModel):
    payload: TranslationPayload


LLM_DIR = os.environ["LLM_DIR"]
model = M2M100ForConditionalGeneration.from_pretrained(LLM_DIR)
tokenizer = M2M100Tokenizer.from_pretrained(LLM_DIR)

app = FastAPI()


@app.post("/translation")
async def translation(request_model: RequestModel) -> dict:
    payload = request_model.payload
    tokenizer.src_lang = payload.fromLang
    result = []
    for record in payload.records:
        model_inputs = tokenizer(record.text, return_tensors="pt")
        generated_tokens = model.generate(**model_inputs, forced_bos_token_id=tokenizer.get_lang_id(payload.toLang))
        resp = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
        log.warning("%s, %s", record.text, resp)
        result.append({"id": record.id, "text": resp})
    return {"result": result}
