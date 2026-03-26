from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List
from enum import Enum

class UpdateType(str, Enum):
    EDUCATION = "education"
    PROJECT = "project"
    MUSIC = "music"
    BIO = "bio"

class PortfolioUpdate(BaseModel):
    """
    The strict schema for any portfolio update. 
    This is what PydanticAI uses to validate the AI's intent.
    """
    type: UpdateType = Field(..., description="The category of the update")
    
    # Education specific
    cgpa: Optional[float] = Field(None, ge=0.0, le=10.0, description="The CGPA value, must be between 0 and 10")
    semester: Optional[int] = Field(None, ge=1, le=8, description="The semester number")
    
    # Project/Media specific
    title: Optional[str] = Field(None, description="Title of the project or reel")
    link: Optional[HttpUrl] = Field(None, description="A valid URL for the project, video, or image")
    description: Optional[str] = Field(None, description="The text content for a bio or project description")

    class Config:
        schema_extra = {
            "example": {
                "type": "education",
                "cgpa": 9.2,
                "semester": 6
            }
        }