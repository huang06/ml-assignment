from __future__ import annotations

import argparse
import asyncio
import json
import time

from aiohttp import ClientSession

parser = argparse.ArgumentParser()
parser.add_argument("--model")
parser.add_argument("--preheat", action="store_true")
args = parser.parse_args()

if args.model == "torch":
    link = "http://127.0.0.1:9527/translation_torch"
elif args.model == "onnx":
    link = "http://127.0.0.1:9527/translation_onnx"
else:
    raise


async def post(session, batch):
    json_data = {
        "payload": {
            "fromLang": "en",
            "records": [{"id": "123", "text": "Life is like a box of chocolates."}] * batch,
            "toLang": "ja",
        }
    }
    t1 = time.time()
    async with session.post(link, json=json_data) as resp:
        _ = await resp.json()
    return batch, time.time() - t1


async def main():
    for b in range(1, 11):
        print(b)
        async with ClientSession() as session:
            tasks = [post(session, b)]
            time_list = await asyncio.gather(*tasks)
        if not args.preheat:
            with open("./records.txt", "a") as fp:
                for b, t in time_list:
                    fp.write(json.dumps({"model": args.model, "batch_size": b, "time": t}) + "\n")


asyncio.run(main())
