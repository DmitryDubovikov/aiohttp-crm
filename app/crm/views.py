import uuid
from app.web.app import View
from app.web.utils import json_response
from aiohttp.web_exceptions import HTTPNotFound
from app.crm.models import User
from aiohttp_apispec import docs, request_schema, querystring_schema, response_schema
from app.crm.schemas import (
    UserAddSchema,
    UserGetRequestSchema,
    ListUsersResponseSchema,
    UserGetResponseSchema,
)
from app.web.schemas import OkResponseSchema


class AddUserView(View):
    @docs(tags=["crm"], summary="Add new user", description="Add new user to database")
    @request_schema(UserAddSchema)
    @response_schema(OkResponseSchema, 200)
    async def post(self):
        # data = await self.request.json()
        data = self.request["data"]  # data was already  retrieved during validation
        user = User(email=data["email"], id_=uuid.uuid4())
        await self.request.app.crm_accessor.add_user(user)
        return json_response()


class ListUsersView(View):
    @docs(
        tags=["crm"],
        summary="List all users",
        description="List all users from database",
    )
    @response_schema(ListUsersResponseSchema, 200)
    async def get(self):
        users = await self.request.app.crm_accessor.list_users()
        raw_users = [{"email": user.email, "id_": str(user.id_)} for user in users]
        return json_response(data={"users": raw_users})


class GetUserView(View):
    @docs(tags=["crm"], summary="Get user", description="Get user from database")
    @querystring_schema(UserGetRequestSchema)
    @response_schema(UserGetResponseSchema, 200)
    async def get(self):
        user_id = self.request.query["id"]
        user = await self.request.app.crm_accessor.get_user(uuid.UUID(user_id))
        if user:
            return json_response(
                data={
                    "user": {"email": user.email, "id_": str(user.id_)},
                }
            )
        else:
            raise HTTPNotFound
