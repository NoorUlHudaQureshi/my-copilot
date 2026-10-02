from typing import Dict, Type, Any
from app.skills.base import BaseSkill, SkillMetadata

class SkillRegistry:
    """Singleton registry to manage and execute AI skills."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SkillRegistry, cls).__new__(cls)
            cls._instance.skills: Dict[str, BaseSkill] = {}
        return cls._instance

    def register(self, skill_cls: Type[BaseSkill]):
        """Register a skill class into the registry."""
        skill_instance = skill_cls()
        name = skill_instance.metadata.name
        self.skills[name] = skill_instance
        print(f"Skill Registered: {name}")

    def get_skill(self, name: str) -> Optional[BaseSkill]:
        """Retrieve a skill by its name."""
        return self.skills.get(name)

    def get_all_metadata(self) -> List[Dict[str, Any]]:
        """Return metadata for all registered skills as LLM tool definitions."""
        return [
            {
                "type": "function",
                "function": {
                    "name": s.metadata.name,
                    "description": s.metadata.description,
                    "parameters": s.metadata.parameters
                }
            }
            for s in self.skills.values()
        ]

# Global registry instance
registry = SkillRegistry()
