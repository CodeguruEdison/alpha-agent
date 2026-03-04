from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "alpha-agent API"}


@app.get("/health")
def health():
    return {"status": "ok"}


def run():
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
