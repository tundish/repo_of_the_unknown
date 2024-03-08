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
import functools
import os
import pathlib
import sqlite3
import sys
import tempfile
import textwrap
from types import SimpleNamespace
import unittest

import aiosqlite
import asgi_lifespan
import httpx
import hypercorn
from hypercorn.asyncio import serve
from starlette.applications import Starlette
from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse
from starlette.responses import PlainTextResponse
from starlette.routing import Route

import rotu

# Example lifespan-capable ASGI app. Any ASGI app that supports
# the lifespan protocol will do, e.g. FastAPI, Quart, Responder, ...

sql = SimpleNamespace(
    create=textwrap.dedent("""
        CREATE TABLE {db}.witness (
        name TEXT NOT NULL
        )
        """),
    insert="INSERT INTO {db}.witness ( name ) VALUES ( ? )",
    select="SELECT ( name ) FROM {db}.witness",
)

class DBAdaptor:

    @staticmethod
    def dsn(parent: pathlib.Path, database: str = "main", suffix: str = ".db"):
        return parent.joinpath(database).with_suffix(suffix).expanduser().as_uri()

    def get_connector(dsn, loop=None):
        return aiosqlite.connect(
            dsn,
            detect_types=sqlite3.PARSE_COLNAMES | sqlite3.PARSE_DECLTYPES,
            uri=True,
            loop=loop
        )

    def get_connector(dsn, loop=None):
        return functools.partial(
            aiosqlite.connect,
            dsn,
            detect_types=sqlite3.PARSE_COLNAMES | sqlite3.PARSE_DECLTYPES,
            uri=True,
            loop=loop
        )

# TODO: ATTACH DATABASE '{db_file_path!s}' AS {db_file_path.name}

@contextlib.asynccontextmanager
async def lifespan(app):
    print("Starting up!")
    yield
    print("Shutting down!")

class Root(HTTPEndpoint):
    async def get(self, request):
        text = f"RotU {rotu.__version__}\n"
        return PlainTextResponse(text)

    async def post(self, request):
        body = await request.json()
        try:
            name = body["name"]
            print(f"{request.app.state.connector=}", file=sys.stderr)
            async with request.app.state.connector() as connection:
                await connection.execute(sql.insert.format(db="main"), (name,))
            return JSONResponse({"name": name})

        except KeyError:
            return HTTPException(404, detail="Parameter not recognised", headers=None)

routes = [
    Route("/", Root, name="info"),
    Route("/", Root, methods=["POST"], name="register"),
]

def build_app():
    return Starlette(routes=routes)
#app = Starlette(lifespan=lifespan)

async def main():
    async with asgi_lifespan.LifespanManager(app) as manager:
        print("We're in!")

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
        print("setUp", file=sys.stderr)
        self.temp_fd, temp_db = tempfile.mkstemp(suffix="_tmp.db", dir=pathlib.Path.cwd())
        self.temp_db = pathlib.Path(temp_db)
        self.dsn = DBAdaptor.dsn(self.temp_db.parent, self.temp_db.name, self.temp_db.suffix)
        self.db_connector = DBAdaptor.get_connector(self.dsn)

    async def create_db_fixture(self, connection):
        await connection.execute(sql.create.format(db="main"))
        cursor = await connection.execute(sql.select.format(db="main"))
        rows = await cursor.fetchall()
        return rows

    async def asyncSetUp(self):
        self._async_connection = AsyncConnection()
        print("asyncSetUp", file=sys.stderr)

    async def test_endpoint_get(self):
        print(self.id(), file=sys.stderr)

        async with self.db_connector() as connection:
            rows = await self.create_db_fixture(connection)

        app = build_app()
        app.state.connector = self.db_connector

        transport = httpx.ASGITransport(app=app)
        async with asgi_lifespan.LifespanManager(app) as manager:
            async with httpx.AsyncClient(base_url="http://localhost", transport=transport) as client:
                response = await client.get("/")

        # response = await self._async_connection.get("https://localhost")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.text.startswith("RotU"), response.text)

    async def test_endpoint_post(self):
        print(self.id(), file=sys.stderr)

        async with self.db_connector() as connection:
            rows = await self.create_db_fixture(connection)

        print(f"rows=", file=sys.stderr)

        app = build_app()
        app.state.connector = self.db_connector

        transport = httpx.ASGITransport(app=app)
        async with asgi_lifespan.LifespanManager(app) as manager:
            async with httpx.AsyncClient(base_url="http://localhost", transport=transport) as client:
                response = await client.post("/", json={"name": self.id()})

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data.get("name", "").endswith("test_endpoint_post") , data)
        self.addAsyncCleanup(self.on_cleanup)

    def tearDown(self):
        print("tearDown", file=sys.stderr)
        os.close(self.temp_fd)
        self.temp_db.unlink()

    async def asyncTearDown(self):
        await self._async_connection.close()
        print("asyncTearDown", file=sys.stderr)

    async def on_cleanup(self):
        print("cleanup", file=sys.stderr)


if __name__ == "__main__":

    # asyncio.run(main())
    unittest.main()
    host="localhost"
    port=8080
    settings = hypercorn.Config.from_mapping({"bind": f"{host}:{port}", "errorlog": "-"})

    # asyncio.run(serve(app, settings))
