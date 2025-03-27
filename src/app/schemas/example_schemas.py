"""Pydantic models"""

from typing import Any, Dict

from pydantic import BaseModel, Field


class Example(BaseModel):
    request: Dict[str, Any] = Field(description="The request data")
