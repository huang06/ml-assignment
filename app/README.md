# Demo

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

```bash
export LLM_DIR="${PWD}/artifacts/models--facebook--m2m100_418M/snapshots/62d980b8566a7c30e96918baf450d6a7218aadec/"
uvicorn app.main:app --host 0.0.0.0 --port 9527
```
