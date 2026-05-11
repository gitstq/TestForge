"""
TestForge Core Engine
"""

__version__ = "1.0.0"

import ast
import os
import re
import json
import hashlib
import keyword
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Tuple
from enum import Enum
from pathlib import Path


class TestFramework(Enum):
    """Supported test frameworks"""
    PYTEST = "pytest"
    UNITTEST = "unittest"
    JEST = "jest"
    JUNIT = "junit"
    GO_TEST = "go_test"
    RUST_TEST = "rust_test"


class Language(Enum):
    """Supported programming languages"""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    GO = "go"
    RUST = "rust"
    JAVA = "java"


@dataclass
class FunctionInfo:
    """Information about a function/method"""
    name: str
    args: List[str]
    returns: Optional[str]
    docstring: Optional[str]
    is_async: bool = False
    is_method: bool = False
    class_name: Optional[str] = None
    decorators: List[str] = field(default_factory=list)
    body_lines: int = 0
    complexity: int = 1
    source_code: str = ""


@dataclass
class ClassInfo:
    """Information about a class"""
    name: str
    methods: List[FunctionInfo]
    attributes: List[str]
    docstring: Optional[str]
    bases: List[str]
    decorators: List[str] = field(default_factory=list)


@dataclass
class ModuleInfo:
    """Information about a module/file"""
    path: str
    functions: List[FunctionInfo]
    classes: List[ClassInfo]
    imports: List[str]
    docstring: Optional[str]
    language: Language = Language.PYTHON


@dataclass
class TestCase:
    """Generated test case"""
    name: str
    function_name: str
    test_code: str
    test_type: str  # unit, integration, edge_case, etc.
    description: str
    priority: int = 1  # 1-5, 5 being highest
    tags: List[str] = field(default_factory=list)


@dataclass
class TestSuite:
    """Collection of test cases"""
    module_path: str
    test_cases: List[TestCase]
    framework: TestFramework
    coverage_estimate: float = 0.0
    imports: List[str] = field(default_factory=list)


class CodeAnalyzer:
    """Analyzes source code to extract structure information"""
    
    def __init__(self):
        self.supported_extensions = {
            '.py': Language.PYTHON,
            '.js': Language.JAVASCRIPT,
            '.ts': Language.TYPESCRIPT,
            '.go': Language.GO,
            '.rs': Language.RUST,
            '.java': Language.JAVA,
        }
    
    def analyze_file(self, file_path: str) -> ModuleInfo:
        """Analyze a source file and extract structure information"""
        path = Path(file_path)
        ext = path.suffix.lower()
        
        if ext not in self.supported_extensions:
            raise ValueError(f"Unsupported file type: {ext}")
        
        language = self.supported_extensions[ext]
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            source = f.read()
        
        if language == Language.PYTHON:
            return self._analyze_python(file_path, source)
        elif language in (Language.JAVASCRIPT, Language.TYPESCRIPT):
            return self._analyze_javascript(file_path, source, language)
        elif language == Language.GO:
            return self._analyze_go(file_path, source)
        elif language == Language.RUST:
            return self._analyze_rust(file_path, source)
        elif language == Language.JAVA:
            return self._analyze_java(file_path, source)
        
        return ModuleInfo(
            path=file_path,
            functions=[],
            classes=[],
            imports=[],
            docstring=None,
            language=language
        )
    
    def _analyze_python(self, file_path: str, source: str) -> ModuleInfo:
        """Analyze Python source code using AST"""
        try:
            tree = ast.parse(source)
        except SyntaxError:
            return ModuleInfo(
                path=file_path,
                functions=[],
                classes=[],
                imports=[],
                docstring=None,
                language=Language.PYTHON
            )
        
        # Extract module docstring
        module_docstring = ast.get_docstring(tree)
        
        # Extract imports
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                imports.append(ast.unparse(node))
        
        functions = []
        classes = []
        
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.FunctionDef):
                func_info = self._extract_function_info(node, source)
                functions.append(func_info)
            elif isinstance(node, ast.AsyncFunctionDef):
                func_info = self._extract_function_info(node, source, is_async=True)
                functions.append(func_info)
            elif isinstance(node, ast.ClassDef):
                class_info = self._extract_class_info(node, source)
                classes.append(class_info)
        
        return ModuleInfo(
            path=file_path,
            functions=functions,
            classes=classes,
            imports=list(set(imports)),
            docstring=module_docstring,
            language=Language.PYTHON
        )
    
    def _extract_function_info(self, node, source: str, is_async: bool = False, 
                                class_name: Optional[str] = None) -> FunctionInfo:
        """Extract function information from AST node"""
        args = []
        for arg in node.args.args:
            args.append(arg.arg)
        
        # Get return type annotation
        returns = None
        if node.returns:
            returns = ast.unparse(node.returns)
        
        # Get docstring
        docstring = ast.get_docstring(node)
        
        # Get decorators
        decorators = []
        for dec in node.decorator_list:
            decorators.append(ast.unparse(dec))
        
        # Calculate complexity (simplified)
        complexity = self._calculate_complexity(node)
        
        # Get source code
        source_lines = source.split('\n')
        start_line = node.lineno - 1
        end_line = node.end_lineno if hasattr(node, 'end_lineno') else start_line + 1
        func_source = '\n'.join(source_lines[start_line:end_line])
        
        return FunctionInfo(
            name=node.name,
            args=args,
            returns=returns,
            docstring=docstring,
            is_async=is_async,
            is_method=class_name is not None,
            class_name=class_name,
            decorators=decorators,
            body_lines=end_line - start_line,
            complexity=complexity,
            source_code=func_source
        )
    
    def _extract_class_info(self, node, source: str) -> ClassInfo:
        """Extract class information from AST node"""
        methods = []
        attributes = []
        
        # Get bases
        bases = []
        for base in node.bases:
            bases.append(ast.unparse(base))
        
        # Get decorators
        decorators = []
        for dec in node.decorator_list:
            decorators.append(ast.unparse(dec))
        
        # Get docstring
        docstring = ast.get_docstring(node)
        
        # Extract methods and attributes
        for child in node.body:
            if isinstance(child, ast.FunctionDef):
                func_info = self._extract_function_info(child, source, class_name=node.name)
                methods.append(func_info)
            elif isinstance(child, ast.AsyncFunctionDef):
                func_info = self._extract_function_info(child, source, is_async=True, class_name=node.name)
                methods.append(func_info)
            elif isinstance(child, ast.Assign):
                for target in child.targets:
                    if isinstance(target, ast.Name):
                        attributes.append(target.id)
        
        return ClassInfo(
            name=node.name,
            methods=methods,
            attributes=attributes,
            docstring=docstring,
            bases=bases,
            decorators=decorators
        )
    
    def _calculate_complexity(self, node) -> int:
        """Calculate cyclomatic complexity (simplified)"""
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        return complexity
    
    def _analyze_javascript(self, file_path: str, source: str, language: Language) -> ModuleInfo:
        """Analyze JavaScript/TypeScript source code"""
        functions = []
        classes = []
        
        # Simple regex-based extraction for JS/TS
        # Function declarations
        func_pattern = r'(?:async\s+)?function\s+(\w+)\s*\(([^)]*)\)'
        for match in re.finditer(func_pattern, source):
            name = match.group(1)
            args = [a.strip() for a in match.group(2).split(',') if a.strip()]
            functions.append(FunctionInfo(
                name=name,
                args=args,
                returns=None,
                docstring=None,
                is_async='async' in match.group(0),
                source_code=match.group(0)
            ))
        
        # Arrow functions
        arrow_pattern = r'(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?\([^)]*\)\s*=>'
        for match in re.finditer(arrow_pattern, source):
            functions.append(FunctionInfo(
                name=match.group(1),
                args=[],
                returns=None,
                docstring=None,
                is_async='async' in match.group(0),
                source_code=match.group(0)
            ))
        
        # Class declarations
        class_pattern = r'class\s+(\w+)(?:\s+extends\s+(\w+))?'
        for match in re.finditer(class_pattern, source):
            class_name = match.group(1)
            base = match.group(2) or ""
            classes.append(ClassInfo(
                name=class_name,
                methods=[],
                attributes=[],
                docstring=None,
                bases=[base] if base else []
            ))
        
        return ModuleInfo(
            path=file_path,
            functions=functions,
            classes=classes,
            imports=[],
            docstring=None,
            language=language
        )
    
    def _analyze_go(self, file_path: str, source: str) -> ModuleInfo:
        """Analyze Go source code"""
        functions = []
        
        # Function declarations
        func_pattern = r'func\s+(?:\((\w+)\s+\*?(\w+)\)\s+)?(\w+)\s*\(([^)]*)\)(?:\s*\(([^)]*)\)|\s+(\w+))?'
        for match in re.finditer(func_pattern, source):
            receiver_name = match.group(1)
            receiver_type = match.group(2)
            func_name = match.group(3)
            args_str = match.group(4) or ""
            
            args = [a.strip().split()[-1] if a.strip() else "" for a in args_str.split(',') if a.strip()]
            
            functions.append(FunctionInfo(
                name=func_name,
                args=args,
                returns=None,
                docstring=None,
                is_method=receiver_type is not None,
                class_name=receiver_type,
                source_code=match.group(0)
            ))
        
        return ModuleInfo(
            path=file_path,
            functions=functions,
            classes=[],
            imports=[],
            docstring=None,
            language=Language.GO
        )
    
    def _analyze_rust(self, file_path: str, source: str) -> ModuleInfo:
        """Analyze Rust source code"""
        functions = []
        
        # Function declarations
        func_pattern = r'(?:pub\s+)?(?:async\s+)?fn\s+(\w+)\s*(?:<[^>]*>)?\s*\(([^)]*)\)(?:\s*->\s*([^{]+))?'
        for match in re.finditer(func_pattern, source):
            name = match.group(1)
            args_str = match.group(2) or ""
            returns = match.group(3).strip() if match.group(3) else None
            
            args = [a.strip().split(':')[-1].strip() for a in args_str.split(',') if ':' in a]
            
            functions.append(FunctionInfo(
                name=name,
                args=args,
                returns=returns,
                docstring=None,
                is_async='async' in match.group(0),
                source_code=match.group(0)
            ))
        
        return ModuleInfo(
            path=file_path,
            functions=functions,
            classes=[],
            imports=[],
            docstring=None,
            language=Language.RUST
        )
    
    def _analyze_java(self, file_path: str, source: str) -> ModuleInfo:
        """Analyze Java source code"""
        functions = []
        classes = []
        
        # Class declarations
        class_pattern = r'(?:public|private|protected)?\s*(?:abstract|final)?\s*class\s+(\w+)(?:\s+extends\s+(\w+))?(?:\s+implements\s+([^{]+))?'
        for match in re.finditer(class_pattern, source):
            class_name = match.group(1)
            base = match.group(2) or ""
            classes.append(ClassInfo(
                name=class_name,
                methods=[],
                attributes=[],
                docstring=None,
                bases=[base] if base else []
            ))
        
        # Method declarations
        method_pattern = r'(?:public|private|protected)?\s*(?:static)?\s*(?:\w+(?:<[^>]+>)?)\s+(\w+)\s*\(([^)]*)\)'
        for match in re.finditer(method_pattern, source):
            name = match.group(1)
            if name in ('if', 'while', 'for', 'switch', 'class', 'interface'):
                continue
            args_str = match.group(2) or ""
            args = [a.strip().split()[-1] for a in args_str.split(',') if a.strip()]
            
            functions.append(FunctionInfo(
                name=name,
                args=args,
                returns=None,
                docstring=None,
                source_code=match.group(0)
            ))
        
        return ModuleInfo(
            path=file_path,
            functions=functions,
            classes=classes,
            imports=[],
            docstring=None,
            language=Language.JAVA
        )


class TestGenerator:
    """Generates test cases based on code analysis"""
    
    def __init__(self, framework: TestFramework = TestFramework.PYTEST):
        self.framework = framework
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, str]:
        """Load test templates for different frameworks"""
        return {
            TestFramework.PYTEST: {
                'function': '''
def test_{function_name}():
    """Test {function_name} function"""
    # Arrange
    {arrange}
    
    # Act
    {act}
    
    # Assert
    {assertion}
''',
                'class': '''
class Test{class_name}:
    """Test class for {class_name}"""
    
    def test_{method_name}(self):
        """Test {method_name} method"""
        {test_body}
''',
                'async': '''
@pytest.mark.asyncio
async def test_{function_name}():
    """Test async {function_name} function"""
    {test_body}
'''
            },
            TestFramework.UNITTEST: {
                'function': '''
    def test_{function_name}(self):
        """Test {function_name} function"""
        # Arrange
        {arrange}
        
        # Act
        {act}
        
        # Assert
        {assertion}
''',
                'class': '''
class Test{class_name}(unittest.TestCase):
    """Test class for {class_name}"""
    
    def test_{method_name}(self):
        """Test {method_name} method"""
        {test_body}
'''
            },
            TestFramework.JEST: {
                'function': '''
test('{function_name}', () => {{
    // Arrange
    {arrange}
    
    // Act
    {act}
    
    // Assert
    expect({expect}).{matcher};
}});
''',
                'async': '''
test('{function_name}', async () => {{
    {test_body}
}});
'''
            },
            TestFramework.GO_TEST: {
                'function': '''
func Test{function_name}(t *testing.T) {{
    // Arrange
    {arrange}
    
    // Act
    {act}
    
    // Assert
    if {condition} {{
        t.Errorf("{error_message}")
    }}
}}
'''
            },
            TestFramework.RUST_TEST: {
                'function': '''
#[test]
fn test_{function_name}() {{
    // Arrange
    {arrange}
    
    // Act
    {act}
    
    // Assert
    assert!({condition}, "{error_message}");
}}
'''
            }
        }
    
    def generate_tests(self, module_info: ModuleInfo) -> TestSuite:
        """Generate test suite for a module"""
        test_cases = []
        
        # Generate tests for standalone functions
        for func in module_info.functions:
            if not func.is_method and not func.name.startswith('_'):
                test_cases.extend(self._generate_function_tests(func, module_info))
        
        # Generate tests for class methods
        for cls in module_info.classes:
            for method in cls.methods:
                if not method.name.startswith('_'):
                    test_cases.extend(self._generate_method_tests(method, cls, module_info))
        
        # Calculate estimated coverage
        coverage = self._estimate_coverage(module_info, test_cases)
        
        return TestSuite(
            module_path=module_info.path,
            test_cases=test_cases,
            framework=self.framework,
            coverage_estimate=coverage,
            imports=self._get_required_imports(module_info)
        )
    
    def _generate_function_tests(self, func: FunctionInfo, module_info: ModuleInfo) -> List[TestCase]:
        """Generate test cases for a function"""
        tests = []
        
        # Basic functionality test
        tests.append(TestCase(
            name=f"test_{func.name}_basic",
            function_name=func.name,
            test_code=self._render_function_test(func, 'basic'),
            test_type='unit',
            description=f"Basic functionality test for {func.name}",
            priority=5,
            tags=['unit', 'basic']
        ))
        
        # Edge case tests based on arguments
        for i, arg in enumerate(func.args):
            if arg in ('value', 'val', 'x', 'n', 'num', 'count', 'size'):
                tests.append(TestCase(
                    name=f"test_{func.name}_edge_zero",
                    function_name=func.name,
                    test_code=self._render_function_test(func, 'edge_zero', arg),
                    test_type='edge_case',
                    description=f"Edge case test for {func.name} with zero {arg}",
                    priority=4,
                    tags=['edge_case', 'zero']
                ))
                tests.append(TestCase(
                    name=f"test_{func.name}_edge_negative",
                    function_name=func.name,
                    test_code=self._render_function_test(func, 'edge_negative', arg),
                    test_type='edge_case',
                    description=f"Edge case test for {func.name} with negative {arg}",
                    priority=3,
                    tags=['edge_case', 'negative']
                ))
            elif arg in ('s', 'string', 'text', 'name', 'path'):
                tests.append(TestCase(
                    name=f"test_{func.name}_edge_empty_string",
                    function_name=func.name,
                    test_code=self._render_function_test(func, 'edge_empty_string', arg),
                    test_type='edge_case',
                    description=f"Edge case test for {func.name} with empty string",
                    priority=4,
                    tags=['edge_case', 'empty_string']
                ))
            elif arg in ('items', 'list', 'data', 'arr', 'values'):
                tests.append(TestCase(
                    name=f"test_{func.name}_edge_empty_list",
                    function_name=func.name,
                    test_code=self._render_function_test(func, 'edge_empty_list', arg),
                    test_type='edge_case',
                    description=f"Edge case test for {func.name} with empty list",
                    priority=4,
                    tags=['edge_case', 'empty_list']
                ))
        
        # Exception test
        tests.append(TestCase(
            name=f"test_{func.name}_exception",
            function_name=func.name,
            test_code=self._render_function_test(func, 'exception'),
            test_type='exception',
            description=f"Exception handling test for {func.name}",
            priority=3,
            tags=['exception', 'error_handling']
        ))
        
        return tests
    
    def _generate_method_tests(self, method: FunctionInfo, cls: ClassInfo, 
                                module_info: ModuleInfo) -> List[TestCase]:
        """Generate test cases for a class method"""
        tests = []
        
        # Basic method test
        tests.append(TestCase(
            name=f"test_{cls.name}_{method.name}_basic",
            function_name=method.name,
            test_code=self._render_method_test(method, cls, 'basic'),
            test_type='unit',
            description=f"Basic test for {cls.name}.{method.name}",
            priority=5,
            tags=['unit', 'method', cls.name]
        ))
        
        # State mutation test
        if method.args and len(method.args) > 1:  # self + args
            tests.append(TestCase(
                name=f"test_{cls.name}_{method.name}_state_change",
                function_name=method.name,
                test_code=self._render_method_test(method, cls, 'state_change'),
                test_type='integration',
                description=f"State change test for {cls.name}.{method.name}",
                priority=4,
                tags=['integration', 'state']
            ))
        
        return tests
    
    def _render_function_test(self, func: FunctionInfo, test_type: str, 
                               edge_arg: str = None) -> str:
        """Render test code for a function"""
        template = self.templates[self.framework]['function']
        
        if test_type == 'basic':
            arrange = self._generate_arrange(func)
            act = self._generate_act(func)
            assertion = self._generate_assert(func)
        elif test_type == 'edge_zero':
            arrange = f"# Edge case: zero value\n        {edge_arg} = 0"
            act = self._generate_act(func)
            assertion = "# Verify behavior with zero"
        elif test_type == 'edge_negative':
            arrange = f"# Edge case: negative value\n        {edge_arg} = -1"
            act = self._generate_act(func)
            assertion = "# Verify behavior with negative value"
        elif test_type == 'edge_empty_string':
            arrange = f"# Edge case: empty string\n        {edge_arg} = ''"
            act = self._generate_act(func)
            assertion = "# Verify behavior with empty string"
        elif test_type == 'edge_empty_list':
            arrange = f"# Edge case: empty list\n        {edge_arg} = []"
            act = self._generate_act(func)
            assertion = "# Verify behavior with empty list"
        elif test_type == 'exception':
            arrange = "# Test exception handling\n        # TODO: Add invalid inputs"
            act = self._generate_act(func, wrap_try=True)
            assertion = "# Verify exception is raised correctly"
        else:
            arrange = "# TODO: Add test data"
            act = self._generate_act(func)
            assertion = "# TODO: Add assertions"
        
        return template.format(
            function_name=func.name,
            arrange=arrange,
            act=act,
            assertion=assertion
        )
    
    def _render_method_test(self, method: FunctionInfo, cls: ClassInfo, 
                            test_type: str) -> str:
        """Render test code for a class method"""
        template = self.templates[self.framework]['class']
        
        test_body = f"# Create instance\n        instance = {cls.name}()\n        \n        # TODO: Add test implementation"
        
        return template.format(
            class_name=cls.name,
            method_name=method.name,
            test_body=test_body
        )
    
    def _generate_arrange(self, func: FunctionInfo) -> str:
        """Generate arrange section for test"""
        lines = []
        for arg in func.args:
            if arg == 'self':
                continue
            # Generate default test values based on argument name
            if arg in ('value', 'val', 'x', 'n'):
                lines.append(f"{arg} = 42")
            elif arg in ('s', 'string', 'text', 'name'):
                lines.append(f"{arg} = 'test_value'")
            elif arg in ('items', 'list', 'data'):
                lines.append(f"{arg} = [1, 2, 3]")
            elif arg in ('flag', 'enabled', 'active'):
                lines.append(f"{arg} = True")
            else:
                lines.append(f"{arg} = None  # TODO: Provide test value")
        return '\n        '.join(lines) if lines else "# No arguments"
    
    def _generate_act(self, func: FunctionInfo, wrap_try: bool = False) -> str:
        """Generate act section for test"""
        args = ', '.join([a for a in func.args if a != 'self'])
        
        if func.is_async:
            if wrap_try:
                return f"with pytest.raises(Exception):\n            result = await {func.name}({args})"
            return f"result = await {func.name}({args})"
        else:
            if wrap_try:
                return f"with pytest.raises(Exception):\n            result = {func.name}({args})"
            return f"result = {func.name}({args})"
    
    def _generate_assert(self, func: FunctionInfo) -> str:
        """Generate assert section for test"""
        if func.returns:
            return f"assert result is not None  # Verify return type: {func.returns}"
        return "assert result is not None  # TODO: Add specific assertions"
    
    def _estimate_coverage(self, module_info: ModuleInfo, test_cases: List[TestCase]) -> float:
        """Estimate test coverage percentage"""
        total_items = len(module_info.functions) + sum(len(c.methods) for c in module_info.classes)
        if total_items == 0:
            return 100.0
        
        tested_functions = set(tc.function_name for tc in test_cases)
        covered = sum(1 for f in module_info.functions if f.name in tested_functions)
        covered += sum(1 for c in module_info.classes for m in c.methods if m.name in tested_functions)
        
        return min(100.0, (covered / total_items) * 100)
    
    def _get_required_imports(self, module_info: ModuleInfo) -> List[str]:
        """Get required imports for test file"""
        imports = []
        
        if self.framework == TestFramework.PYTEST:
            imports.append("import pytest")
        elif self.framework == TestFramework.UNITTEST:
            imports.append("import unittest")
        
        # Add import for the module being tested
        module_name = Path(module_info.path).stem
        imports.append(f"from {module_name} import *")
        
        return imports


class LLMProvider:
    """Base class for LLM providers"""
    
    def __init__(self, api_key: str = None, model: str = None, base_url: str = None):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url
    
    def generate_test(self, func: FunctionInfo, context: str = "") -> str:
        """Generate test using LLM - to be implemented by subclasses"""
        raise NotImplementedError
    
    def analyze_code(self, code: str) -> Dict[str, Any]:
        """Analyze code using LLM - to be implemented by subclasses"""
        raise NotImplementedError


class OpenAIProvider(LLMProvider):
    """OpenAI API provider"""
    
    def __init__(self, api_key: str = None, model: str = "gpt-4"):
        super().__init__(api_key=api_key, model=model, base_url="https://api.openai.com/v1")
    
    def generate_test(self, func: FunctionInfo, context: str = "") -> str:
        """Generate test using OpenAI API"""
        # This is a placeholder - actual implementation would call the API
        prompt = f"""Generate a comprehensive unit test for the following function:

Function: {func.name}
Arguments: {func.args}
Returns: {func.returns}
Docstring: {func.docstring}

Source code:
```python
{func.source_code}
```

Context: {context}

Generate pytest-compatible test cases including:
1. Basic functionality test
2. Edge cases
3. Exception handling
"""
        return f"# TODO: Implement OpenAI-based test generation\n# Prompt: {prompt[:100]}..."


class AnthropicProvider(LLMProvider):
    """Anthropic Claude API provider"""
    
    def __init__(self, api_key: str = None, model: str = "claude-3-opus-20240229"):
        super().__init__(api_key=api_key, model=model, base_url="https://api.anthropic.com/v1")
    
    def generate_test(self, func: FunctionInfo, context: str = "") -> str:
        """Generate test using Anthropic API"""
        # Placeholder implementation
        return f"# TODO: Implement Anthropic-based test generation for {func.name}"


class OllamaProvider(LLMProvider):
    """Ollama local LLM provider"""
    
    def __init__(self, model: str = "llama2", base_url: str = "http://localhost:11434"):
        super().__init__(api_key=None, model=model, base_url=base_url)
    
    def generate_test(self, func: FunctionInfo, context: str = "") -> str:
        """Generate test using Ollama"""
        # Placeholder implementation
        return f"# TODO: Implement Ollama-based test generation for {func.name}"


class TestForge:
    """Main TestForge engine"""
    
    def __init__(self, framework: TestFramework = TestFramework.PYTEST,
                 llm_provider: LLMProvider = None):
        self.analyzer = CodeAnalyzer()
        self.generator = TestGenerator(framework)
        self.llm_provider = llm_provider
        self.framework = framework
    
    def analyze(self, file_path: str) -> ModuleInfo:
        """Analyze a source file"""
        return self.analyzer.analyze_file(file_path)
    
    def generate(self, module_info: ModuleInfo) -> TestSuite:
        """Generate test suite for analyzed module"""
        return self.generator.generate_tests(module_info)
    
    def generate_from_file(self, file_path: str) -> TestSuite:
        """Analyze file and generate tests in one step"""
        module_info = self.analyze(file_path)
        return self.generate(module_info)
    
    def export_tests(self, test_suite: TestSuite, output_path: str = None) -> str:
        """Export test suite to file"""
        if output_path is None:
            # Generate output path based on module path
            module_path = Path(test_suite.module_path)
            output_path = module_path.parent / f"test_{module_path.name}"
        
        # Build test file content
        lines = []
        
        # Add imports
        for imp in test_suite.imports:
            lines.append(imp)
        lines.append("")
        
        # Add module docstring
        lines.append(f'"""')
        lines.append(f"Auto-generated tests for {test_suite.module_path}")
        lines.append(f"Generated by TestForge v{__version__}")
        lines.append(f"Framework: {test_suite.framework.value}")
        lines.append(f"Estimated coverage: {test_suite.coverage_estimate:.1f}%")
        lines.append(f'"""')
        lines.append("")
        
        # Add test cases
        for tc in test_suite.test_cases:
            lines.append(f"# Test: {tc.name}")
            lines.append(f"# Type: {tc.test_type}")
            lines.append(f"# Priority: {tc.priority}")
            lines.append(f"# Tags: {', '.join(tc.tags)}")
            lines.append(tc.test_code)
            lines.append("")
        
        content = '\n'.join(lines)
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return str(output_path)
    
    def get_statistics(self, test_suite: TestSuite) -> Dict[str, Any]:
        """Get statistics about generated tests"""
        return {
            'total_tests': len(test_suite.test_cases),
            'by_type': self._count_by_type(test_suite.test_cases),
            'by_priority': self._count_by_priority(test_suite.test_cases),
            'coverage_estimate': test_suite.coverage_estimate,
            'framework': test_suite.framework.value
        }
    
    def _count_by_type(self, test_cases: List[TestCase]) -> Dict[str, int]:
        """Count tests by type"""
        counts = {}
        for tc in test_cases:
            counts[tc.test_type] = counts.get(tc.test_type, 0) + 1
        return counts
    
    def _count_by_priority(self, test_cases: List[TestCase]) -> Dict[int, int]:
        """Count tests by priority"""
        counts = {}
        for tc in test_cases:
            counts[tc.priority] = counts.get(tc.priority, 0) + 1
        return counts
