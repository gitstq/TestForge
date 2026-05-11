"""
TestForge Unit Tests
"""

import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from testforge.core import (
    TestForge, CodeAnalyzer, TestGenerator,
    TestFramework, Language, FunctionInfo, ClassInfo, ModuleInfo
)


class TestCodeAnalyzer:
    """Tests for CodeAnalyzer"""
    
    def setup_method(self):
        self.analyzer = CodeAnalyzer()
    
    def test_analyze_python_function(self, tmp_path):
        """Test analyzing Python function"""
        # Create test file
        test_file = tmp_path / "sample.py"
        test_file.write_text('''
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

async def fetch_data(url: str):
    """Fetch data from URL."""
    pass
''')
        
        result = self.analyzer.analyze_file(str(test_file))
        
        assert result.language == Language.PYTHON
        assert len(result.functions) == 2
        assert result.functions[0].name == 'add'
        assert result.functions[0].is_async == False
        assert result.functions[1].name == 'fetch_data'
        assert result.functions[1].is_async == True
    
    def test_analyze_python_class(self, tmp_path):
        """Test analyzing Python class"""
        test_file = tmp_path / "sample.py"
        test_file.write_text('''
class Calculator:
    """Simple calculator."""
    
    def __init__(self):
        self.value = 0
    
    def add(self, x: int) -> int:
        """Add to value."""
        self.value += x
        return self.value
''')
        
        result = self.analyzer.analyze_file(str(test_file))
        
        assert len(result.classes) == 1
        assert result.classes[0].name == 'Calculator'
        assert len(result.classes[0].methods) == 2
    
    def test_analyze_javascript(self, tmp_path):
        """Test analyzing JavaScript file"""
        test_file = tmp_path / "sample.js"
        test_file.write_text('''
function greet(name) {
    return "Hello, " + name;
}

const add = (a, b) => a + b;

class Person {
    constructor(name) {
        this.name = name;
    }
}
''')
        
        result = self.analyzer.analyze_file(str(test_file))
        
        assert result.language == Language.JAVASCRIPT
        assert len(result.functions) >= 2
        assert len(result.classes) == 1


class TestTestGenerator:
    """Tests for TestGenerator"""
    
    def setup_method(self):
        self.generator = TestGenerator(TestFramework.PYTEST)
    
    def test_generate_function_tests(self):
        """Test generating tests for a function"""
        func = FunctionInfo(
            name='calculate',
            args=['value', 'multiplier'],
            returns='int',
            docstring='Calculate something',
            source_code='def calculate(value, multiplier): return value * multiplier'
        )
        
        module = ModuleInfo(
            path='test.py',
            functions=[func],
            classes=[],
            imports=[],
            docstring=None
        )
        
        suite = self.generator.generate_tests(module)
        
        assert len(suite.test_cases) > 0
        assert suite.framework == TestFramework.PYTEST
        assert any(tc.function_name == 'calculate' for tc in suite.test_cases)
    
    def test_generate_class_tests(self):
        """Test generating tests for a class"""
        method = FunctionInfo(
            name='process',
            args=['self', 'data'],
            returns='str',
            docstring='Process data',
            is_method=True,
            class_name='Processor',
            source_code='def process(self, data): return str(data)'
        )
        
        cls = ClassInfo(
            name='Processor',
            methods=[method],
            attributes=[],
            docstring='Data processor',
            bases=[]
        )
        
        module = ModuleInfo(
            path='processor.py',
            functions=[],
            classes=[cls],
            imports=[],
            docstring=None
        )
        
        suite = self.generator.generate_tests(module)
        
        assert len(suite.test_cases) > 0
        assert any('Processor' in tc.name for tc in suite.test_cases)
    
    def test_coverage_estimation(self):
        """Test coverage estimation"""
        func = FunctionInfo(
            name='test_func',
            args=[],
            returns=None,
            docstring=None,
            source_code='def test_func(): pass'
        )
        
        module = ModuleInfo(
            path='test.py',
            functions=[func],
            classes=[],
            imports=[],
            docstring=None
        )
        
        suite = self.generator.generate_tests(module)
        
        assert suite.coverage_estimate >= 0
        assert suite.coverage_estimate <= 100


class TestTestForge:
    """Tests for TestForge main class"""
    
    def setup_method(self):
        self.forge = TestForge()
    
    def test_analyze_and_generate(self, tmp_path):
        """Test full analyze and generate workflow"""
        test_file = tmp_path / "sample.py"
        test_file.write_text('''
def add(a, b):
    return a + b

class Calculator:
    def multiply(self, a, b):
        return a * b
''')
        
        module = self.forge.analyze(str(test_file))
        suite = self.forge.generate(module)
        
        assert len(module.functions) == 1
        assert len(module.classes) == 1
        assert len(suite.test_cases) > 0
    
    def test_export_tests(self, tmp_path):
        """Test exporting tests to file"""
        func = FunctionInfo(
            name='test_func',
            args=[],
            returns=None,
            docstring='Test function',
            source_code='def test_func(): pass'
        )
        
        module = ModuleInfo(
            path=str(tmp_path / 'sample.py'),
            functions=[func],
            classes=[],
            imports=[],
            docstring=None
        )
        
        suite = self.forge.generate(module)
        output = tmp_path / 'test_sample.py'
        
        result = self.forge.export_tests(suite, str(output))
        
        assert output.exists()
        content = output.read_text()
        assert 'test_test_func' in content


class TestFrameworkSupport:
    """Tests for different test frameworks"""
    
    def test_pytest_generation(self, tmp_path):
        """Test pytest generation"""
        forge = TestForge(framework=TestFramework.PYTEST)
        
        test_file = tmp_path / "sample.py"
        test_file.write_text('def hello(): return "world"')
        
        suite = forge.generate_from_file(str(test_file))
        
        assert suite.framework == TestFramework.PYTEST
        assert 'pytest' in str(suite.imports)
    
    def test_unittest_generation(self, tmp_path):
        """Test unittest generation"""
        forge = TestForge(framework=TestFramework.UNITTEST)
        
        test_file = tmp_path / "sample.py"
        test_file.write_text('def hello(): return "world"')
        
        suite = forge.generate_from_file(str(test_file))
        
        assert suite.framework == TestFramework.UNITTEST


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
