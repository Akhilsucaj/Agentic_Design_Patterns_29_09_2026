from typing import Literal, TypedDict
from typing_extensions import NotRequired

class AgentState(TypedDict):
    question: str
    route: NotRequired[Literal["math", "general"]]
    expression: NotRequired[str]
    result: NotRequired[str]
    answer: NotRequired[str]