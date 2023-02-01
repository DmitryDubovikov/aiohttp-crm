from aiohttp.web import (
    Application as AiohttpApplication,
    run_app as aiohttp_run_app,
    View as AiohttpView,
    Request as AiohttpRequest,
)
from app.web.routes import setup_routes
from typing import Optional
from app.store.crm.accessor import CrmAccessor
from app.store import setup_accessors
from aiohttp_apispec import setup_aiohttp_apispec
from app.web.middlewares import setup_middlewares
from app.web.config import Config, setup_config


class Application(AiohttpApplication):
    config: Optional[Config] = None
    database: dict = {}
    crm_accessor: Optional[CrmAccessor] = None


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

    # read and setup config from yaml
    setup_config(app)

    # connect urls to views
    setup_routes(app)

    # validation and swagger docs
    setup_aiohttp_apispec(
        app, title="CRM Application", url="/docs/json", swagger_path="/docs"
    )

    # middlewares for error handling and validation
    setup_middlewares(app)

    # to work with DB
    setup_accessors(app)

    # run app
    aiohttp_run_app(app)
