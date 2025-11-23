import os
from pathlib import Path
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class CodeParser:
    """Parses code files to extract structure and metadata."""
    
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
    
    def parse_file(self, file_path: str, content: str) -> Dict:
        """Parse a single code file and extract structure."""
        language = self.detect_language(file_path)
        
        if not language:
            logger.warning(f"Unsupported file type: {file_path}")
            return {}
        
        try:
            # Basic structure extraction (we'll enhance this)
            return {
                "file_path": file_path,
                "language": language,
                "size_bytes": len(content.encode('utf-8')),
                "line_count": len(content.splitlines()),
                "has_functions": "def " in content,
                "has_classes": "class " in content,
                "imports": self._extract_imports(content, language)
            }
        except Exception as e:
            logger.error(f"Error parsing {file_path}: {str(e)}")
            return {}
    
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