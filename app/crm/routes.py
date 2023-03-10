import typing


if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_routes(app: "Application"):
    from app.crm.views import AddUserView, ListUsersView, GetUserView

    app.router.add_view("/add-user", AddUserView)
    app.router.add_view("/list-users", ListUsersView)
    app.router.add_view("/get-user", GetUserView)
