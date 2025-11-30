"""
VexenContainer - Manual Dependency Injection Container.

This container manages the lifecycle and dependencies of all Vexen systems:
- vexen-user: User management
- vexen-rbac: Role-based access control
- vexen-auth: Authentication
"""

from vexen_auth import AuthConfig, VexenAuth
from vexen_rbac import RBAC, RBACConfig
from vexen_user import VexenUser, VexenUserConfig

from .config import VexenConfig


class VexenContainer:
	"""
	Manual DI container for all Vexen systems.

	Integrates vexen-user, vexen-rbac, and vexen-auth into a unified interface.

	Example:
		>>> config = VexenConfig(
		...     database_url="postgresql+asyncpg://user:pass@localhost/db",
		...     secret_key="your-secret-key"
		... )
		>>>
		>>> async with VexenContainer(config) as vexen:
		...     # Use the integrated services
		...     user = await vexen.user.service.create(...)
		...     role = await vexen.rbac.roles.create(...)
		...     auth_result = await vexen.auth.service.login(...)
	"""

	def __init__(self, config: VexenConfig):
		"""
		Initialize container with configuration.

		Args:
			config: VexenConfig instance
		"""
		self.config = config

		# System instances
		self._user_system: VexenUser | None = None
		self._rbac_system: RBAC | None = None
		self._auth_system: VexenAuth | None = None

	async def init(self):
		"""
		Initialize all Vexen systems.

		This method initializes:
		1. User management system (vexen-user)
		2. RBAC system (vexen-rbac)
		3. Authentication system (vexen-auth)
		"""
		# Initialize user system
		user_config = VexenUserConfig(
			database_url=self.config.database_url,
			echo=self.config.echo,
			pool_size=self.config.pool_size,
			max_overflow=self.config.max_overflow,
		)
		self._user_system = VexenUser(
			database_url=user_config.database_url,
			echo=user_config.echo,
			pool_size=user_config.pool_size,
			max_overflow=user_config.max_overflow,
		)
		await self._user_system.init()

		# Initialize RBAC system
		rbac_config = RBACConfig(
			database_url=self.config.database_url,
			echo=self.config.echo,
			pool_size=self.config.pool_size,
			max_overflow=self.config.max_overflow,
		)
		self._rbac_system = RBAC(config=rbac_config)
		await self._rbac_system.init()

		# Initialize auth system
		auth_config = AuthConfig(
			database_url=self.config.database_url,
			secret_key=self.config.secret_key,
			algorithm=self.config.algorithm,
			access_token_expires_minutes=self.config.access_token_expires_minutes,
			refresh_token_expires_days=self.config.refresh_token_expires_days,
			user_repository=self._user_system.repository,
		)
		self._auth_system = VexenAuth(auth_config)
		await self._auth_system.init()

	@property
	def user(self) -> VexenUser:
		"""
		Access the user management system.

		Returns:
			VexenUser: User system instance

		Raises:
			RuntimeError: If container not initialized
		"""
		if self._user_system is None:
			raise RuntimeError("VexenContainer not initialized. Call await init() first.")
		return self._user_system

	@property
	def rbac(self) -> RBAC:
		"""
		Access the RBAC system.

		Returns:
			RBAC: RBAC system instance

		Raises:
			RuntimeError: If container not initialized
		"""
		if self._rbac_system is None:
			raise RuntimeError("VexenContainer not initialized. Call await init() first.")
		return self._rbac_system

	@property
	def auth(self) -> VexenAuth:
		"""
		Access the authentication system.

		Returns:
			VexenAuth: Auth system instance

		Raises:
			RuntimeError: If container not initialized
		"""
		if self._auth_system is None:
			raise RuntimeError("VexenContainer not initialized. Call await init() first.")
		return self._auth_system

	async def close(self):
		"""Close all systems and cleanup resources."""
		if self._auth_system:
			await self._auth_system.close()
		if self._rbac_system:
			await self._rbac_system.close()
		if self._user_system:
			await self._user_system.close()

	async def __aenter__(self):
		"""Context manager entry - initializes all systems."""
		await self.init()
		return self

	async def __aexit__(self, exc_type, exc_val, exc_tb):
		"""
		Context manager exit - handles cleanup.

		Automatically closes all resources.
		"""
		await self.close()
