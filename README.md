# vexen-core

Integration layer for the Vexen system suite (user, rbac, auth).

## Overview

`vexen-core` provides a unified container that integrates three independent Vexen systems:

- **vexen-user**: User management with hexagonal architecture
- **vexen-rbac**: Role-Based Access Control system
- **vexen-auth**: Authentication with JWT tokens

## Installation

```bash
pip install vexen-core
```

This will automatically install all three systems as dependencies.

## Quick Start

```python
import asyncio
from vexen_core import VexenConfig, VexenContainer

async def main():
    # Create configuration
    config = VexenConfig(
        database_url="postgresql+asyncpg://user:pass@localhost/db",
        secret_key="your-secret-key-change-in-production",
        algorithm="HS256",
        echo=False
    )

    # Use context manager (recommended)
    async with VexenContainer(config) as vexen:
        # Access all three systems
        user_system = vexen.user
        rbac_system = vexen.rbac
        auth_system = vexen.auth

        # Use the services
        # users = await vexen.user.service.list()
        # roles = await vexen.rbac.roles.list()
        # auth_response = await vexen.auth.service.login(request)

if __name__ == "__main__":
    asyncio.run(main())
```

## Configuration

The `VexenConfig` dataclass accepts the following parameters:

```python
@dataclass
class VexenConfig:
    # Database configuration
    database_url: str
    echo: bool = False
    pool_size: int = 5
    max_overflow: int = 10

    # Authentication configuration
    secret_key: str
    algorithm: str = "HS256"
    access_token_expires_minutes: int = 15
    refresh_token_expires_days: int = 30
```

## Usage

### User Management

```python
from vexen_user.application.dto import CreateUserRequest

async with VexenContainer(config) as vexen:
    # Create a user
    request = CreateUserRequest(
        email="john@example.com",
        name="John Doe"
    )
    response = await vexen.user.service.create(request)

    if response.success:
        print(f"User created: {response.data.id}")
```

### RBAC

```python
from vexen_rbac.application.dto import CreateRoleRequest

async with VexenContainer(config) as vexen:
    # Create a role
    request = CreateRoleRequest(
        name="admin",
        description="Administrator role"
    )
    response = await vexen.rbac.roles.create(request)

    if response.success:
        print(f"Role created: {response.data.id}")
```

### Authentication

```python
from vexen_auth.application.dto import LoginRequest

async with VexenContainer(config) as vexen:
    # Login
    request = LoginRequest(
        email="john@example.com",
        password="SecurePassword123"
    )
    response = await vexen.auth.service.login(request)

    if response:
        print(f"Access token: {response.access_token}")
        print(f"User ID: {response.user_id}")
```

## Architecture

### System Integration

The `VexenContainer` initializes all three systems with shared configuration:

1. **User System** - Initialized first, provides user repository
2. **RBAC System** - Initialized second, manages roles and permissions
3. **Auth System** - Initialized last, configured to use the user repository

### Dependency Injection

The auth system is automatically configured to work with the user repository:

```python
# Automatic integration
async with VexenContainer(config) as vexen:
    # Auth system can access user information
    # without tight coupling to user service
    pass
```

### Manual Lifecycle

If you need more control over initialization:

```python
vexen = VexenContainer(config)
await vexen.init()

try:
    # Use systems
    pass
finally:
    await vexen.close()
```

## API Reference

### VexenContainer

#### Properties

- `user: VexenUser` - Access to user management system
- `rbac: RBAC` - Access to RBAC system
- `auth: VexenAuth` - Access to authentication system

#### Methods

- `async init()` - Initialize all systems
- `async close()` - Close all systems and cleanup resources
- `async __aenter__()` - Context manager entry
- `async __aexit__()` - Context manager exit

## Examples

See the [examples](./examples) directory for complete examples:

- `basic_usage.py` - Basic integration example
- More examples coming soon...

## Development

### Running Tests

```bash
pytest
```

### Code Quality

```bash
# Format code
ruff format .

# Lint code
ruff check . --fix
```

## License

MIT

## Links

- [vexen-user](https://github.com/vexen-labs/vexen-user)
- [vexen-rbac](https://github.com/vexen-labs/vexen-rbac)
- [vexen-auth](https://github.com/vexen-labs/vexen-auth)
