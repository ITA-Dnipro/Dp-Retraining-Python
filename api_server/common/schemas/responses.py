from typing import Any

from pydantic import BaseModel, Field


class ResponseBaseSchema(BaseModel):
    """Base http response schema."""
    status_code: Any = Field()
    data: Any = Field()
    errors: Any = Field()
