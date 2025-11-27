from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.code_analysis import Codebase, CodeFile
from app.models.code_analysis import CodebaseResponse, CodeFileResponse

router = APIRouter()

@router.get("/codebases/", response_model=list[CodebaseResponse])
def list_codebases(db: Session = Depends(get_db)):
    """Get all codebases."""
    return db.query(Codebase).all()

@router.get("/codebases/{codebase_id}/files", response_model=list[CodeFileResponse])
def get_codebase_files(codebase_id: str, db: Session = Depends(get_db)):
    """Get all files in a codebase."""
    codebase = db.query(Codebase).filter(Codebase.id == codebase_id).first()
    if not codebase:
        raise HTTPException(status_code=404, detail="Codebase not found")
    
    return db.query(CodeFile).filter(CodeFile.codebase_id == codebase_id).all()

#API dashboard analytics endpoint
@router.get("/codebases/{codebase_id}/analysis")
def get_codebase_analysis(codebase_id: str, db: Session = Depends(get_db)):
    """Get detailed analysis of a codebase."""
    files = db.query(CodeFile).filter(CodeFile.codebase_id == codebase_id).all()
    
    analysis = {
        "total_files": len(files),
        "total_functions": sum(f.function_count or 0 for f in files),
        "total_classes": sum(f.class_count or 0 for f in files),
        "languages": {},
        "files": []
    }
    
    for file in files:
        analysis["languages"][file.language] = analysis["languages"].get(file.language, 0) + 1
        analysis["files"].append({
            "path": file.file_path,
            "functions": file.analysis_result.get('functions', []) if file.analysis_result else [],
            "classes": file.analysis_result.get('classes', []) if file.analysis_result else []
        })
    
    return analysis