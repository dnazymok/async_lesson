import aiohttp

from .models import User, CreateUserParams


class UserRepository:
    def __init__(self):
        self._users = [
            User(
                id=1,
                username="John",
                email="john@email.com"
            ),
            User(
                id=2,
                username="Jane",
                email="jane@email.com"
            )
        ]
        self._serial = len(self._users)

    async def list_users(self) -> list[User]:
        return self._users.copy()

    async def create_user(self, params: CreateUserParams) -> User:
        user = User(
            id=self._serial,
            **params.dict()
        )
        self._serial += 1
        self._users.append(user)
        return user


class JSONPlaceholderUserRepository(UserRepository):
    def __init__(self):
        self._endpoint = "https://jsonplaceholder.typicode.com/users"

    async def list_users(self) -> list[User]:
        raw_users = await self._list_users()
        return [self._convert_user(raw_users) for raw_user in raw_users]

    async def create_user(self, params: CreateUserParams) -> User:
        raw_user = await self._create_user(params)
        return self._convert_user(raw_user)

    async def _create_user(self, params):
        async with aiohttp.ClientSession() as session:
            resp = await session.post(self._endpoint, json=params.dict())
            raw_user = await resp.json()
            return raw_user

    async def _list_users(self):
        async with aiohttp.ClientSession as session:
            resp = await session.get(self._endpoint)
            raw_users = await resp.json()
            return raw_users

    def _convert_user(self, raw_user):
        return User(**raw_user)


class UserRepositoryFactory:
    def __init__(self):
        self._repo = None

    def __call__(self):
        if self._repo is None:
            self._repo = JSONPlaceholderUserRepository()
        return self._repo


get_user_repository = UserRepositoryFactory()
