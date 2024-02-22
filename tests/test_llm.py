from __future__ import annotations

import os
from pathlib import Path

from optimum.onnxruntime import ORTModelForSeq2SeqLM
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

here = Path(__file__).resolve().parent


def test_m2m100():
    LLM_DIR = str(here / "../artifacts/m2m100_418M")
    model = M2M100ForConditionalGeneration.from_pretrained(LLM_DIR, local_files_only=True)
    tokenizer = M2M100Tokenizer.from_pretrained(LLM_DIR, local_files_only=True)
    tokenizer.src_lang = "en"
    batch = ["Life is like a box of chocolates."]
    model_inputs = tokenizer(batch, return_tensors="pt")
    generated_tokens = model.generate(**model_inputs, forced_bos_token_id=tokenizer.get_lang_id("ja"))
    outputs = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
    assert outputs == ["人生はチョコレートの箱のようなものだ。"]


# def test_m2m100_onnx():
#     LLM_DIR = str(here / "../artifacts/m2m100_418M_onnx")
#     model = ORTModelForSeq2SeqLM.from_pretrained(LLM_DIR, local_files_only=True, use_cache=False)
#     tokenizer = M2M100Tokenizer.from_pretrained(LLM_DIR, local_files_only=True)
#     tokenizer.src_lang = "en"
#     batch = ["Life is like a box of chocolates."]
#     model_inputs = tokenizer(batch, return_tensors="pt")
#     generated_tokens = model.generate(**model_inputs, forced_bos_token_id=tokenizer.get_lang_id("ja"))
#     outputs = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
#     assert outputs == ["人生はチョコレートの箱のようなものだ。"]
