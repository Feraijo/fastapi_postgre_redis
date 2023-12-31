import os

import yaml
from pydantic_settings import BaseSettings

ENVIRONMENT = os.getenv("ENV_VAR", "local")
par_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
with open(
    os.path.join(os.path.dirname(par_dir), f"config/{ENVIRONMENT.lower()}.yml")
) as f:
    sett_dict = yaml.load(f, Loader=yaml.FullLoader)


class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_PASSWORD: str
    PROJECT_NAME: str
    PRJ_HOST: str
    PRJ_PORT: int

    LOG_LEVEL: str

    DB_SCHEMA: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    REDIS_HOST: str
    REDIS_PORT: int
    SESSION_EXPIRE: int
    SSID: str

    BLOCKED_EXTS: str

    @property
    def CONN_STRING(self) -> str:
        return "{drivername}://{user}:{password}@{server}:{port}/{database}".format(
            drivername="postgresql+asyncpg",
            user=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            server=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            database=self.POSTGRES_DB,
        )

    @property
    def BAD_EXTS(self) -> list:
        return [x for x in self.BLOCKED_EXTS.split(",")]


settings = Settings(**sett_dict)
