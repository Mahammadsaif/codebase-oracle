from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
import shutil
import os
from pathlib import Path
from typing import List

from app.core.database import get_db
from app.schemas.code_analysis import Codebase, CodeFile
from app.models.code_analysis import CodebaseCreate, CodebaseResponse
from app.services.code_parser import CodeParser

router = APIRouter()
code_parser = CodeParser()

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
    """Upload and parse multiple code files."""
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
            
            # Parse file
            parsed_data = code_parser.parse_file(file.filename, content_str)
            
            # Save to database
            db_file = CodeFile(
                codebase_id=codebase_id,
                file_path=file.filename,
                content=content_str,
                language=parsed_data.get('language', 'unknown')
            )
            db.add(db_file)
            processed_files.append({
                "filename": file.filename,
                "language": parsed_data.get('language'),
                "line_count": parsed_data.get('line_count', 0)
            })
        
        db.commit()
        return {"message": f"Processed {len(processed_files)} files", "files": processed_files}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))