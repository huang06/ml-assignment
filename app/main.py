from __future__ import annotations

import logging
import os

from fastapi import FastAPI
from optimum.onnxruntime import ORTModelForSeq2SeqLM
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
ONNX_DIR = os.environ["ONNX_DIR"]
torch_model = M2M100ForConditionalGeneration.from_pretrained(LLM_DIR, local_files_only=True)
torch_tokenizer = M2M100Tokenizer.from_pretrained(LLM_DIR, local_files_only=True)
onnx_model = ORTModelForSeq2SeqLM.from_pretrained(ONNX_DIR, local_files_only=True)
onnx_tokenizer = M2M100Tokenizer.from_pretrained(ONNX_DIR, local_files_only=True)

app = FastAPI()


def inference(batch, model, tokenizer, src_lang, tgt_lang):
    tokenizer.src_lang = src_lang
    model_inputs = tokenizer(batch, return_tensors="pt")
    generated_texts = model.generate(**model_inputs, forced_bos_token_id=tokenizer.get_lang_id(tgt_lang))
    return tokenizer.batch_decode(generated_texts, skip_special_tokens=True)


@app.post("/translation_torch")
def translation_with_torch(request_model: RequestModel) -> dict:
    payload = request_model.payload
    batch = [record.text for record in payload.records]
    generated_texts = inference(batch, torch_model, torch_tokenizer, payload.fromLang, payload.toLang)
    return {"result": [{"id": record.id, "text": text} for record, text in zip(payload.records, generated_texts)]}


@app.post("/translation")
@app.post("/translation_onnx")
def translation_with_onnx(request_model: RequestModel) -> dict:
    payload = request_model.payload
    batch = [record.text for record in payload.records]
    generated_texts = inference(batch, onnx_model, onnx_tokenizer, payload.fromLang, payload.toLang)
    return {"result": [{"id": record.id, "text": text} for record, text in zip(payload.records, generated_texts)]}
