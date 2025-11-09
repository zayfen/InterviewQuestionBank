import random
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app import crud, schemas
from app.models import Question, DifficultyLevel, QuestionCategory

router = APIRouter()

@router.get("/", response_model=List[schemas.QuestionResponse])
def get_random_questions(
    *,
    db: Session = Depends(get_db),
    count: int = Query(..., ge=1, le=50, description="题目数量"),
    categories: List[QuestionCategory] = Query(None, description="题目类别筛选"),
    difficulties: List[DifficultyLevel] = Query(None, description="难度等级筛选"),
):
    """随机获取题目"""
    
    # 构建查询
    query = db.query(Question)
    
    if categories:
        query = query.filter(Question.category.in_(categories))
    
    if difficulties:
        query = query.filter(Question.difficulty.in_(difficulties))
    
    # 获取符合条件的所有题目ID
    question_ids = query.with_entities(Question.id).all()
    question_ids = [id[0] for id in question_ids]
    
    if not question_ids:
        raise HTTPException(status_code=404, detail="没有找到符合条件的题目")
    
    # 随机选择题目
    if count >= len(question_ids):
        selected_ids = question_ids
    else:
        selected_ids = random.sample(question_ids, count)
    
    # 获取选中的题目详情
    questions = db.query(Question).filter(Question.id.in_(selected_ids)).all()
    
    # 随机打乱顺序
    random.shuffle(questions)
    
    return questions

@router.post("/advanced", response_model=schemas.QuestionListResponse)
def get_advanced_random_questions(
    *,
    db: Session = Depends(get_db),
    request: schemas.RandomQuestionRequest,
):
    """高级随机选题功能"""
    
    # 构建查询
    query = db.query(Question)
    
    if request.categories:
        query = query.filter(Question.category.in_(request.categories))
    
    if request.difficulties:
        query = query.filter(Question.difficulty.in_(request.difficulties))
    
    # 获取符合条件的所有题目
    all_questions = query.all()
    
    if not all_questions:
        raise HTTPException(status_code=404, detail="没有找到符合条件的题目")
    
    # 随机选择题目
    if request.count >= len(all_questions):
        selected_questions = all_questions
    else:
        selected_questions = random.sample(all_questions, request.count)
    
    # 随机打乱顺序
    random.shuffle(selected_questions)
    
    return schemas.QuestionListResponse(
        items=selected_questions,
        total=len(selected_questions),
        page=1,
        size=len(selected_questions),
        pages=1
    )