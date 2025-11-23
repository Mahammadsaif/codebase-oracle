from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
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