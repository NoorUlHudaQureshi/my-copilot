from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class SkillMetadata(BaseModel):
    name: str
    description: str
    parameters: Dict[str, Any] = Field(default_factory=dict)

class BaseSkill(ABC):
    """Abstract base class for all AI skills."""

    @property
    @abstractmethod
    def metadata(self) -> SkillMetadata:
        """Return the metadata of the skill for LLM tool definition."""
        pass

    @abstractmethod
    async def run(self, **kwargs) -> Any:
        """Execute the skill logic."""
        pass
