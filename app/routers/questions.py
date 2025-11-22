from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import schemas, crud
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/questions", tags=["questions"])

@router.get("/", response_model=List[schemas.Question])
def read_questions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        questions = crud.QuestionCRUD.get_questions(db, skip=skip, limit=limit)
        return questions
    except Exception as e:
        logger.error(f"Error fetching questions: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/", response_model=schemas.Question, status_code=status.HTTP_201_CREATED)
def create_question(question: schemas.QuestionCreate, db: Session = Depends(get_db)):
    try:
        return crud.QuestionCRUD.create_question(db=db, question=question)
    except Exception as e:
        logger.error(f"Error creating question: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{question_id}", response_model=schemas.QuestionWithAnswers)
def read_question(question_id: int, db: Session = Depends(get_db)):
    try:
        question = crud.QuestionCRUD.get_question(db, question_id=question_id)
        if question is None:
            logger.warning(f"Question with id={question_id} not found")
            raise HTTPException(status_code=404, detail="Question not found")
        return question
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching question: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/{question_id}")
def delete_question(question_id: int, db: Session = Depends(get_db)):
    try:
        success = crud.QuestionCRUD.delete_question(db, question_id=question_id)
        if not success:
            raise HTTPException(status_code=404, detail="Question not found")
        return {"message": "Question deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting question: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")