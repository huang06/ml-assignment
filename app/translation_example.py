from __future__ import annotations

import os
from pathlib import Path

from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

here = Path(__file__).resolve().parent
LLM_DIR = os.environ.get("LLM_DIR") or str(
    here / "../artifacts/models--facebook--m2m100_418M/snapshots/62d980b8566a7c30e96918baf450d6a7218aadec"
)
model = M2M100ForConditionalGeneration.from_pretrained(LLM_DIR)  # ("facebook/m2m100_418M")
tokenizer = M2M100Tokenizer.from_pretrained(
    LLM_DIR, src_lang="en", tgt_lang="fr"
)  # ("facebook/m2m100_418M", src_lang="en", tgt_lang="fr")


if __name__ == "__main__":

    src_text = "Life is like a box of chocolates."
    tgt_lang = "人生はチョコレートの箱のようなものだ。"

    tokenizer.src_lang = "en"
    tokenizer.tgt_lang = "ja"
    model_inputs = tokenizer(src_text, return_tensors="pt")
    generated_tokens = model.generate(**model_inputs, forced_bos_token_id=tokenizer.get_lang_id("ja"))
    result = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)

    print(result[0])
    print(result)
