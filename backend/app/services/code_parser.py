import os
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging
import re

logger = logging.getLogger(__name__)

class CodeParser:
    """Enhanced code parser for AI analysis."""
    
    def __init__(self):
        self.supported_languages = {
            '.py': 'python',
            '.js': 'javascript', 
            '.ts': 'typescript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.go': 'go'
        }
    
    def detect_language(self, file_path: str) -> Optional[str]:
        """Detect programming language from file extension."""
        extension = Path(file_path).suffix.lower()
        return self.supported_languages.get(extension)
    
    def parse_file(self, file_path: str, content: str) -> Dict[str, Any]:
        """Parse a single code file and extract detailed structure."""
        language = self.detect_language(file_path)
        
        if not language:
            logger.warning(f"Unsupported file type: {file_path}")
            return {}
        
        try:
            # Enhanced parsing based on language
            if language == 'python':
                analysis = self._parse_python(content)
            elif language in ['javascript', 'typescript']:
                analysis = self._parse_javascript(content)
            else:
                analysis = self._parse_generic(content)
            
            return {
                "file_path": file_path,
                "language": language,
                "size_bytes": len(content.encode('utf-8')),
                "line_count": len(content.splitlines()),
                **analysis  # Merge language-specific analysis
            }
        except Exception as e:
            logger.error(f"Error parsing {file_path}: {str(e)}")
            return {}
    
    def _parse_python(self, content: str) -> Dict[str, Any]:
        """Parse Python-specific code structure."""
        lines = content.splitlines()
        
        # Extract functions using regex (basic approach)
        function_pattern = r'def\s+(\w+)\s*\('
        functions = re.findall(function_pattern, content)
        
        # Extract classes
        class_pattern = r'class\s+(\w+)'
        classes = re.findall(class_pattern, content)
        
        # Extract imports
        imports = []
        for line in lines:
            line = line.strip()
            if line.startswith(('import ', 'from ')):
                imports.append(line)
        
        return {
            "functions": functions,
            "classes": classes,
            "imports": imports,
            "function_count": len(functions),
            "class_count": len(classes),
            "import_count": len(imports),
            "analysis_result": {
                "functions": [{"name": fn, "type": "function"} for fn in functions],
                "classes": [{"name": cls, "type": "class"} for cls in classes],
                "imports": imports
            }
        }
    
    def _parse_javascript(self, content: str) -> Dict[str, Any]:
        """Parse JavaScript/TypeScript code structure."""
        # Extract functions
        function_pattern = r'function\s+(\w+)|const\s+(\w+)\s*=\s*\([^)]*\)\s*=>|(\w+)\s*\([^)]*\)\s*\{'
        matches = re.findall(function_pattern, content)
        functions = [m[0] or m[1] or m[2] for m in matches if any(m)]
        
        # Extract imports
        imports = []
        for line in content.splitlines():
            if 'import' in line or 'require(' in line:
                imports.append(line.strip())
        
        return {
            "functions": functions,
            "classes": [],  # JS classes need different parsing
            "imports": imports,
            "function_count": len(functions),
            "class_count": 0,
            "import_count": len(imports),
            "analysis_result": {
                "functions": [{"name": fn, "type": "function"} for fn in functions],
                "imports": imports
            }
        }
    
    def _parse_generic(self, content: str) -> Dict[str, Any]:
        """Generic parser for other languages."""
        return {
            "functions": [],
            "classes": [],
            "imports": [],
            "function_count": 0,
            "class_count": 0,
            "import_count": 0,
            "analysis_result": {}
        }
    
    def _extract_imports(self, content: str, language: str) -> List[str]:
        """Extract import statements from code."""
        imports = []
        lines = content.splitlines()
        
        for line in lines:
            line = line.strip()
            if language == 'python' and line.startswith(('import ', 'from ')):
                imports.append(line)
            elif language in ['javascript', 'typescript'] and 'import' in line:
                imports.append(line)
                
        return imports