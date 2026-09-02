from fastapi import FastAPI

app = FastAPI(
    title="ResiliNet Backend",
    description="Backend API for ResiliNet",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "resilinet-backend"
    }