from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/ask")
def ask(prompt: str):
    res = requests.post(
        "http://127.0.0.1:11434/api/generate",
        json={"model": "llama3.2:3b", "prompt": prompt, "stream": False}
    )
    data = res.json()
    return {"response": data.get("response", "no reply")}
