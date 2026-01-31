import logging
import re
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, validator
from fastapi import HTTPException

logging.basicConfig(level=logging.INFO)

class QuestionValidator:
    """Utility class for validating user questions in the Q&A portal."""
    
    def __init__(self):
        """Initialize the validator with default prohibited words and technical keywords."""
        self.prohibited_words = {'spam', 'illegal', 'malware'}
        self.technical_keywords = {'how', 'why', 'what', 'explain', 'steps', 'guide'}
    
    @validator('question')
    def validate_question(self, value: str) -> str:
        """
        Validate that the question meets the portal's requirements.
        
        Args:
            value: The user's question to validate
            
        Returns:
            str: Validated question
            
        Raises:
            ValueError: If question is empty or contains prohibited content
        """
        try:
            if not value.strip():
                raise ValueError("Question cannot be empty")
                
            if any(word in value.lower() for word in self.prohibited_words):
                raise ValueError("Question contains prohibited content")
                
            if not any(word in value.lower() for word in self.technical_keywords):
                logging.warning("Question may not be technical enough: %s", value)
                
            return value
        except Exception as e:
            logging.error("Validation error: %s", e)
            raise HTTPException(status_code=400, detail=str(e))

class DocumentationHelper:
    """Utility class for handling documentation links and formatting."""
    
    def __init__(self):
        """Initialize with default documentation categories and links."""
        self.documentation_links = {
            'python': 'https://docs.python.org/3/',
            'machine-learning': 'https://machinelearning.com/',
            'api': 'https://api-reference.example.com/'
        }
    
    def get_documentation_links(self, category: str) -> List[Dict[str, str]]:
        """
        Get relevant documentation links based on question category.
        
        Args:
            category: The category of the question (e.g., 'python')
            
        Returns:
            List[Dict]: List of documentation links with titles and URLs
            
        Raises:
            ValueError: If category is not recognized
        """
        try:
            if category not in self.documentation_links:
                raise ValueError(f"Category '{category}' not found in documentation links")
                
            return [{
                'title': f"Documentation for {category}",
                'url': self.documentation_links[category]
            }]
        except Exception as e:
            logging.error("Error retrieving documentation links: %s", e)
            return []

def sanitize_input(text: Union[str, None]) -> str:
    """
    Sanitize user input by removing HTML tags and special characters.
    
    Args:
        text: The text to sanitize
        
    Returns:
        str: Sanitized text
        
    Raises:
        ValueError: If input is not a string
    """
    try:
        if text is None:
            return ""
            
        if not isinstance(text, str):
            raise ValueError("Input must be a string")
            
        # Remove HTML tags and special characters
        sanitized = re.sub(r'<[^>]+>', '', text)
        sanitized = re.sub(r'[^\w\s\-\.\,\!\?\;\:\(\)\{\}\[\]]', '', sanitized)
        return sanitized.strip()
    except Exception as e:
        logging.error("Error sanitizing input: %s", e)
        return ""

def format_response(content: str, category: str) -> Dict[str, Any]:
    """
    Format the response with category information and documentation links.
    
    Args:
        content: The main content of the response
        category: The category of the question (e.g., 'python')
        
    Returns:
        Dict: Formatted response with content, category, and documentation links
    """
    try:
        validator = QuestionValidator()
        doc_helper = DocumentationHelper()
        
        # Validate category to ensure it's recognized
        validator.validate_question(category)
        
        return {
            'content': content,
            'category': category,
            'documentation': doc_helper.get_documentation_links(category)
        }
    except Exception as e:
        logging.error("Error formatting response: %s", e)
        return {
            'content': content,
            'category': 'unknown',
            'documentation': []
        }