from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class QuestionBase(BaseModel):
    text: str

class QuestionCreate(QuestionBase):
    pass

class Question(QuestionBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class QuestionWithAnswers(Question):
    answers: List['Answer'] = []

class AnswerBase(BaseModel):
    text: str
    user_id: str

class AnswerCreate(AnswerBase):
    pass

class Answer(AnswerBase):
    id: int
    question_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

QuestionWithAnswers.update_forward_refs()