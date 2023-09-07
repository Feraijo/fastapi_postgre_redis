import uvicorn
from docs_app.api.api_router import api_router
from docs_app.core.config import settings
from fastapi import FastAPI

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(
        "asgi:app",
        host=settings.PRJ_HOST,
        port=settings.PRJ_PORT,
        log_level=settings.LOG_LEVEL,
        reload=True,
    )
