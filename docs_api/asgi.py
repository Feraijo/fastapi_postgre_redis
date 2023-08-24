import uvicorn
from fastapi import FastAPI
from docs_app.core.config import settings
from docs_app.routers.docs_router import router

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("asgi:app", host=settings.PRJ_HOST, port=settings.PRJ_PORT,
                log_level=settings.LOG_LEVEL, reload=True)
