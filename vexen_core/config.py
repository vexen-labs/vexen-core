"""Configuration for VexenCore."""

from dataclasses import dataclass


@dataclass
class VexenConfig:
	"""
	Unified configuration for all Vexen systems.

	Attributes:
		database_url: PostgreSQL connection URL
		secret_key: Secret key for JWT signing
		algorithm: JWT algorithm (default: HS256)
		echo: Echo SQL queries (default: False)
		pool_size: Database connection pool size (default: 5)
		max_overflow: Max overflow connections (default: 10)
		access_token_expires_minutes: Access token TTL (default: 15)
		refresh_token_expires_days: Refresh token TTL (default: 30)
	"""

	# Database
	database_url: str

	# Security
	secret_key: str
	algorithm: str = "HS256"

	# Database pool
	echo: bool = False
	pool_size: int = 5
	max_overflow: int = 10

	# Token expiration
	access_token_expires_minutes: int = 15
	refresh_token_expires_days: int = 30
