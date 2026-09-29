from typing import Literal, TypedDict

from config.llm import get_llm
from tools.calculator import calculator
from .state import AgentState
from langchain_core.messages import HumanMessage, SystemMessage

llm = get_llm()
planner = llm.with_structured_output(
    TypedDict(
        "RoutingDecision",
        {"route": Literal["math", "general"], "expression": str},
    )
)

def reasoning_agent(state: AgentState):
    decision = planner.invoke(
        [
            SystemMessage(
                content=(
                    "Classify the user's question. Choose 'math' only when it asks "
                    "for a numeric calculation that can be represented as a basic "
                    "Python arithmetic expression. For definitions, explanations, "
                    "factual questions, or anything else, choose 'general'. When "
                    "route is 'general', set expression to an empty string. When "
                          "route is 'math', return only the arithmetic expression. "
                          "Preserve the order of operations requested by the user and "
                          "use parentheses to group intermediate calculations. For "
                          "example, the square of the average of 10 and 5 is "
                          "((10 + 5) / 2) ** 2, not (10 + 5) / 2 ** 2."
                )
            ),
            HumanMessage(content=state["question"]),
        ]
    )
    return {"route": decision["route"], "expression": decision["expression"]}

def tool_executor(state: AgentState):
    result = calculator(state["expression"])
    return {"result": result, "answer": result}

def fallback_agent(state: AgentState):
    response = llm.invoke(
        [
            SystemMessage(
                content=(
                    "Answer the user's question clearly and accurately. If the "
                    "question is ambiguous, briefly state the assumption you make."
                )
            ),
            HumanMessage(content=state["question"]),
        ]
    )
    answer = response.content.strip()
    return {"answer": answer, "result": answer}