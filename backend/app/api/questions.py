from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas
from app.models import DifficultyLevel, QuestionCategory

router = APIRouter()

@router.post("/", response_model=schemas.QuestionResponse)
def create_question(
    *,
    db: Session = Depends(get_db),
    question_in: schemas.QuestionCreate,
):
    """创建新题目"""
    question = crud.create_question(db=db, question=question_in)
    return question

@router.get("/", response_model=schemas.QuestionListResponse)
def read_questions(
    db: Session = Depends(get_db),
    q: str = Query(None, description="搜索关键词"),
    category: QuestionCategory = Query(None, description="题目类别"),
    difficulty: DifficultyLevel = Query(None, description="难度等级"),
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(10, ge=1, le=100, description="每页记录数"),
):
    """获取题目列表（支持搜索和筛选）"""
    # 如果有搜索或筛选条件，使用搜索功能
    if q or category or difficulty:
        params = schemas.QuestionSearchParams(
            q=q,
            category=category,
            difficulty=difficulty,
            page=page,
            size=size
        )
        questions, total = crud.search_questions(db, params)
    else:
        # 无搜索条件时，直接获取所有题目
        skip = (page - 1) * size
        questions = crud.get_questions(db, skip=skip, limit=size)
        total = crud.get_questions_count(db)
    
    return schemas.QuestionListResponse(
        items=questions,
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size
    )

@router.get("/search", response_model=schemas.QuestionListResponse)
def search_questions(
    db: Session = Depends(get_db),
    q: str = Query(None, description="搜索关键词"),
    category: QuestionCategory = Query(None, description="题目类别"),
    difficulty: DifficultyLevel = Query(None, description="难度等级"),
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(10, ge=1, le=100, description="每页记录数"),
):
    """搜索和筛选题目"""
    params = schemas.QuestionSearchParams(
        q=q,
        category=category,
        difficulty=difficulty,
        page=page,
        size=size
    )
    questions, total = crud.search_questions(db, params)
    
    return schemas.QuestionListResponse(
        items=questions,
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size
    )

@router.get("/{question_id}", response_model=schemas.QuestionResponse)
def read_question(
    *,
    db: Session = Depends(get_db),
    question_id: int,
):
    """获取题目详情"""
    question = crud.get_question(db=db, question_id=question_id)
    if not question:
        raise HTTPException(status_code=404, detail="题目不存在")
    return question

@router.put("/{question_id}", response_model=schemas.QuestionResponse)
def update_question(
    *,
    db: Session = Depends(get_db),
    question_id: int,
    question_in: schemas.QuestionUpdate,
):
    """更新题目"""
    question = crud.update_question(db=db, question_id=question_id, question=question_in)
    if not question:
        raise HTTPException(status_code=404, detail="题目不存在")
    return question

@router.delete("/{question_id}", response_model=schemas.QuestionResponse)
def delete_question(
    *,
    db: Session = Depends(get_db),
    question_id: int,
):
    """删除题目"""
    question = crud.get_question(db=db, question_id=question_id)
    if not question:
        raise HTTPException(status_code=404, detail="题目不存在")
    
    crud.delete_question(db=db, question_id=question_id)
    return question