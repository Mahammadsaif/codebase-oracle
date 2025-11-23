from pydantic import BaseModel, UUID4
from typing import Optional, List
from datetime import datetime

class CodebaseCreate(BaseModel):
    name: str
    version: Optional[str] = None

class CodebaseResponse(BaseModel):
    id: UUID4
    name: str
    version: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class CodeFileResponse(BaseModel):
    id: UUID4
    file_path: str
    language: str
    # REMOVED: line_count - not in database
    parsed_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class CodeFileCreate(BaseModel):
    file_path: str
    content: str
    language: str