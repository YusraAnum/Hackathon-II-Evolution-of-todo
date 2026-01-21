from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Todo:
    """
    Represents a single todo item with required attributes per specification.

    Attributes:
        id: Unique identifier assigned automatically upon creation
        description: Text content describing the task
        status: Either "incomplete" or "complete"
        created_at: Timestamp automatically assigned upon creation
    """
    id: int
    description: str
    status: str  # "incomplete" or "complete"
    created_at: datetime

    def __post_init__(self):
        """Validate that status is either 'incomplete' or 'complete'."""
        if self.status not in ["incomplete", "complete"]:
            raise ValueError(f"Status must be 'incomplete' or 'complete', got '{self.status}'")