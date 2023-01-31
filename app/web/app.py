from aiohttp.web import (
    Application as AiohttpApplication,
    run_app as aiohttp_run_app,
    View as AiohttpView,
    Request as AiohttpRequest,
)
from app.web.routes import setup_routes


class Application(AiohttpApplication):
    database: dict = {}


class Request(AiohttpRequest):
    @property
    def app(self) -> "Application":
        return super().app


class View(AiohttpView):
    @property
    def request(self) -> Request:
        return super().request


app = Application()


def run_app():
    setup_routes(app)
    aiohttp_run_app(app)
