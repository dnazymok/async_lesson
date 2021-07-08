from fastapi import FastAPI

from apps import users


def create_app():
    app = FastAPI()
    app.include_router(users.router, prefix="/users")
    return app


app = create_app()
