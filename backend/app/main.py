from fastapi import FastAPI

from app.routes import (
    roads,
    vehicles,
    incidents,
    risk,
    accessibility,
    routes,
    scenarios,
    verification,
    weather,
    sync,
)


app = FastAPI(
    title="ResiliNet Backend",
    description="Backend API for ResiliNet",
    version="1.0.0",
)


app.include_router(roads.router)
app.include_router(vehicles.router)
app.include_router(incidents.router)
app.include_router(risk.router)
app.include_router(accessibility.router)
app.include_router(routes.router)
app.include_router(scenarios.router)
app.include_router(verification.router)
app.include_router(weather.router)
app.include_router(sync.router)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "resilinet-backend"
    }