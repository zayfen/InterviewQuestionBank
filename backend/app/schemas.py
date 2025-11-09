from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
from app.models import DifficultyLevel, QuestionCategory
import json

class QuestionBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    category: QuestionCategory
    difficulty: DifficultyLevel
    analysis: Optional[str] = None
    tags: Optional[List[str]] = []

class QuestionCreate(QuestionBase):
    pass

class QuestionUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    category: Optional[QuestionCategory] = None
    difficulty: Optional[DifficultyLevel] = None
    analysis: Optional[str] = None
    tags: Optional[List[str]] = []

class QuestionResponse(QuestionBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    @field_validator('tags', mode='before')
    @classmethod
    def parse_tags(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except:
                return []
        return v if v else []
    
    class Config:
        from_attributes = True

class QuestionListResponse(BaseModel):
    items: List[QuestionResponse]
    total: int
    page: int
    size: int
    pages: int

class QuestionSearchParams(BaseModel):
    q: Optional[str] = None
    category: Optional[QuestionCategory] = None
    difficulty: Optional[DifficultyLevel] = None
    page: int = Field(default=1, ge=1)
    size: int = Field(default=10, ge=1, le=100)

class QuestionGenerateRequest(BaseModel):
    category: QuestionCategory
    difficulty: DifficultyLevel
    count: int = Field(..., ge=1, le=10)

class RandomQuestionRequest(BaseModel):
    count: int = Field(..., ge=1, le=50)
    categories: Optional[List[QuestionCategory]] = None
    difficulties: Optional[List[DifficultyLevel]] = None

class InterviewSessionRequest(BaseModel):
    easy_count: int = Field(default=2, ge=0, le=10)
    medium_count: int = Field(default=3, ge=0, le=10)
    hard_count: int = Field(default=1, ge=0, le=10)