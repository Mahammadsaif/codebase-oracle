import logging
from typing import Dict, List, Any
import re

logger = logging.getLogger(__name__)

class MCPParser:
    """Simple multi-language parser that actually works."""
    
    def parse_code(self, content: str, file_path: str) -> Dict[str, Any]:
        """Parse any code file based on its extension."""
        language = self._detect_language(file_path)
        
        if language == 'python':
            return self._parse_python(content)
        elif language == 'javascript':
            return self._parse_javascript(content)
        else:
            return self._parse_generic(content, language)
    
    def _detect_language(self, file_path: str) -> str:
        """Detect language from file extension."""
        extensions = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript', 
            '.java': 'java',
            '.cpp': 'cpp'
        }
        
        for ext, lang in extensions.items():
            if file_path.endswith(ext):
                return lang
        return 'unknown'
    
    def _parse_python(self, content: str) -> Dict[str, Any]:
        """Parse Python code - SIMPLE VERSION."""
        functions = []
        classes = []
        imports = []
        
        # Find functions
        function_matches = re.findall(r'def\s+(\w+)\(([^)]*)\)', content)
        for func_name, params in function_matches:
            functions.append({
                "name": func_name,
                "parameters": params.split(',') if params else [],
                "language": "python"
            })
        
        # Find classes
        class_matches = re.findall(r'class\s+(\w+)', content)
        for class_name in class_matches:
            classes.append({
                "name": class_name,
                "language": "python"
            })
        
        # Find imports
        import_matches = re.findall(r'(import\s+[^\n]+|from\s+[^\n]+\s+import\s+[^\n]+)', content)
        imports.extend(import_matches)
        
        return {
            "functions": functions,
            "classes": classes, 
            "imports": imports,
            "language": "python",
            "parser": "mcp-simple"
        }
    
    def _parse_javascript(self, content: str) -> Dict[str, Any]:
        """Parse JavaScript code - SIMPLE VERSION."""
        functions = []
        classes = []
        imports = []
        
        # Find functions
        function_patterns = [
            r'function\s+(\w+)\s*\(',
            r'const\s+(\w+)\s*=\s*\([^)]*\)\s*=>',
            r'let\s+(\w+)\s*=\s*\([^)]*\)\s*=>'
        ]
        
        for pattern in function_patterns:
            matches = re.findall(pattern, content)
            for func_name in matches:
                functions.append({
                    "name": func_name,
                    "language": "javascript"
                })
        
        # Find classes
        class_matches = re.findall(r'class\s+(\w+)', content)
        for class_name in class_matches:
            classes.append({
                "name": class_name,
                "language": "javascript" 
            })
        
        # Find imports
        import_matches = re.findall(r'import\s+[^;]+', content)
        imports.extend(import_matches)
        
        return {
            "functions": functions,
            "classes": classes,
            "imports": imports,
            "language": "javascript",
            "parser": "mcp-simple"
        }
    
    def _parse_generic(self, content: str, language: str) -> Dict[str, Any]:
        """Generic parser for other languages."""
        return {
            "functions": [],
            "classes": [],
            "imports": [],
            "language": language,
            "parser": "mcp-generic"
        }