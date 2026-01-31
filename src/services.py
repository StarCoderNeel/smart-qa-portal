import logging
from typing import Optional, Dict, List
from pydantic import BaseModel, ValidationError
from fastapi import HTTPException

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QuestionModel(BaseModel):
    """Pydantic model for incoming question data"""
    question: str
    user_id: Optional[str] = None

class ResponseModel(BaseModel):
    """Pydantic model for structured response data"""
    category: str
    answer: str
    documentation_links: List[str]
    troubleshooting_steps: List[str]

class ModelService:
    """Service class for interacting with machine learning models"""
    
    def __init__(self):
        self.model_loaded = False
        self.model_name = "qa_categorizer_v1"
    
    def load_model(self) -> None:
        """Simulate model loading process"""
        try:
            # In production, this would load an actual model
            self.model_loaded = True
            logger.info(f"Model {self.model_name} loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load model {self.model_name}: {str(e)}")
            raise
    
    def categorize_question(self, question: str) -> str:
        """Categorize a question using the loaded model"""
        if not self.model_loaded:
            raise HTTPException(status_code=503, detail="Model not available")
        
        if not question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        # Simulate model inference
        categories = ["networking", "security", "storage", "virtualization"]
        return categories[int(len(question) % len(categories))]

class QuestionProcessor:
    """Main service class for processing questions"""
    
    def __init__(self, model_service: ModelService):
        self.model_service = model_service
    
    def process_question(self, question_data: QuestionModel) -> ResponseModel:
        """
        Main entry point for processing a question
        
        Args:
            question_data: Pydantic model containing question and user ID
            
        Returns:
            ResponseModel with structured answer data
            
        Raises:
            HTTPException for validation errors or model unavailability
        """
        try:
            # Validate input data
            if not question_data.question.strip():
                raise HTTPException(status_code=400, detail="Question cannot be empty")
            
            logger.info(f"Processing question: {question_data.question[:50]}...")
            
            # Categorize the question
            category = self.model_service.categorize_question(question_data.question)
            
            # Generate documentation links (simulated)
            documentation_links = self._generate_documentation_links(category)
            
            # Generate troubleshooting steps (simulated)
            troubleshooting_steps = self._generate_troubleshooting_steps(category)
            
            # Construct response
            return ResponseModel(
                category=category,
                answer=self._generate_answer(category),
                documentation_links=documentation_links,
                troubleshooting_steps=troubleshooting_steps
            )
        except ValidationError as ve:
            logger.error(f"Validation error: {str(ve)}")
            raise HTTPException(status_code=400, detail=str(ve))
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")
    
    def _generate_answer(self, category: str) -> str:
        """Generate a sample answer based on the question category"""
        answers = {
            "networking": "For networking issues, check router settings and firewall rules.",
            "security": "Security problems often require reviewing access controls and encryption protocols.",
            "storage": "Storage issues may involve disk space management or RAID configuration.",
            "virtualization": "Virtualization problems typically relate to resource allocation or hypervisor settings."
        }
        return answers.get(category, "No specific guidance available for this category")
    
    def _generate_documentation_links(self, category: str) -> List[str]:
        """Generate sample documentation links based on category"""
        links = {
            "networking": [
                "https://docs.example.com/networking-guide",
                "https://support.example.com/network-troubleshooting"
            ],
            "security": [
                "https://docs.example.com/security-best-practices",
                "https://support.example.com/secure-configuration"
            ],
            "storage": [
                "https://docs.example.com/storage-optimization",
                "https://support.example.com/storage-diagnosis"
            ],
            "virtualization": [
                "https://docs.example.com/virtualization-tips",
                "https://support.example.com/vm-configuration"
            ]
        }
        return links.get(category, [])
    
    def _generate_troubleshooting_steps(self, category: str) -> List[str]:
        """Generate sample troubleshooting steps based on category"""
        steps = {
            "networking": [
                "Check physical connections and router LEDs",
                "Restart network devices and test connectivity",
                "Verify firewall rules and port configurations"
            ],
            "security": [
                "Review access control lists and permissions",
                "Check for unauthorized device connections",
                "Verify encryption protocols and certificate validity"
            ],
            "storage": [
                "Monitor disk space and storage quotas",
                "Check RAID array status and rebuild if needed",
                "Verify storage path configurations and permissions"
            ],
            "virtualization": [
                "Check resource allocation for virtual machines",
                "Verify hypervisor version and patches",
                "Monitor VM performance counters for bottlenecks"
            ]
        }
        return steps.get(category, [])

def validate_question(question: str) -> bool:
    """
    Validate question input
    
    Args:
        question: Question text to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not question or len(question.strip()) < 3:
        logger.warning("Question too short for meaningful analysis")
        return False
    if len(question) > 1000:
        logger.warning("Question exceeds maximum length of 1000 characters")
        return False
    return True