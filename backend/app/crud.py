from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import List, Optional
import json

from app.models import Question
from app.schemas import QuestionCreate, QuestionUpdate, QuestionSearchParams

def get_question_by_title(db: Session, title: str) -> Optional[Question]:
    """根据标题查找题目"""
    return db.query(Question).filter(Question.title == title).first()

def create_question(db: Session, question: QuestionCreate) -> Question:
    db_question = Question(
        title=question.title,
        content=question.content,
        category=question.category,
        difficulty=question.difficulty,
        analysis=question.analysis,
        tags=json.dumps(question.tags) if question.tags else None
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

def get_question(db: Session, question_id: int) -> Optional[Question]:
    return db.query(Question).filter(Question.id == question_id).first()

def get_questions(db: Session, skip: int = 0, limit: int = 10) -> List[Question]:
    return db.query(Question).offset(skip).limit(limit).all()

def get_questions_count(db: Session) -> int:
    return db.query(Question).count()

def update_question(db: Session, question_id: int, question: QuestionUpdate) -> Optional[Question]:
    db_question = db.query(Question).filter(Question.id == question_id).first()
    if not db_question:
        return None
    
    update_data = question.dict(exclude_unset=True)
    if "tags" in update_data and update_data["tags"] is not None:
        update_data["tags"] = json.dumps(update_data["tags"])
    
    for field, value in update_data.items():
        setattr(db_question, field, value)
    
    db.commit()
    db.refresh(db_question)
    return db_question

def delete_question(db: Session, question_id: int) -> bool:
    db_question = db.query(Question).filter(Question.id == question_id).first()
    if not db_question:
        return False
    
    db.delete(db_question)
    db.commit()
    return True

def search_questions(db: Session, params: QuestionSearchParams) -> tuple:
    query = db.query(Question)
    
    if params.q:
        search_term = f"%{params.q}%"
        query = query.filter(
            or_(
                Question.title.ilike(search_term),
                Question.content.ilike(search_term),
                Question.analysis.ilike(search_term)
            )
        )
    
    if params.category:
        query = query.filter(Question.category == params.category)
    
    if params.difficulty:
        query = query.filter(Question.difficulty == params.difficulty)
    
    total = query.count()
    questions = query.offset((params.page - 1) * params.size).limit(params.size).all()
    
    return questions, total