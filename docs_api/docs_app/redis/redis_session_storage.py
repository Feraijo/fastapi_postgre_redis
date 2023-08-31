import aioredis
from docs_app.core.config import settings
from uuid import uuid4
import json

def genSessionId() -> str:
    return uuid4().hex

class SessionStorage:
    def __init__(self):
        self.client = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
                                        decode_responses=True)

    async def write_session(self, token):
        sessionId = genSessionId()
        await self.client.set(sessionId, json.dumps(token))
        return sessionId
    
    async def read_session(self, sessionId):
        q = await self.client.get(sessionId)
        r = json.loads(q)
        return r['access_token']
