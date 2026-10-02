from app.skills.base import BaseSkill, SkillMetadata
from app.agents.registry import registry
import datetime
import math

class TimeSkill(BaseSkill):
    @property
    def metadata(self) -> SkillMetadata:
        return SkillMetadata(
            name="get_current_time",
            description="Returns the current system time and date.",
            parameters={"type": "object", "properties": {}}
        )

    async def run(self, **kwargs) -> str:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"The current date and time is {now}."

class CalculatorSkill(BaseSkill):
    @property
    def metadata(self) -> SkillMetadata:
        return SkillMetadata(
            name="calculate",
            description="Performs basic arithmetic operations.",
            parameters={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The math expression to evaluate (e.g., '2 + 2')"
                    }
                },
                "required": ["expression"]
            }
        )

    async def run(self, **kwargs) -> str:
        expr = kwargs.get("expression", "")
        try:
            # Using eval safely for a beginner example, but in production use a math parser
            result = eval(expr, {"__builtins__": None}, {})
            return f"The result of {expr} is {result}."
        except Exception as e:
            return f"Error calculating expression: {str(e)}"

# Register the skills
registry.register(TimeSkill)
registry.register(CalculatorSkill)
