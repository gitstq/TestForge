<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/badge/Zero%20Dependencies-✓-brightgreen?style=for-the-badge" alt="Zero Dependencies">
</p>

<p align="center">
  <a href="README.md">简体中文</a> | <a href="README_EN.md">English</a> | <a href="README_TW.md">繁體中文</a>
</p>

<h1 align="center">🧪 TestForge</h1>

<p align="center">
  <strong>Lightweight AI-Powered Test Case Intelligent Generation Engine</strong>
</p>

<p align="center">
  <em>轻量级AI驱动测试用例智能生成引擎</em>
</p>

---

## 🎉 Introduction

**TestForge** is a **zero-dependency** Python CLI tool that intelligently analyzes source code structure and automatically generates high-quality unit test cases. Through deep code analysis technology, it automatically extracts function signatures, parameter types, return values, and generates test code that follows best practices.

### 🎯 Problems Solved

- 😫 **Manual test writing is time-consuming** - Auto-generate test scaffolding, save 80%+ writing time
- 🤔 **Edge cases are easily missed** - Smart parameter feature recognition, auto-generate edge tests
- 📉 **Test coverage is hard to improve** - One-click complete test suite generation, quickly boost coverage
- 🔧 **Multi-framework switching is difficult** - Unified interface supporting pytest, unittest, Jest, and more

### ✨ Key Differentiators

| Feature | TestForge | Other Tools |
|---------|-----------|-------------|
| Zero Dependencies | ✅ Pure Python | ❌ Requires multiple packages |
| Multi-language Support | ✅ Python/JS/Go/Rust/Java | ❌ Usually single language |
| Multi-framework Support | ✅ pytest/unittest/Jest/Go Test | ❌ Fixed framework |
| Edge Case Testing | ✅ Smart parameter analysis | ❌ Manual configuration |
| Complexity Analysis | ✅ Cyclomatic complexity | ❌ None |

---

## ✨ Core Features

### 🔍 Intelligent Code Analysis
- **Multi-language Parsing**: Supports Python, JavaScript, TypeScript, Go, Rust, Java
- **Deep AST Analysis**: Precisely extracts function signatures, class structures, decorators, type annotations
- **Complexity Assessment**: Automatically calculates cyclomatic complexity, identifies high-risk code

### 🤖 Intelligent Test Generation
- **Basic Functionality Tests**: Auto-generates function basic behavior verification
- **Edge Case Tests**: Smart recognition of numeric, string, list parameter boundary scenarios
- **Exception Handling Tests**: Auto-generates exception capture test cases
- **State Change Tests**: State change verification for class methods

### 🎨 Multi-framework Support
```python
# pytest style
def test_function_basic():
    # Arrange
    value = 42
    # Act
    result = function(value)
    # Assert
    assert result is not None

# unittest style
class TestClass(unittest.TestCase):
    def test_method(self):
        instance = MyClass()
        self.assertIsNotNone(instance.method())
```

### 📊 Test Quality Assessment
- **Coverage Estimation**: Estimates test coverage percentage
- **Test Classification**: Statistics by type (unit/integration/edge_case)
- **Priority Ranking**: Auto-assigns test priority based on code complexity

---

## 🚀 Quick Start

### 📋 Requirements

- Python 3.8+
- No additional dependencies!

### 📦 Installation

```bash
# Clone repository
git clone https://github.com/gitstq/TestForge.git
cd TestForge

# Install (development mode)
pip install -e .
```

### 🎮 Basic Usage

```bash
# Analyze source code structure
testforge analyze my_module.py

# Generate test cases (default pytest format)
testforge generate my_module.py

# Specify output path
testforge generate my_module.py -o tests/test_my_module.py

# Use unittest framework
testforge generate my_module.py -f unittest

# Batch process directory
testforge batch ./src -f pytest
```

---

## 📖 Detailed Usage Guide

### 🔬 Code Analysis Command

```bash
# Analyze single file
testforge analyze calculator.py

# Export analysis results as JSON
testforge analyze calculator.py -o analysis.json
```

**Output Example:**
```
📊 Analysis Results:
  Language: python
  Functions: 5
  Classes: 2
  Imports: 3

🔧 Functions:
  • add(a, b)
    Returns: int
    Doc: Add two numbers
  • calculate(value, multiplier)
    Args: value, multiplier
```

### 🧪 Test Generation Command

```bash
# Basic generation
testforge generate myapp.py

# Specify test framework
testforge generate myapp.py -f pytest     # pytest (default)
testforge generate myapp.py -f unittest   # unittest
testforge generate myapp.py -f jest       # Jest (JavaScript)
testforge generate myapp.py -f go         # Go test
testforge generate myapp.py -f rust       # Rust test
```

### 📁 Batch Processing

```bash
# Process entire directory
testforge batch ./src

# Only process specific extension
testforge batch ./src -e .py

# Specify test framework
testforge batch ./src -f unittest
```

### 📈 View Statistics

```bash
testforge stats tests/test_myapp.py
```

---

## 💡 Design Philosophy & Roadmap

### 🏗️ Architecture Design

```
TestForge
├── analyzers/          # Code analyzers
│   ├── python.py       # Python AST analysis
│   ├── javascript.py   # JS/TS regex analysis
│   └── ...
├── generators/         # Test generators
│   ├── pytest.py       # pytest templates
│   ├── unittest.py     # unittest templates
│   └── ...
├── providers/          # LLM provider interfaces
│   ├── openai.py
│   ├── anthropic.py
│   └── ollama.py
└── cli.py              # Command line interface
```

### 🎯 Technology Choices

1. **Pure Python Implementation**: Zero dependencies, install and run, avoid version conflicts
2. **AST Parsing**: More precise than regex, supports complex syntax structures
3. **Template Engine**: Flexible and extensible, supports custom test styles
4. **Multi-LLM Interface**: Reserved AI enhancement interface, supports intelligent test generation

### 📅 Future Roadmap

| Version | Features |
|---------|----------|
| v1.1 | Integrate OpenAI/Claude API for AI-powered test generation |
| v1.2 | Support automatic Mock object generation |
| v1.3 | Test case quality scoring and optimization suggestions |
| v1.4 | CI/CD integration, auto-detect code changes and generate tests |
| v2.0 | Web UI visualization interface |

---

## 📦 Packaging & Deployment Guide

### Local Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
python -m pytest tests/ -v

# Build distribution package
pip install build
python -m build
```

### Use as Library

```python
from testforge import TestForge, TestFramework

# Create engine instance
forge = TestForge(framework=TestFramework.PYTEST)

# Analyze code
module_info = forge.analyze('my_module.py')

# Generate tests
test_suite = forge.generate(module_info)

# Export test file
forge.export_tests(test_suite, 'test_my_module.py')

# Get statistics
stats = forge.get_statistics(test_suite)
print(f"Generated {stats['total_tests']} test cases")
print(f"Estimated coverage: {stats['coverage_estimate']:.1f}%")
```

---

## 🤝 Contributing Guide

We welcome all forms of contributions!

### PR Submission Process

1. Fork this repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'feat: add some amazing feature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Submit Pull Request

### Commit Convention

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation update
- `refactor:` Code refactoring
- `test:` Test related

### Issue Reporting

Please use [GitHub Issues](https://github.com/gitstq/TestForge/issues) to submit problems, including:
- Problem description
- Reproduction steps
- Expected behavior
- Actual behavior

---

## 📄 License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2026 gitstq

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/gitstq">gitstq</a>
</p>

<p align="center">
  If this project helps you, please give it a ⭐️ Star!
</p>
