from __future__ import annotations

import argparse
import asyncio

from aiohttp import ClientSession

parser = argparse.ArgumentParser()
parser.add_argument("--model")
parser.add_argument("--n-records", type=int, default=1)
parser.add_argument("--n-requests", type=int, default=1)
args = parser.parse_args()

if args.model == "torch":
    link = "http://127.0.0.1:9527/translation_torch"
elif args.model == "onnx":
    link = "http://127.0.0.1:9527/translation_onnx"
else:
    raise


async def post(session, n):
    json_data = {
        "payload": {
            "fromLang": "en",
            "records": [{"id": "123", "text": "Life is like a box of chocolates."}] * args.n_records,
            "toLang": "ja",
        }
    }
    async with session.post(link, json=json_data) as resp:
        resp_json = await resp.json()
        print(f"{n=} {resp_json}")


async def main():
    headers = {"x-nd-token": "test"}
    async with ClientSession(headers=headers) as session:
        tasks = [post(session, n) for n in range(args.n_requests)]
        await asyncio.gather(*tasks)


asyncio.run(main())
