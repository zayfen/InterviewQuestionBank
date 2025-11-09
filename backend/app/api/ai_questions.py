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
        
        # 保存生成的题目到数据库，跳过重复标题
        saved_questions = []
        skipped_titles = []
        
        for question_data in questions_data:
            # 检查标题是否已存在
            existing_question = crud.get_question_by_title(db=db, title=question_data.title)
            if existing_question:
                skipped_titles.append(question_data.title)
                continue
            
            # 保存新题目
            question = crud.create_question(db=db, question=question_data)
            saved_questions.append(question)
        
        # 如果有跳过的题目，记录日志
        if skipped_titles:
            import logging
            logger = logging.getLogger(__name__)
            logger.info(f"AI生成题目去重: 跳过了 {len(skipped_titles)} 个重复标题: {skipped_titles}")
        
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