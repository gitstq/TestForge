"""
TestForge CLI - Command Line Interface
"""

import argparse
import sys
import os
import json
from pathlib import Path
from typing import Optional, List

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from testforge.core import (
    TestForge, CodeAnalyzer, TestGenerator, TestSuite,
    TestFramework, Language, LLMProvider
)
from testforge import __version__


# ANSI color codes
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_banner():
    """Print TestForge banner"""
    banner = f"""
{Colors.CYAN}╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   {Colors.BOLD}{Colors.GREEN}TestForge{Colors.END}{Colors.CYAN} - AI-Powered Test Generation Engine        ║
║                                                               ║
║   {Colors.YELLOW}轻量级AI驱动测试用例智能生成引擎{Colors.END}{Colors.CYAN}                  ║
║                                                               ║
║   Version: {__version__}                                        ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝{Colors.END}
"""
    print(banner)


def print_success(message: str):
    """Print success message"""
    print(f"{Colors.GREEN}✓{Colors.END} {message}")


def print_error(message: str):
    """Print error message"""
    print(f"{Colors.RED}✗{Colors.END} {message}", file=sys.stderr)


def print_info(message: str):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ{Colors.END} {message}")


def print_warning(message: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠{Colors.END} {message}")


def cmd_analyze(args):
    """Analyze source file command"""
    print_banner()
    
    file_path = args.file
    
    if not os.path.exists(file_path):
        print_error(f"File not found: {file_path}")
        return 1
    
    print_info(f"Analyzing: {file_path}")
    
    try:
        analyzer = CodeAnalyzer()
        module_info = analyzer.analyze_file(file_path)
        
        print()
        print(f"{Colors.BOLD}📊 Analysis Results:{Colors.END}")
        print(f"  Language: {module_info.language.value}")
        print(f"  Functions: {len(module_info.functions)}")
        print(f"  Classes: {len(module_info.classes)}")
        print(f"  Imports: {len(module_info.imports)}")
        
        if module_info.functions:
            print()
            print(f"{Colors.BOLD}🔧 Functions:{Colors.END}")
            for func in module_info.functions:
                async_marker = " [async]" if func.is_async else ""
                method_marker = f" ({func.class_name})" if func.is_method else ""
                print(f"  • {func.name}{method_marker}{async_marker}")
                if func.args:
                    print(f"    Args: {', '.join(func.args)}")
                if func.returns:
                    print(f"    Returns: {func.returns}")
                if func.docstring:
                    doc_preview = func.docstring[:50] + "..." if len(func.docstring) > 50 else func.docstring
                    print(f"    Doc: {doc_preview}")
        
        if module_info.classes:
            print()
            print(f"{Colors.BOLD}📦 Classes:{Colors.END}")
            for cls in module_info.classes:
                print(f"  • {cls.name}")
                if cls.bases:
                    print(f"    Extends: {', '.join(cls.bases)}")
                if cls.methods:
                    print(f"    Methods: {', '.join(m.name for m in cls.methods)}")
        
        if args.output:
            output_data = {
                'path': module_info.path,
                'language': module_info.language.value,
                'functions': [
                    {
                        'name': f.name,
                        'args': f.args,
                        'returns': f.returns,
                        'docstring': f.docstring,
                        'is_async': f.is_async,
                        'complexity': f.complexity
                    }
                    for f in module_info.functions
                ],
                'classes': [
                    {
                        'name': c.name,
                        'methods': [m.name for m in c.methods],
                        'attributes': c.attributes,
                        'bases': c.bases
                    }
                    for c in module_info.classes
                ]
            }
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2)
            print_success(f"Analysis saved to: {args.output}")
        
        print_success("Analysis complete!")
        return 0
        
    except Exception as e:
        print_error(f"Analysis failed: {str(e)}")
        return 1


def cmd_generate(args):
    """Generate tests command"""
    print_banner()
    
    file_path = args.file
    
    if not os.path.exists(file_path):
        print_error(f"File not found: {file_path}")
        return 1
    
    # Determine framework
    framework_map = {
        'pytest': TestFramework.PYTEST,
        'unittest': TestFramework.UNITTEST,
        'jest': TestFramework.JEST,
        'junit': TestFramework.JUNIT,
        'go': TestFramework.GO_TEST,
        'rust': TestFramework.RUST,
    }
    framework = framework_map.get(args.framework, TestFramework.PYTEST)
    
    print_info(f"Framework: {framework.value}")
    print_info(f"Source: {file_path}")
    
    try:
        forge = TestForge(framework=framework)
        
        # Analyze
        print_info("Analyzing source code...")
        module_info = forge.analyze(file_path)
        
        # Generate
        print_info("Generating test cases...")
        test_suite = forge.generate(module_info)
        
        # Get statistics
        stats = forge.get_statistics(test_suite)
        
        print()
        print(f"{Colors.BOLD}📈 Generation Statistics:{Colors.END}")
        print(f"  Total tests: {stats['total_tests']}")
        print(f"  Estimated coverage: {stats['coverage_estimate']:.1f}%")
        print()
        print(f"  By type:")
        for test_type, count in stats['by_type'].items():
            print(f"    • {test_type}: {count}")
        
        # Determine output path
        if args.output:
            output_path = args.output
        else:
            module_path = Path(file_path)
            output_path = module_path.parent / f"test_{module_path.name}"
        
        # Export
        forge.export_tests(test_suite, output_path)
        print_success(f"Tests generated: {output_path}")
        
        return 0
        
    except Exception as e:
        print_error(f"Generation failed: {str(e)}")
        import traceback
        if args.verbose:
            traceback.print_exc()
        return 1


def cmd_batch(args):
    """Batch process multiple files"""
    print_banner()
    
    path = Path(args.path)
    
    if not path.exists():
        print_error(f"Path not found: {path}")
        return 1
    
    # Find source files
    extensions = ['.py', '.js', '.ts', '.go', '.rs', '.java']
    if args.extension:
        extensions = [args.extension]
    
    files = []
    if path.is_file():
        files = [path]
    else:
        for ext in extensions:
            files.extend(path.rglob(f'*{ext}'))
    
    if not files:
        print_warning("No source files found")
        return 0
    
    print_info(f"Found {len(files)} source file(s)")
    
    framework_map = {
        'pytest': TestFramework.PYTEST,
        'unittest': TestFramework.UNITTEST,
        'jest': TestFramework.JEST,
    }
    framework = framework_map.get(args.framework, TestFramework.PYTEST)
    
    forge = TestForge(framework=framework)
    success_count = 0
    
    for file_path in files:
        try:
            print_info(f"Processing: {file_path}")
            test_suite = forge.generate_from_file(str(file_path))
            
            output_path = Path(file_path).parent / f"test_{Path(file_path).name}"
            forge.export_tests(test_suite, str(output_path))
            success_count += 1
            print_success(f"Generated: {output_path}")
        except Exception as e:
            print_error(f"Failed: {file_path} - {str(e)}")
    
    print()
    print(f"{Colors.BOLD}📊 Batch Summary:{Colors.END}")
    print(f"  Processed: {success_count}/{len(files)}")
    
    return 0 if success_count == len(files) else 1


def cmd_stats(args):
    """Show statistics for generated tests"""
    print_banner()
    
    test_file = args.file
    
    if not os.path.exists(test_file):
        print_error(f"File not found: {test_file}")
        return 1
    
    # Simple analysis of test file
    with open(test_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    test_count = content.count('def test_') + content.count('test(') + content.count('func Test')
    
    print(f"{Colors.BOLD}📊 Test File Statistics:{Colors.END}")
    print(f"  File: {test_file}")
    print(f"  Estimated tests: {test_count}")
    print(f"  Lines: {len(content.splitlines())}")
    
    return 0


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        prog='testforge',
        description='TestForge - AI-Powered Test Case Intelligent Generation Engine CLI'
    )
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {__version__}')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze source code structure')
    analyze_parser.add_argument('file', help='Source file to analyze')
    analyze_parser.add_argument('-o', '--output', help='Output JSON file for analysis results')
    analyze_parser.set_defaults(func=cmd_analyze)
    
    # Generate command
    generate_parser = subparsers.add_parser('generate', help='Generate test cases')
    generate_parser.add_argument('file', help='Source file to generate tests for')
    generate_parser.add_argument('-f', '--framework', default='pytest',
                                  choices=['pytest', 'unittest', 'jest', 'junit', 'go', 'rust'],
                                  help='Test framework to use')
    generate_parser.add_argument('-o', '--output', help='Output test file path')
    generate_parser.add_argument('--verbose', action='store_true', help='Verbose output')
    generate_parser.set_defaults(func=cmd_generate)
    
    # Batch command
    batch_parser = subparsers.add_parser('batch', help='Batch process multiple files')
    batch_parser.add_argument('path', help='Directory or file to process')
    batch_parser.add_argument('-f', '--framework', default='pytest',
                               choices=['pytest', 'unittest', 'jest'],
                               help='Test framework to use')
    batch_parser.add_argument('-e', '--extension', help='File extension to process')
    batch_parser.set_defaults(func=cmd_batch)
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show test statistics')
    stats_parser.add_argument('file', help='Test file to analyze')
    stats_parser.set_defaults(func=cmd_stats)
    
    args = parser.parse_args()
    
    if args.command is None:
        print_banner()
        parser.print_help()
        return 0
    
    return args.func(args)


if __name__ == '__main__':
    sys.exit(main())
