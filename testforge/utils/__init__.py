"""
TestForge Utilities Module
"""

import os
import re
from pathlib import Path
from typing import List, Optional


def find_source_files(directory: str, extensions: List[str] = None) -> List[str]:
    """Find source files in a directory"""
    if extensions is None:
        extensions = ['.py', '.js', '.ts', '.go', '.rs', '.java']
    
    files = []
    for ext in extensions:
        files.extend(str(p) for p in Path(directory).rglob(f'*{ext}'))
    return files


def sanitize_name(name: str) -> str:
    """Sanitize a name for use in test function names"""
    # Replace invalid characters with underscores
    sanitized = re.sub(r'[^a-zA-Z0-9_]', '_', name)
    # Remove leading digits
    sanitized = re.sub(r'^[0-9]+', '', sanitized)
    return sanitized.lower()


def calculate_hash(content: str) -> str:
    """Calculate MD5 hash of content"""
    import hashlib
    return hashlib.md5(content.encode()).hexdigest()[:8]


def format_duration(seconds: float) -> str:
    """Format duration in human-readable format"""
    if seconds < 1:
        return f"{seconds * 1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.1f}s"
    else:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}m {secs:.0f}s"


__all__ = ['find_source_files', 'sanitize_name', 'calculate_hash', 'format_duration']
