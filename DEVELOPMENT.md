# Development Guide

## Setup

### Installing Dependencies

Since `vexen-auth` is not yet published to PyPI, you need to install it from the local repository:

```bash
# From the vexen/core directory
cd /home/albakore/Documents/Repositories/vexen/core

# Install vexen-user and vexen-rbac from PyPI
pip install vexen-user>=0.1.3 vexen-rbac>=0.1.3

# Install vexen-auth from local path
pip install -e ../auth

# Install other dependencies
pip install sqlalchemy[asyncio]>=2.0.44 asyncpg>=0.29.0 greenlet>=3.0.0 pyjwt>=2.8.0 bcrypt>=4.1.0

# Install dev dependencies
pip install pytest>=8.0.0 pytest-asyncio>=0.23.0 ruff>=0.8.0
```

### Using uv (recommended)

```bash
# Install dependencies with uv
cd /home/albakore/Documents/Repositories/vexen/core
uv pip install -e ../auth
uv pip install vexen-user>=0.1.3 vexen-rbac>=0.1.3
uv sync
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=vexen_core --cov-report=html

# Run specific test
pytest tests/test_container.py::test_container_initialization
```

### Integration Tests

Integration tests require a running PostgreSQL database:

```bash
# Start PostgreSQL with Docker
docker run --name vexen-test-db \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_USER=vexen \
  -e POSTGRES_DB=vexen_test \
  -p 5432:5432 \
  -d postgres:15

# Run integration tests
DATABASE_URL="postgresql+asyncpg://vexen:password@localhost:5432/vexen_test" \
  pytest -v
```

## Code Quality

### Formatting

```bash
# Format code
ruff format .

# Check formatting
ruff format --check .
```

### Linting

```bash
# Lint and auto-fix
ruff check . --fix

# Lint without auto-fix
ruff check .
```

### Type Checking

```bash
# Run mypy (if installed)
mypy vexen_core
```

## Project Structure

```
vexen-core/
├── vexen_core/           # Source code
│   ├── __init__.py       # Public API
│   ├── config.py         # Configuration dataclass
│   └── container.py      # Main container implementation
├── examples/             # Usage examples
│   └── basic_usage.py
├── tests/                # Test suite
│   └── test_container.py
├── pyproject.toml        # Project configuration
└── README.md             # User documentation
```

## Publishing

### Before Publishing

1. Ensure vexen-auth is published to PyPI
2. Update version in pyproject.toml
3. Run all tests
4. Run code quality checks

### Build Package

```bash
# Install build tools
pip install build twine

# Build package
python -m build

# Check package
twine check dist/*
```

### Publish to PyPI

```bash
# Test PyPI first
twine upload --repository testpypi dist/*

# Production PyPI
twine upload dist/*
```

## Architecture Notes

### Current Limitations

1. **No Shared Transactions**: Currently, each system (user, rbac, auth) manages its own database session. This means operations across systems are not atomic.

2. **Future Improvement**: To enable shared transactions, the underlying systems would need to support accepting external sessions. This is a planned enhancement.

### System Initialization Order

The container initializes systems in this order:

1. **User System** - First, as it has no dependencies
2. **RBAC System** - Second, independent of user
3. **Auth System** - Last, configured with user repository

This order ensures that auth can access user information through the repository interface.

### Dependency Injection Pattern

The container uses manual dependency injection:

```python
# Auth is configured to use user's repository
auth_config = AuthConfig(
    database_url=self.config.database_url,
    user_repository=self._user_system.repository,  # DI here
    # ... other config
)
```

This creates loose coupling while enabling system integration.

## Common Issues

### Import Errors

If you get `ModuleNotFoundError: No module named 'vexen_auth'`:

```bash
# Make sure vexen-auth is installed from local path
pip install -e ../auth
```

### Database Connection Errors

Make sure PostgreSQL is running and accessible:

```bash
# Test connection
psql postgresql://user:password@localhost:5432/dbname
```

### Type Checking Issues

Some type issues may appear due to optional dependencies. These are usually safe to ignore in development.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and code quality checks
5. Submit a pull request

## Questions?

Open an issue on GitHub or contact the maintainers.
