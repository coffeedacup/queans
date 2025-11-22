from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas, crud
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/questions/{question_id}/answers", tags=["answers"])

@router.post("/", response_model=schemas.Answer, status_code=status.HTTP_201_CREATED)
def create_answer(question_id: int, answer: schemas.AnswerCreate, db: Session = Depends(get_db)):
    try:
        db_answer = crud.AnswerCRUD.create_answer(db=db, answer=answer, question_id=question_id)
        if db_answer is None:
            raise HTTPException(status_code=404, detail="Question not found")
        return db_answer
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating answer: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{answer_id}", response_model=schemas.Answer)
def read_answer(answer_id: int, db: Session = Depends(get_db)):
    try:
        answer = crud.AnswerCRUD.get_answer(db, answer_id=answer_id)
        if answer is None:
            logger.warning(f"Answer with id={answer_id} not found")
            raise HTTPException(status_code=404, detail="Answer not found")
        return answer
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching answer: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/{answer_id}")
def delete_answer(answer_id: int, db: Session = Depends(get_db)):
    try:
        success = crud.AnswerCRUD.delete_answer(db, answer_id=answer_id)
        if not success:
            raise HTTPException(status_code=404, detail="Answer not found")
        return {"message": "Answer deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting answer: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")