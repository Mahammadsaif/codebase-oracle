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