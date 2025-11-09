from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas
from app.services.ai_service import ai_service
from app.models import DifficultyLevel, QuestionCategory

router = APIRouter()

@router.post("/generate", response_model=List[schemas.QuestionResponse])
def generate_questions(
    *,
    db: Session = Depends(get_db),
    request: schemas.QuestionGenerateRequest,
):
    """使用AI生成题目"""
    try:
        # 调用AI服务生成题目
        questions_data = ai_service.generate_questions(
            category=request.category,
            difficulty=request.difficulty,
            count=request.count
        )
        
        # 保存生成的题目到数据库
        saved_questions = []
        for question_data in questions_data:
            question = crud.create_question(db=db, question=question_data)
            saved_questions.append(question)
        
        return saved_questions
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成题目失败: {str(e)}")

@router.get("/categories", response_model=List[str])
def get_categories():
    """获取所有题目类别"""
    return [category.value for category in QuestionCategory]

@router.get("/difficulties", response_model=List[str])
def get_difficulties():
    """获取所有难度等级"""
    return [difficulty.value for difficulty in DifficultyLevel]