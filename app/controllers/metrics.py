from blacksheep.server.controllers import Controller, get, post, put
from sqlalchemy import text

from ..database import SessionMaker
from ..responses import json


class Metrics(Controller):
    @get("/metrics")
    async def index(self, session_maker: SessionMaker):
        async with session_maker() as session:
            result = await session.execute(text("SELECT @@VERSION"))
            print(result)

        return await self.view_async("create")

    @post("/metrics")
    async def create(self):
        return await self.view_async("_update", slug="hello", value=0.01)

    @get("/metrics/{slug}")
    async def read(self, slug: str):
        if slug == "banana":
            return json({""})

    @put("/metrics/{slug}")
    async def update(self, slug: str):
        return await self.view_async("_update")
