#!/bin/python

import trio_asyncio
from hypercorn.config import Config
from hypercorn.trio import serve

from application import app

if __name__ == "__main__":
    trio_asyncio.run(serve, app, Config.from_toml("application.toml"))
