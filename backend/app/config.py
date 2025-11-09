from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./interview_questions.db"
    OPENAI_API_KEY: str = ""
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Interview Question Bank API"
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    class Config:
        env_file = ".env"

settings = Settings()