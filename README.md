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
  <strong>轻量级AI驱动测试用例智能生成引擎</strong>
</p>

<p align="center">
  <em>Lightweight AI-Powered Test Case Intelligent Generation Engine</em>
</p>

---

## 🎉 项目介绍

**TestForge** 是一款**零依赖**的Python CLI工具，能够智能分析源代码结构并自动生成高质量单元测试用例。通过深度代码分析技术，自动提取函数签名、参数类型、返回值等信息，生成符合最佳实践的测试代码。

### 🎯 解决的痛点

- 😫 **手动编写测试耗时费力** - 自动生成测试框架，节省80%+编写时间
- 🤔 **边界条件容易遗漏** - 智能识别参数特征，自动生成边界测试
- 📉 **测试覆盖率难以提升** - 一键生成完整测试套件，快速提升覆盖率
- 🔧 **多框架切换困难** - 统一接口支持pytest、unittest、Jest等多种框架

### ✨ 自研差异化亮点

| 特性 | TestForge | 其他工具 |
|-----|-----------|---------|
| 零依赖 | ✅ 纯Python实现 | ❌ 需要多个依赖包 |
| 多语言支持 | ✅ Python/JS/Go/Rust/Java | ❌ 通常只支持单一语言 |
| 多框架支持 | ✅ pytest/unittest/Jest/Go Test | ❌ 框架固定 |
| 边界测试 | ✅ 智能参数分析 | ❌ 需手动配置 |
| 复杂度分析 | ✅ 圈复杂度计算 | ❌ 无 |

---

## ✨ 核心特性

### 🔍 智能代码分析
- **多语言解析**：支持 Python、JavaScript、TypeScript、Go、Rust、Java
- **AST深度分析**：精确提取函数签名、类结构、装饰器、类型注解
- **复杂度评估**：自动计算圈复杂度，识别高风险代码

### 🤖 智能测试生成
- **基础功能测试**：自动生成函数基本行为验证
- **边界条件测试**：智能识别数值、字符串、列表等参数的边界场景
- **异常处理测试**：自动生成异常捕获测试用例
- **状态变更测试**：针对类方法的状态变化验证

### 🎨 多框架支持
```python
# pytest 风格
def test_function_basic():
    # Arrange
    value = 42
    # Act
    result = function(value)
    # Assert
    assert result is not None

# unittest 风格
class TestClass(unittest.TestCase):
    def test_method(self):
        instance = MyClass()
        self.assertIsNotNone(instance.method())
```

### 📊 测试质量评估
- **覆盖率估算**：预估测试覆盖率百分比
- **测试分类**：按类型（unit/integration/edge_case）分类统计
- **优先级排序**：根据代码复杂度自动分配测试优先级

---

## 🚀 快速开始

### 📋 环境要求

- Python 3.8+
- 无需额外依赖！

### 📦 安装

```bash
# 克隆仓库
git clone https://github.com/gitstq/TestForge.git
cd TestForge

# 安装（开发模式）
pip install -e .
```

### 🎮 基本使用

```bash
# 分析源代码结构
testforge analyze my_module.py

# 生成测试用例（默认pytest格式）
testforge generate my_module.py

# 指定输出路径
testforge generate my_module.py -o tests/test_my_module.py

# 使用unittest框架
testforge generate my_module.py -f unittest

# 批量处理目录
testforge batch ./src -f pytest
```

---

## 📖 详细使用指南

### 🔬 代码分析命令

```bash
# 分析单个文件
testforge analyze calculator.py

# 导出分析结果为JSON
testforge analyze calculator.py -o analysis.json
```

**输出示例：**
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

### 🧪 测试生成命令

```bash
# 基础生成
testforge generate myapp.py

# 指定测试框架
testforge generate myapp.py -f pytest     # pytest (默认)
testforge generate myapp.py -f unittest   # unittest
testforge generate myapp.py -f jest       # Jest (JavaScript)
testforge generate myapp.py -f go         # Go test
testforge generate myapp.py -f rust       # Rust test
```

### 📁 批量处理

```bash
# 处理整个目录
testforge batch ./src

# 只处理特定扩展名
testforge batch ./src -e .py

# 指定测试框架
testforge batch ./src -f unittest
```

### 📈 查看统计信息

```bash
testforge stats tests/test_myapp.py
```

---

## 💡 设计思路与迭代规划

### 🏗️ 架构设计

```
TestForge
├── analyzers/          # 代码分析器
│   ├── python.py       # Python AST分析
│   ├── javascript.py   # JS/TS正则分析
│   └── ...
├── generators/         # 测试生成器
│   ├── pytest.py       # pytest模板
│   ├── unittest.py     # unittest模板
│   └── ...
├── providers/          # LLM提供商接口
│   ├── openai.py
│   ├── anthropic.py
│   └── ollama.py
└── cli.py              # 命令行接口
```

### 🎯 技术选型原因

1. **纯Python实现**：零依赖，安装即用，避免版本冲突
2. **AST解析**：比正则更精确，支持复杂语法结构
3. **模板引擎**：灵活可扩展，支持自定义测试风格
4. **多LLM接口**：预留AI增强接口，支持智能测试生成

### 📅 后续迭代计划

| 版本 | 功能 |
|-----|------|
| v1.1 | 集成OpenAI/Claude API，AI智能生成测试 |
| v1.2 | 支持Mock对象自动生成 |
| v1.3 | 测试用例质量评分与优化建议 |
| v1.4 | CI/CD集成，自动检测代码变更生成测试 |
| v2.0 | Web UI可视化界面 |

---

## 📦 打包与部署指南

### 本地开发

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
python -m pytest tests/ -v

# 构建分发包
pip install build
python -m build
```

### 作为库使用

```python
from testforge import TestForge, TestFramework

# 创建引擎实例
forge = TestForge(framework=TestFramework.PYTEST)

# 分析代码
module_info = forge.analyze('my_module.py')

# 生成测试
test_suite = forge.generate(module_info)

# 导出测试文件
forge.export_tests(test_suite, 'test_my_module.py')

# 获取统计信息
stats = forge.get_statistics(test_suite)
print(f"生成了 {stats['total_tests']} 个测试用例")
print(f"预估覆盖率: {stats['coverage_estimate']:.1f}%")
```

---

## 🤝 贡献指南

我们欢迎所有形式的贡献！

### 提交PR流程

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'feat: 添加某个很棒的功能'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

### 提交规范

- `feat:` 新功能
- `fix:` 修复问题
- `docs:` 文档更新
- `refactor:` 代码重构
- `test:` 测试相关

### Issue反馈

请使用 [GitHub Issues](https://github.com/gitstq/TestForge/issues) 提交问题，包含：
- 问题描述
- 复现步骤
- 期望行为
- 实际行为

---

## 📄 开源协议说明

本项目采用 **MIT License** 开源协议。

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
  如果这个项目对你有帮助，请给一个 ⭐️ Star！
</p>
