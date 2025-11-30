"""Tests for VexenContainer integration."""

import pytest

from vexen_core import VexenConfig, VexenContainer


@pytest.mark.asyncio
async def test_container_initialization():
	"""Test that container initializes all systems."""
	config = VexenConfig(
		database_url="postgresql+asyncpg://user:pass@localhost/test_db",
		secret_key="test-secret-key",
	)

	container = VexenContainer(config)

	# Should not raise error
	assert container.config == config


@pytest.mark.asyncio
async def test_container_properties_before_init():
	"""Test that accessing properties before init raises error."""
	config = VexenConfig(
		database_url="postgresql+asyncpg://user:pass@localhost/test_db",
		secret_key="test-secret-key",
	)

	container = VexenContainer(config)

	# Should raise RuntimeError
	with pytest.raises(RuntimeError, match="not initialized"):
		_ = container.user

	with pytest.raises(RuntimeError, match="not initialized"):
		_ = container.rbac

	with pytest.raises(RuntimeError, match="not initialized"):
		_ = container.auth


@pytest.mark.asyncio
async def test_container_context_manager():
	"""Test container as context manager (requires database)."""
	# This test requires a real database connection
	# Skip if no database available
	pytest.skip("Requires database connection")

	config = VexenConfig(
		database_url="postgresql+asyncpg://user:pass@localhost/test_db",
		secret_key="test-secret-key",
	)

	async with VexenContainer(config) as vexen:
		# Should be able to access systems
		assert vexen.user is not None
		assert vexen.rbac is not None
		assert vexen.auth is not None


@pytest.mark.asyncio
async def test_container_manual_lifecycle():
	"""Test manual initialization and cleanup (requires database)."""
	# This test requires a real database connection
	# Skip if no database available
	pytest.skip("Requires database connection")

	config = VexenConfig(
		database_url="postgresql+asyncpg://user:pass@localhost/test_db",
		secret_key="test-secret-key",
	)

	vexen = VexenContainer(config)

	try:
		await vexen.init()
		assert vexen.user is not None
		assert vexen.rbac is not None
		assert vexen.auth is not None
	finally:
		await vexen.close()
