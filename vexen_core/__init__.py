"""
VexenCore - Integration layer for Vexen systems.

This package provides a unified container for managing:
- vexen-user: User management
- vexen-rbac: Role-based access control
- vexen-auth: Authentication

All systems share the same database session for transactional consistency.

Example:
	>>> from vexen_core import VexenContainer, VexenConfig
	>>>
	>>> config = VexenConfig(
	...     database_url="postgresql+asyncpg://user:pass@localhost/db",
	...     secret_key="your-secret-key"
	... )
	>>>
	>>> async with VexenContainer(config) as vexen:
	...     # Create user
	...     user = await vexen.user.create(...)
	...
	...     # Login
	...     auth = await vexen.auth.login(...)
	...
	...     # All in one transaction
	...     await vexen.commit()
"""

from .config import VexenConfig
from .container import VexenContainer

__version__ = "0.1.0"

__all__ = [
	"VexenContainer",
	"VexenConfig",
]
