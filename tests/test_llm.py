from __future__ import annotations

import os

from optimum.onnxruntime import ORTModelForSeq2SeqLM
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer


def test_m2m100_torch():
    LLM_DIR = os.environ["LLM_DIR"]
    model = M2M100ForConditionalGeneration.from_pretrained(LLM_DIR, local_files_only=True)
    tokenizer = M2M100Tokenizer.from_pretrained(LLM_DIR, local_files_only=True)
    tokenizer.src_lang = "en"
    batch = ["Life is like a box of chocolates."] * 10
    model_inputs = tokenizer(batch, return_tensors="pt")
    generated_tokens = model.generate(**model_inputs, forced_bos_token_id=tokenizer.get_lang_id("ja"))
    outputs = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
    assert outputs == ["人生はチョコレートの箱のようなものだ。"] * 10


def test_m2m100_onnx():
    ONNX_DIR = os.environ["ONNX_DIR"]
    model = ORTModelForSeq2SeqLM.from_pretrained(ONNX_DIR, local_files_only=True)
    tokenizer = M2M100Tokenizer.from_pretrained(ONNX_DIR, local_files_only=True)
    tokenizer.src_lang = "en"
    batch = ["Life is like a box of chocolates."] * 10
    model_inputs = tokenizer(batch, return_tensors="pt")
    generated_tokens = model.generate(**model_inputs, forced_bos_token_id=tokenizer.get_lang_id("ja"))
    outputs = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
    assert outputs == ["人生はチョコレートの箱のようなものだ。"] * 10
