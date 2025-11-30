"""
Basic usage example for VexenCore.

This example shows how to use the VexenContainer to integrate
all Vexen systems (user, rbac, auth) with shared resources.
"""

import asyncio

from vexen_core import VexenConfig, VexenContainer


async def main():
	"""Basic usage example"""

	# 1. Create configuration
	config = VexenConfig(
		database_url="postgresql+asyncpg://user:password@localhost:5432/vexen",
		secret_key="your-secret-key-change-in-production",
		algorithm="HS256",
		echo=False,  # Set to True to see SQL queries
	)

	# 2. Use VexenContainer with context manager (recommended)
	async with VexenContainer(config) as vexen:
		print("VexenContainer initialized successfully!")
		print(f"- User system: {vexen.user}")
		print(f"- RBAC system: {vexen.rbac}")
		print(f"- Auth system: {vexen.auth}")

		# All systems are ready to use

		# Example operations (uncomment when you have a database):

		# # 3. Create a user
		# from vexen_user.application.dto import CreateUserRequest
		# user_request = CreateUserRequest(
		#     email="john@example.com",
		#     name="John Doe",
		# )
		# user_response = await vexen.user.service.create(user_request)
		#
		# if user_response.success:
		#     print(f"User created: {user_response.data.id}")
		# else:
		#     print(f"Error: {user_response.error}")
		#     return

		# # 4. Create a role in RBAC
		# from vexen_rbac.application.dto import CreateRoleRequest
		# role_request = CreateRoleRequest(
		#     name="admin",
		#     description="Administrator role"
		# )
		# role_response = await vexen.rbac.roles.create(role_request)
		# if role_response.success:
		#     print(f"Role created: {role_response.data.name}")

		# # 5. Register user credentials for authentication
		# from vexen_auth.application.dto import RegisterRequest
		# register_request = RegisterRequest(
		#     email="john@example.com",
		#     password="SecurePassword123",
		#     user_id=user_response.data.id
		# )
		# await vexen.auth.service.register(register_request)

		# # 6. Login with Auth
		# from vexen_auth.application.dto import LoginRequest
		# login_request = LoginRequest(
		#     email="john@example.com",
		#     password="SecurePassword123"
		# )
		# login_response = await vexen.auth.service.login(login_request)
		#
		# if login_response:
		#     print(f"Login successful!")
		#     print(f"Access token: {login_response.access_token[:50]}...")
		#     print(f"User ID: {login_response.user_id}")

		print("\nAll systems initialized and ready!")

	print("VexenContainer closed.")


async def manual_lifecycle_example():
	"""Example with manual lifecycle management"""

	config = VexenConfig(
		database_url="postgresql+asyncpg://user:password@localhost:5432/vexen",
		secret_key="your-secret-key",
	)

	# Manual initialization
	vexen = VexenContainer(config)
	await vexen.init()

	try:
		# Use the systems
		# users = await vexen.user.service.list()
		# roles = await vexen.rbac.roles.list()
		print("Systems ready to use")

	except Exception as e:
		print(f"Error occurred: {e}")
		raise

	finally:
		# Always close
		await vexen.close()


async def auth_integration_example():
	"""Example showing authentication with user integration"""

	config = VexenConfig(
		database_url="postgresql+asyncpg://user:password@localhost:5432/vexen",
		secret_key="your-secret-key",
	)

	async with VexenContainer(config) as vexen:
		# The auth system is automatically configured to work with the user repository
		# This means it can validate users and retrieve user information

		# Example workflow:
		# 1. Create user
		# 2. Register credentials
		# 3. Login
		# 4. Use token for authentication

		print(f"Auth system integrated: {vexen.auth}")
		print(f"User repository available: {vexen.user.repository}")
		print("Ready to handle authentication operations")


if __name__ == "__main__":
	print("=" * 60)
	print("VexenCore - Basic Usage Example")
	print("=" * 60)
	print()

	asyncio.run(main())
