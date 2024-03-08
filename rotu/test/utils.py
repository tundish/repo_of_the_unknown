#!/usr/bin/env python
# encoding: utf8

# Copyright 2024 D E Haynes

# This file is part of rotu.
#
# Rotu is free software: you can redistribute it and/or modify it under the terms of the
# GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.
#
# Rotu is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License along with Rotu.
# If not, see <https://www.gnu.org/licenses/>.

import asyncio
import contextlib
import sqlite3
from types import SimpleNamespace
import unittest

import aiosqlite
import asgi_lifespan
import httpx
import hypercorn
from hypercorn.asyncio import serve
from starlette.applications import Starlette
from starlette.endpoints import HTTPEndpoint
from starlette.responses import PlainTextResponse
from starlette.routing import Route

import rotu

# Example lifespan-capable ASGI app. Any ASGI app that supports
# the lifespan protocol will do, e.g. FastAPI, Quart, Responder, ...

@contextlib.asynccontextmanager
async def lifespan(app):
    print("Starting up!")
    yield
    print("Shutting down!")

class Root(HTTPEndpoint):
    async def get(self, request):
        text = f"RotU {rotu.__version__}\n"
        return PlainTextResponse(text)

routes = [
    Route("/", Root, name="root"),
]
app = Starlette(routes=routes)
#app = Starlette(lifespan=lifespan)

async def main():
    async with asgi_lifespan.LifespanManager(app) as manager:
        print("We're in!")

events = []

class AsyncConnection:

    async def __await__(self):
        await asyncio.sleep(0.5)
        return self

    async def get(self, url):
        await asyncio.sleep(0.5)
        return SimpleNamespace(
            status_code=200,
        )

    async def close(self):
        return self


class LifecycleTests(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        events.append("setUp")

    async def asyncSetUp(self):
        self._async_connection = AsyncConnection()
        events.append("asyncSetUp")

    async def test_response(self):
        events.append("test_response")

        transport = httpx.ASGITransport(app=app)
        async with asgi_lifespan.LifespanManager(app) as manager:
            async with httpx.AsyncClient(base_url="http://localhost", transport=transport) as client:
                response = await client.get("/")
                print(response.text)

        # response = await self._async_connection.get("https://localhost")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.text.startswith("RotU"), response.text)
        self.addAsyncCleanup(self.on_cleanup)

    def tearDown(self):
        events.append("tearDown")

    async def asyncTearDown(self):
        await self._async_connection.close()
        events.append("asyncTearDown")

    async def on_cleanup(self):
        events.append("cleanup")
        print(*events, sep="\n")


if __name__ == "__main__":

    # asyncio.run(main())
    unittest.main()
    host="localhost"
    port=8080
    settings = hypercorn.Config.from_mapping({"bind": f"{host}:{port}", "errorlog": "-"})

    # asyncio.run(serve(app, settings))
