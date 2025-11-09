import random
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import schemas
from app.models import Question, DifficultyLevel

router = APIRouter()

@router.post("/", response_model=schemas.QuestionListResponse)
def create_interview_session(
    *,
    db: Session = Depends(get_db),
    request: schemas.InterviewSessionRequest,
):
    """创建面试会话，按难度梯度返回题目"""
    
    total_questions = request.easy_count + request.medium_count + request.hard_count
    
    if total_questions == 0:
        raise HTTPException(status_code=400, detail="题目总数不能为0")
    
    # 按难度分别获取题目
    interview_questions = []
    
    # 获取简单题目
    if request.easy_count > 0:
        easy_questions = db.query(Question).filter(
            Question.difficulty == DifficultyLevel.EASY
        ).all()
        if easy_questions:
            easy_selected = random.sample(
                easy_questions, 
                min(request.easy_count, len(easy_questions))
            )
            interview_questions.extend(easy_selected)
    
    # 获取中等题目
    if request.medium_count > 0:
        medium_questions = db.query(Question).filter(
            Question.difficulty == DifficultyLevel.MEDIUM
        ).all()
        if medium_questions:
            medium_selected = random.sample(
                medium_questions, 
                min(request.medium_count, len(medium_questions))
            )
            interview_questions.extend(medium_selected)
    
    # 获取困难题目
    if request.hard_count > 0:
        hard_questions = db.query(Question).filter(
            Question.difficulty == DifficultyLevel.HARD
        ).all()
        if hard_questions:
            hard_selected = random.sample(
                hard_questions, 
                min(request.hard_count, len(hard_questions))
            )
            interview_questions.extend(hard_selected)
    
    if not interview_questions:
        raise HTTPException(status_code=404, detail="没有找到符合条件的题目")
    
    # 按难度排序（简单 -> 中等 -> 困难）
    difficulty_order = {
        DifficultyLevel.EASY: 1,
        DifficultyLevel.MEDIUM: 2,
        DifficultyLevel.HARD: 3
    }
    
    interview_questions.sort(key=lambda q: difficulty_order[q.difficulty])
    
    return schemas.QuestionListResponse(
        items=interview_questions,
        total=len(interview_questions),
        page=1,
        size=len(interview_questions),
        pages=1
    )

@router.get("/preset/{preset_type}", response_model=schemas.QuestionListResponse)
def get_preset_interview(
    *,
    db: Session = Depends(get_db),
    preset_type: str,
):
    """获取预设的面试模式"""
    
    presets = {
        "quick": {"easy": 2, "medium": 2, "hard": 1},
        "standard": {"easy": 3, "medium": 4, "hard": 2},
        "comprehensive": {"easy": 5, "medium": 5, "hard": 3},
        "frontend": {"easy": 2, "medium": 3, "hard": 1},
        "backend": {"easy": 2, "medium": 3, "hard": 2},
        "algorithm": {"easy": 1, "medium": 2, "hard": 2}
    }
    
    if preset_type not in presets:
        raise HTTPException(status_code=400, detail="不支持的预设类型")
    
    preset = presets[preset_type]
    request = schemas.InterviewSessionRequest(
        easy_count=preset["easy"],
        medium_count=preset["medium"],
        hard_count=preset["hard"]
    )
    
    # 重用创建面试会话的逻辑
    total_questions = request.easy_count + request.medium_count + request.hard_count
    
    interview_questions = []
    
    # 获取简单题目
    if request.easy_count > 0:
        easy_questions = db.query(Question).filter(
            Question.difficulty == DifficultyLevel.EASY
        ).all()
        if easy_questions:
            easy_selected = random.sample(
                easy_questions, 
                min(request.easy_count, len(easy_questions))
            )
            interview_questions.extend(easy_selected)
    
    # 获取中等题目
    if request.medium_count > 0:
        medium_questions = db.query(Question).filter(
            Question.difficulty == DifficultyLevel.MEDIUM
        ).all()
        if medium_questions:
            medium_selected = random.sample(
                medium_questions, 
                min(request.medium_count, len(medium_questions))
            )
            interview_questions.extend(medium_selected)
    
    # 获取困难题目
    if request.hard_count > 0:
        hard_questions = db.query(Question).filter(
            Question.difficulty == DifficultyLevel.HARD
        ).all()
        if hard_questions:
            hard_selected = random.sample(
                hard_questions, 
                min(request.hard_count, len(hard_questions))
            )
            interview_questions.extend(hard_selected)
    
    if not interview_questions:
        raise HTTPException(status_code=404, detail="没有找到符合条件的题目")
    
    # 按难度排序
    difficulty_order = {
        DifficultyLevel.EASY: 1,
        DifficultyLevel.MEDIUM: 2,
        DifficultyLevel.HARD: 3
    }
    
    interview_questions.sort(key=lambda q: difficulty_order[q.difficulty])
    
    return schemas.QuestionListResponse(
        items=interview_questions,
        total=len(interview_questions),
        page=1,
        size=len(interview_questions),
        pages=1
    )