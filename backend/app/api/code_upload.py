from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
import shutil
import os
from pathlib import Path
from typing import List

from app.core.database import get_db
from app.schemas.code_analysis import Codebase, CodeFile
from app.models.code_analysis import CodebaseCreate, CodebaseResponse
from app.services.mcp_parser import MCPParser  # CHANGED: Import MCP parser

router = APIRouter()
mcp_parser = MCPParser()  # CHANGED: Use MCP parser instead of basic parser

@router.post("/codebases/", response_model=CodebaseResponse)
async def create_codebase(
    codebase_data: CodebaseCreate,
    db: Session = Depends(get_db)
):
    """Create a new codebase entry."""
    try:
        db_codebase = Codebase(
            name=codebase_data.name,
            version=codebase_data.version
        )
        db.add(db_codebase)
        db.commit()
        db.refresh(db_codebase)
        return db_codebase
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/codebases/{codebase_id}/upload")
async def upload_code_files(
    codebase_id: str,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    """Upload and parse multiple code files with MCP analysis."""
    try:
        # Verify codebase exists
        codebase = db.query(Codebase).filter(Codebase.id == codebase_id).first()
        if not codebase:
            raise HTTPException(status_code=404, detail="Codebase not found")
        
        processed_files = []
        
        for file in files:
            # Read file content
            content = await file.read()
            content_str = content.decode('utf-8')
            
            # ENHANCED: Use MCP parser for professional analysis
            parsed_data = mcp_parser.parse_code(content_str, file.filename)  # CHANGED: Use MCP parser
            
            # Calculate additional metrics
            function_count = len(parsed_data.get('functions', []))
            class_count = len(parsed_data.get('classes', []))
            import_count = len(parsed_data.get('imports', []))
            
            # Save to database with enhanced fields
            db_file = CodeFile(
                codebase_id=codebase_id,
                file_path=file.filename,
                content=content_str,
                language=parsed_data.get('language', 'unknown'),
                # Store MCP analysis results
                analysis_result=parsed_data,  # CHANGED: Store full MCP analysis
                size_bytes=len(content_str.encode('utf-8')),
                line_count=len(content_str.splitlines()),
                function_count=function_count,
                class_count=class_count
            )
            db.add(db_file)
            processed_files.append({
                "filename": file.filename,
                "language": parsed_data.get('language'),
                "functions": parsed_data.get('functions', []),
                "classes": parsed_data.get('classes', []),
                "imports": parsed_data.get('imports', []),
                "parser": parsed_data.get('parser', 'unknown')
            })
        
        db.commit()
        return {"message": f"Processed {len(processed_files)} files", "files": processed_files}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))