from fastapi import FastAPI

from src.backend.core.config import settings
from src.backend.routes.analyze_route import router as analyze_router
from src.backend.routes.health_route import router as health_router
from src.backend.routes.root_router import router as root


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.VERSION,
        description="AI-powered API for matching resumes to job descriptions — extracts hard and soft skills, scores semantic similarity, and identifies skill gaps.",
    )

    app.include_router(analyze_router)
    app.include_router(health_router)
    app.include_router(root)

    return app


app = create_app()
