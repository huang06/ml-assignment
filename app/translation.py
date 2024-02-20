import os

LLM_DIR = os.environ["LLM_DIR"]


class Translator:
    model = M2M100ForConditionalGeneration.from_pretrained(LLM_DIR)
    tokenizer = M2M100Tokenizer.from_pretrained(LLM_DIR)

    def translate(self, text, src_lang, tgt_lang):
        tokenizer.src_lang = payload.fromLang
        result = []
        for record in payload.records:
            model_inputs = tokenizer(record.text, return_tensors="pt")
            generated_tokens = model.generate(**model_inputs, forced_bos_token_id=tokenizer.get_lang_id(payload.toLang))
            resp_list = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
            result.append({"id": record.id, "text": resp_list[0]})
        print(result)
        return {"result": result}
