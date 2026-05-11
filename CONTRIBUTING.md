# Contributing to TestForge

Thank you for your interest in contributing to TestForge! This document provides guidelines and instructions for contributing.

## 🤝 How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- A clear description of the problem
- Steps to reproduce
- Expected behavior
- Actual behavior
- Your environment (Python version, OS, etc.)

### Suggesting Features

We welcome feature suggestions! Please create an issue with:
- A clear description of the feature
- Use case and benefits
- Possible implementation approach (if you have ideas)

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Commit your changes using conventional commits
6. Push to your branch
7. Open a Pull Request

## 📝 Commit Convention

We use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

Example: `feat: add support for Java language analysis`

## 🧪 Running Tests

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ -v --cov=testforge
```

## 📚 Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to public functions and classes
- Keep functions focused and small

## 🙏 Thank You

Every contribution is appreciated! Thank you for helping make TestForge better.
