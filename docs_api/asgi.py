import uvicorn
from fastapi import FastAPI
from docs_app.core.config import settings
from docs_app.api.api_v1.api import api_router

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    uvicorn.run("asgi:app", host=settings.PRJ_HOST, port=settings.PRJ_PORT,
                log_level=settings.LOG_LEVEL, reload=True)
