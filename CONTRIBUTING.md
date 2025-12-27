# Contributing to Agentic AI on WatsonX with MCP Gateway

First off, thank you for considering contributing to this project! It's people like you that make this project such a great tool.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)
- [Community](#community)

---

## Code of Conduct

This project and everyone participating in it is governed by our commitment to fostering an open and welcoming environment. We expect all contributors to:

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

---

## Getting Started

### Prerequisites

Before you begin, ensure you have:

- Python 3.10 or higher
- uv package manager installed
- Git installed and configured
- A GitHub account

### Setting Up Your Development Environment

1. **Fork the repository** on GitHub

2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Agentic-AI-on-WatsonX-with-MCP-Gateway.git
   cd Agentic-AI-on-WatsonX-with-MCP-Gateway
   ```

3. **Add the upstream repository**:
   ```bash
   git remote add upstream https://github.com/ruslanmv/Agentic-AI-on-WatsonX-with-MCP-Gateway.git
   ```

4. **Install dependencies**:
   ```bash
   make install-dev
   ```

5. **Set up pre-commit hooks**:
   ```bash
   make setup
   ```

6. **Create a `.env` file**:
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

---

## Development Workflow

### Creating a Branch

Always create a new branch for your work:

```bash
# Update your main branch
git checkout main
git pull upstream main

# Create a new feature branch
git checkout -b feature/your-feature-name
```

Branch naming conventions:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `refactor/` - Code refactoring
- `test/` - Test additions or modifications

### Making Changes

1. **Make your changes** in your feature branch

2. **Run code quality checks**:
   ```bash
   make format        # Format code
   make lint          # Check linting
   make type-check    # Check types
   make check-all     # Run all checks
   ```

3. **Run tests**:
   ```bash
   make test          # Run tests
   make test-cov      # Run with coverage
   ```

4. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Add descriptive commit message"
   ```

### Commit Message Guidelines

We follow conventional commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Example:**
```
feat(agents): Add Google Search agent implementation

- Implement GoogleSearchAgent class
- Add tests for search functionality
- Update documentation

Closes #123
```

---

## Coding Standards

We maintain high code quality standards:

### Python Style Guide

- **PEP 8**: Follow PEP 8 style guidelines
- **Line Length**: Maximum 100 characters
- **Type Hints**: Use type hints for all function signatures
- **Docstrings**: Google-style docstrings for all public APIs

### Example:

```python
from typing import Optional

def process_data(
    data: str,
    max_length: int = 100,
    verbose: bool = False
) -> Optional[dict[str, str]]:
    """
    Process input data and return structured result.

    Args:
        data: Input data string to process
        max_length: Maximum length for processing (default: 100)
        verbose: Enable verbose logging (default: False)

    Returns:
        Dictionary with processed results, or None if processing fails

    Raises:
        ValueError: If data is empty or invalid
    """
    if not data:
        raise ValueError("Data cannot be empty")

    # Implementation here
    return {"result": data[:max_length]}
```

### Code Quality Tools

We use the following tools (automatically run via pre-commit):

- **Black**: Code formatting
- **isort**: Import sorting
- **Ruff**: Fast linting
- **mypy**: Static type checking

---

## Testing

### Writing Tests

- Place tests in the `tests/` directory
- Mirror the source code structure
- Use descriptive test names
- Follow the AAA pattern (Arrange, Act, Assert)

**Example:**

```python
import pytest
from agentic_ai.agents.wikipedia import WikipediaAgent


@pytest.mark.asyncio
async def test_wikipedia_agent_initialization() -> None:
    """Test that Wikipedia agent initializes correctly."""
    # Arrange
    agent = WikipediaAgent()

    # Act
    await agent.initialize()

    # Assert
    assert agent._initialized is True
    assert agent.client is not None

    # Cleanup
    await agent.cleanup()
```

### Running Tests

```bash
# Run all tests
make test

# Run with coverage
make test-cov

# Run specific test file
uv run pytest tests/test_agents.py -v

# Run specific test
uv run pytest tests/test_agents.py::test_wikipedia_agent_initialization -v
```

### Coverage Requirements

- Aim for >80% code coverage
- All new features must include tests
- Bug fixes should include regression tests

---

## Documentation

### Code Documentation

- **Docstrings**: All public modules, classes, and functions must have docstrings
- **Type Hints**: Use type hints for better IDE support and type checking
- **Comments**: Use comments sparingly, preferring self-documenting code

### Project Documentation

When adding features, update:

- `README.md` - For user-facing changes
- `CONTRIBUTING.md` - For development process changes
- Inline code comments - For complex logic
- API documentation - For new endpoints or agents

---

## Pull Request Process

### Before Submitting

1. **Update your branch** with the latest upstream changes:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run all quality checks**:
   ```bash
   make check-all
   make test-cov
   ```

3. **Update documentation** if needed

4. **Add tests** for new functionality

### Submitting Your PR

1. **Push your branch** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create a Pull Request** on GitHub:
   - Use a clear, descriptive title
   - Reference any related issues
   - Describe what your changes do
   - Include screenshots for UI changes
   - List any breaking changes

3. **PR Template**:
   ```markdown
   ## Description
   Brief description of changes

   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update

   ## Related Issues
   Fixes #123

   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Self-review completed
   - [ ] Comments added for complex code
   - [ ] Documentation updated
   - [ ] Tests added/updated
   - [ ] All tests pass
   - [ ] No new warnings
   ```

### Review Process

- At least one maintainer must approve your PR
- All CI checks must pass
- Address review comments promptly
- Be open to feedback and suggestions

---

## Community

### Getting Help

- **Issues**: Open an issue for bugs or feature requests
- **Discussions**: Use GitHub Discussions for questions
- **Email**: Contact Ruslan Magana for sensitive matters

### Recognition

Contributors will be recognized in:
- Project README
- Release notes
- Git commit history

---

## Questions?

If you have questions about contributing, please:

1. Check existing documentation
2. Search closed issues
3. Open a new discussion
4. Contact the maintainers

Thank you for contributing to Agentic AI on WatsonX with MCP Gateway!

---

**Happy Coding!** 🚀

*Maintained by [Ruslan Magana](https://ruslanmv.com)*
