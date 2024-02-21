from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_translation():
    data = {
        "payload": {
            "fromLang": "en",
            "records": [
                {
                    "id": "123",
                    "text": "Life is like a box of chocolates.",
                },
                {
                    "id": "456",
                    "text": "Life is like a box of chocolates.",
                },
            ],
            "toLang": "ja",
        }
    }

    resp = {
        "result": [
            {
                "id": "123",
                "text": "人生はチョコレートの箱のようなものだ。",
            },
            {
                "id": "456",
                "text": "人生はチョコレートの箱のようなものだ。",
            },
        ]
    }

    response = client.post("/translation", json=data)
    assert response.status_code == 200
    assert response.json() == resp
