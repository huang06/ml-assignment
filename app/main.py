from __future__ import annotations

import os

from fastapi import FastAPI
from pydantic import BaseModel
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer


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
tokenizer = M2M100Tokenizer.from_pretrained(LLM_DIR, src_lang="en", tgt_lang="fr")

app = FastAPI()


@app.post("/translation")
async def translation(request_model: RequestModel) -> dict:
    print(request_model)
    payload = request_model.payload
    tokenizer.src_lang = payload.fromLang
    result = []
    for record in payload.records:
        model_inputs = tokenizer(record.text, return_tensors="pt")
        generated_tokens = model.generate(**model_inputs, forced_bos_token_id=tokenizer.get_lang_id(payload.toLang))
        resp_list = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
        result.append({"id": record.id, "text": resp_list[0]})
    print(result)
    return {"result": result}
