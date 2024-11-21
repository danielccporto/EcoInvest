from typing import Dict, Optional, Union 
from pydantic import BaseModel

class ProcessedTextResponse(BaseModel):
    text: str
    analysis_type: str
    results:  Dict[str, Union[str, float]] 
    success: bool
    message: Optional[str] = None

class ErrorResponse(BaseModel):
    success: bool
    error: str
    details: Optional[str] = None
