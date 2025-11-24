from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
import uuid
from datetime import datetime

from app.core.database import Base

class Codebase(Base):
    __tablename__ = "codebases"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    version = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class CodeFile(Base):
    __tablename__ = "code_files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    codebase_id = Column(UUID(as_uuid=True), ForeignKey("codebases.id"), nullable=False)
    file_path = Column(String, nullable=False)
    content = Column(Text, nullable=True)
    language = Column(String, nullable=False)
    parsed_at = Column(DateTime, nullable=True)
    
    # NEW: Vector embedding storage
    embedding = Column(JSONB, nullable=True)  # Store vector embeddings
    analysis_result = Column(JSONB, nullable=True)  # Store parsed structure
    
    # NEW: File metadata for better analysis
    size_bytes = Column(Integer, nullable=True)
    line_count = Column(Integer, nullable=True)
    function_count = Column(Integer, nullable=True)
    class_count = Column(Integer, nullable=True)