from sqlalchemy.orm import Session
from app import models, schemas
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

class QuestionCRUD:
    @staticmethod
    def get_questions(db: Session, skip: int = 0, limit: int = 100) -> List[models.Question]:
        logger.info(f"Fetching questions with skip={skip}, limit={limit}")
        return db.query(models.Question).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_question(db: Session, question_id: int) -> Optional[models.Question]:
        logger.info(f"Fetching question with id={question_id}")
        return db.query(models.Question).filter(models.Question.id == question_id).first()
    
    @staticmethod
    def create_question(db: Session, question: schemas.QuestionCreate) -> models.Question:
        logger.info("Creating new question")
        db_question = models.Question(text=question.text)
        db.add(db_question)
        db.commit()
        db.refresh(db_question)
        logger.info(f"Question created with id={db_question.id}")
        return db_question
    
    @staticmethod
    def delete_question(db: Session, question_id: int) -> bool:
        logger.info(f"Deleting question with id={question_id}")
        question = db.query(models.Question).filter(models.Question.id == question_id).first()
        if question:
            db.delete(question)
            db.commit()
            logger.info(f"Question with id={question_id} deleted")
            return True
        logger.warning(f"Question with id={question_id} not found for deletion")
        return False

class AnswerCRUD:
    @staticmethod
    def get_answer(db: Session, answer_id: int) -> Optional[models.Answer]:
        logger.info(f"Fetching answer with id={answer_id}")
        return db.query(models.Answer).filter(models.Answer.id == answer_id).first()
    
    @staticmethod
    def create_answer(db: Session, answer: schemas.AnswerCreate, question_id: int) -> Optional[models.Answer]:
        logger.info(f"Creating answer for question_id={question_id}")
        
        # Check if question exists
        question = db.query(models.Question).filter(models.Question.id == question_id).first()
        if not question:
            logger.error(f"Question with id={question_id} not found")
            return None
        
        db_answer = models.Answer(
            text=answer.text,
            user_id=answer.user_id,
            question_id=question_id
        )
        db.add(db_answer)
        db.commit()
        db.refresh(db_answer)
        logger.info(f"Answer created with id={db_answer.id}")
        return db_answer
    
    @staticmethod
    def delete_answer(db: Session, answer_id: int) -> bool:
        logger.info(f"Deleting answer with id={answer_id}")
        answer = db.query(models.Answer).filter(models.Answer.id == answer_id).first()
        if answer:
            db.delete(answer)
            db.commit()
            logger.info(f"Answer with id={answer_id} deleted")
            return True
        logger.warning(f"Answer with id={answer_id} not found for deletion")
        return False
    
    @staticmethod
    def get_answers_by_question(db: Session, question_id: int) -> List[models.Answer]:
        logger.info(f"Fetching answers for question_id={question_id}")
        return db.query(models.Answer).filter(models.Answer.question_id == question_id).all()