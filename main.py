import asyncio

from vexen_user.application.dto.user_dto import CreateUserRequest

from vexen_core import VexenConfig, VexenContainer

config = VexenConfig(
	database_url="sqlite+aiosqlite:///vexen_tests.db",
	secret_key="capo",
	echo=True,
	algorithm="SHA256",
)

container = VexenContainer(config)


async def main():
	await container.init()
	user: CreateUserRequest = CreateUserRequest(
		name="capo",
		email="",
		password="capo1234",
	)
	response = await container.user.service.create(user)
	print(response)


if __name__ == "__main__":
	asyncio.run(main())
