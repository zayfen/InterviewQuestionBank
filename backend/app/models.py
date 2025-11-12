from sqlalchemy import Column, Integer, String, Text, DateTime, Enum
from sqlalchemy.sql import func
from app.database import Base
import enum

class DifficultyLevel(str, enum.Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class QuestionCategory(str, enum.Enum):
    ALGORITHM = "algorithm"
    DATABASE = "database"
    SYSTEM_DESIGN = "system_design"
    FRONTEND = "frontend"
    BACKEND = "backend"
    DEVOPS = "devops"
    MOBILE = "mobile"
    DATA_SCIENCE = "data_science"
    SECURITY = "security"
    TESTING = "testing"
    REACT_NATIVE = "react_native"
    REACT = "react"

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    content = Column(Text, nullable=False)
    category = Column(Enum(QuestionCategory), nullable=False, index=True)
    difficulty = Column(Enum(DifficultyLevel), nullable=False, index=True)
    analysis = Column(Text, nullable=True)
    tags = Column(String(500), nullable=True)  # JSON string of tags
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Question(id={self.id}, title='{self.title}', category={self.category}, difficulty={self.difficulty})>"
