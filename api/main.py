from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes.image_route import router as image_router
from api.routes.clinical_route import router as clinical_router
from database.models import init_db

init_db()

app = FastAPI(
    title="Malaria Detection API",
    version="1.0.0",
    description="API de détection du paludisme — Bénin"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    image_router,
    prefix="/api/v1/image",
    tags=["Imagerie"]
)
app.include_router(
    clinical_router,
    prefix="/api/v1/clinical",
    tags=["Clinique"]
)

@app.get("/health")
def health_check():
    return {"status": "ok", "version": "1.0.0"}