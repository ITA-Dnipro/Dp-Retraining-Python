from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel


class EmployeeBaseSchema(BaseModel):
    """Employee Base schema."""
    pass


class EmployeeInputSchema(BaseModel):
    """Employee Input schema."""
    user_id: UUID

