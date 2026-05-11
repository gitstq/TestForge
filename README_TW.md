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
  <strong>輕量級AI驅動測試案例智慧生成引擎</strong>
</p>

<p align="center">
  <em>Lightweight AI-Powered Test Case Intelligent Generation Engine</em>
</p>

---

## 🎉 專案介紹

**TestForge** 是一款**零依賴**的Python CLI工具，能夠智慧分析原始碼結構並自動生成高品質單元測試案例。透過深度程式碼分析技術，自動提取函數簽名、參數型別、返回值等資訊，生成符合最佳實踐的測試程式碼。

### 🎯 解決的痛點

- 😫 **手動編寫測試耗時費力** - 自動生成測試框架，節省80%+編寫時間
- 🤔 **邊界條件容易遺漏** - 智慧參數特徵識別，自動生成邊界測試
- 📉 **測試覆蓋率難以提升** - 一鍵生成完整測試套件，快速提升覆蓋率
- 🔧 **多框架切換困難** - 統一介面支援pytest、unittest、Jest等多種框架

### ✨ 自研差異化亮點

| 特性 | TestForge | 其他工具 |
|-----|-----------|---------|
| 零依賴 | ✅ 純Python實現 | ❌ 需要多個依賴套件 |
| 多語言支援 | ✅ Python/JS/Go/Rust/Java | ❌ 通常只支援單一語言 |
| 多框架支援 | ✅ pytest/unittest/Jest/Go Test | ❌ 框架固定 |
| 邊界測試 | ✅ 智慧參數分析 | ❌ 需手動配置 |
| 複雜度分析 | ✅ 圈複雜度計算 | ❌ 無 |

---

## ✨ 核心特性

### 🔍 智慧程式碼分析
- **多語言解析**：支援 Python、JavaScript、TypeScript、Go、Rust、Java
- **AST深度分析**：精確提取函數簽名、類別結構、裝飾器、型別註解
- **複雜度評估**：自動計算圈複雜度，識別高風險程式碼

### 🤖 智慧測試生成
- **基礎功能測試**：自動生成函數基本行為驗證
- **邊界條件測試**：智慧識別數值、字串、列表等參數的邊界場景
- **例外處理測試**：自動生成例外捕獲測試案例
- **狀態變更測試**：針對類別方法的狀態變化驗證

### 🎨 多框架支援
```python
# pytest 風格
def test_function_basic():
    # Arrange
    value = 42
    # Act
    result = function(value)
    # Assert
    assert result is not None

# unittest 風格
class TestClass(unittest.TestCase):
    def test_method(self):
        instance = MyClass()
        self.assertIsNotNone(instance.method())
```

### 📊 測試品質評估
- **覆蓋率估算**：預估測試覆蓋率百分比
- **測試分類**：按型別（unit/integration/edge_case）分類統計
- **優先級排序**：根據程式碼複雜度自動分配測試優先級

---

## 🚀 快速開始

### 📋 環境要求

- Python 3.8+
- 無需額外依賴！

### 📦 安裝

```bash
# 複製儲存庫
git clone https://github.com/gitstq/TestForge.git
cd TestForge

# 安裝（開發模式）
pip install -e .
```

### 🎮 基本使用

```bash
# 分析原始碼結構
testforge analyze my_module.py

# 生成測試案例（預設pytest格式）
testforge generate my_module.py

# 指定輸出路徑
testforge generate my_module.py -o tests/test_my_module.py

# 使用unittest框架
testforge generate my_module.py -f unittest

# 批次處理目錄
testforge batch ./src -f pytest
```

---

## 📖 詳細使用指南

### 🔬 程式碼分析命令

```bash
# 分析單一檔案
testforge analyze calculator.py

# 匯出分析結果為JSON
testforge analyze calculator.py -o analysis.json
```

**輸出範例：**
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

### 🧪 測試生成命令

```bash
# 基礎生成
testforge generate myapp.py

# 指定測試框架
testforge generate myapp.py -f pytest     # pytest (預設)
testforge generate myapp.py -f unittest   # unittest
testforge generate myapp.py -f jest       # Jest (JavaScript)
testforge generate myapp.py -f go         # Go test
testforge generate myapp.py -f rust       # Rust test
```

### 📁 批次處理

```bash
# 處理整個目錄
testforge batch ./src

# 只處理特定副檔名
testforge batch ./src -e .py

# 指定測試框架
testforge batch ./src -f unittest
```

### 📈 查看統計資訊

```bash
testforge stats tests/test_myapp.py
```

---

## 💡 設計思路與迭代規劃

### 🏗️ 架構設計

```
TestForge
├── analyzers/          # 程式碼分析器
│   ├── python.py       # Python AST分析
│   ├── javascript.py   # JS/TS正則分析
│   └── ...
├── generators/         # 測試生成器
│   ├── pytest.py       # pytest模板
│   ├── unittest.py     # unittest模板
│   └── ...
├── providers/          # LLM提供商介面
│   ├── openai.py
│   ├── anthropic.py
│   └── ollama.py
└── cli.py              # 命令列介面
```

### 🎯 技術選型原因

1. **純Python實現**：零依賴，安裝即用，避免版本衝突
2. **AST解析**：比正則更精確，支援複雜語法結構
3. **模板引擎**：靈活可擴展，支援自定義測試風格
4. **多LLM介面**：預留AI增強介面，支援智慧測試生成

### 📅 後續迭代計劃

| 版本 | 功能 |
|-----|------|
| v1.1 | 整合OpenAI/Claude API，AI智慧生成測試 |
| v1.2 | 支援Mock物件自動生成 |
| v1.3 | 測試案例品質評分與優化建議 |
| v1.4 | CI/CD整合，自動檢測程式碼變更生成測試 |
| v2.0 | Web UI視覺化介面 |

---

## 📦 打包與部署指南

### 本地開發

```bash
# 安裝開發依賴
pip install -e ".[dev]"

# 執行測試
python -m pytest tests/ -v

# 建置分發套件
pip install build
python -m build
```

### 作為函式庫使用

```python
from testforge import TestForge, TestFramework

# 建立引擎實例
forge = TestForge(framework=TestFramework.PYTEST)

# 分析程式碼
module_info = forge.analyze('my_module.py')

# 生成測試
test_suite = forge.generate(module_info)

# 匯出測試檔案
forge.export_tests(test_suite, 'test_my_module.py')

# 取得統計資訊
stats = forge.get_statistics(test_suite)
print(f"生成了 {stats['total_tests']} 個測試案例")
print(f"預估覆蓋率: {stats['coverage_estimate']:.1f}%")
```

---

## 🤝 貢獻指南

我們歡迎所有形式的貢獻！

### 提交PR流程

1. Fork 本儲存庫
2. 建立特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交變更 (`git commit -m 'feat: 新增某個很棒的功能'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

### 提交規範

- `feat:` 新功能
- `fix:` 修復問題
- `docs:` 文檔更新
- `refactor:` 程式碼重構
- `test:` 測試相關

### Issue回報

請使用 [GitHub Issues](https://github.com/gitstq/TestForge/issues) 提交問題，包含：
- 問題描述
- 重現步驟
- 預期行為
- 實際行為

---

## 📄 開源協議说明

本專案採用 **MIT License** 開源協議。

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
  如果這個專案對你有幫助，請給一個 ⭐️ Star！
</p>
