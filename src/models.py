from enum import Enum
from pydantic import BaseModel, Field, model_validator
from typing import Optional, List
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CategoryEnum(str, Enum):
    """Enum for categorizing questions."""
    TECHNICAL = "Technical"
    GENERAL = "General"
    TROUBLESHOOTING = "Troubleshooting"
    OTHER = "Other"

    @classmethod
    def validate_category(cls, category: str) -> str:
        """Validate and return a valid category."""
        try:
            return cls(category).value
        except ValueError:
            logger.warning(f"Invalid category '{category}', defaulting to 'Other'")
            return cls.OTHER.value

class QuestionBase(BaseModel):
    """Base model for question data."""
    text: str = Field(..., description="The question text.")
    category: str = Field(..., description="The category of the question.")

    @model_validator(mode='validate')
    def validate_category(self) -> None:
        """Validate the category against the CategoryEnum."""
        try:
            CategoryEnum(self.category)
        except ValueError:
            logger.warning(f"Invalid category '{self.category}', defaulting to 'Other'")
            self.category = CategoryEnum.OTHER.value
        return self

class QuestionCreate(QuestionBase):
    """Model for creating a new question."""
    pass

class QuestionInDB(QuestionBase):
    """Model for question data stored in the database."""
    id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class AnswerBase(BaseModel):
    """Base model for answer data."""
    answer_text: str = Field(..., description="The answer text.")
    source: str = Field(..., description="The source of the answer.")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence score between 0 and 1.")

class AnswerCreate(AnswerBase):
    """Model for creating a new answer."""
    pass

def sanitize_input(text: str) -> str:
    """Sanitize input text by removing special characters and trimming whitespace."""
    try:
        sanitized = text.replace('\n', ' ').strip()
        logger.info(f"Sanitized input: {sanitized}")
        return sanitized
    except Exception as e:
        logger.error(f"Error sanitizing input: {e}")
        return text

def validate_category(category: str) -> str:
    """Validate category against the CategoryEnum."""
    try:
        return CategoryEnum(category).value
    except ValueError:
        logger.warning(f"Invalid category '{category}', defaulting to 'Other'")
        return CategoryEnum.OTHER.value