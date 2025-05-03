from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import os

from fastapi import FastAPI, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def home():
    with open("templates/index.html") as f:
        return HTMLResponse(f.read())


@app.get("/login")
async def login():
    return {"author": "1147332"}


@app.post("/decypher")
async def decrypt_files(key: UploadFile, secret: UploadFile):
    try:
        private_key = serialization.load_pem_private_key(
            await key.read(),
            password=None,
        )

        decrypted = private_key.decrypt(
            await secret.read(),
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                         algorithm=hashes.SHA256(),
                         label=None))

        return {"result": decrypted.decode('utf-8')}
    except Exception as e:
        raise HTTPException(400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
