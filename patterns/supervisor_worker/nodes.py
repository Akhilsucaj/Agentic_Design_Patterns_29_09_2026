import re

from config.llm import get_llm
from tools.calculator import calculator
from tools.leaves_db import get_leave_balance
from .state import SupervisorWorkerState

llm = get_llm()


def supervisor(state: SupervisorWorkerState):
    query = state["query"]

    prompt = f"""
    Decide which worker should handle this request.

    Return ONLY one word:
    - math
    - leave
    - general

    Use:
    - math → calculations, percentages, averages, totals
    - leave → leave balance, vacation, sick leave, PTO
    - general → definitions, explanations, factual questions, and anything else

    Examples:
    Request: What is the square of the average of 10 and 5?
    Worker: math
    Request: How many leave days does Alice have?
    Worker: leave
    Request: Define artificial intelligence.
    Worker: general

    When unsure, choose general. Do not choose math unless the request clearly
    asks for a calculation.

    Request: {query}
    """

    worker = llm.invoke(prompt).content.strip().lower()

    has_math_intent = bool(
        re.search(
            r"\b(calculate|compute|sum|add|subtract|difference|multiply|times|product|divide|average|mean|square|cube|percent|percentage|total|evaluate)\b",
            query,
            re.IGNORECASE,
        )
        or re.search(r"\d\s*[+*/%^-]\s*\d", query)
    )
    has_leave_intent = bool(
        re.search(r"\b(leave|pto|vacation|sick|time off)\b", query, re.IGNORECASE)
    )

    if worker not in {"math", "leave", "general"}:
        worker = "general"
    elif worker == "math" and not has_math_intent:
        worker = "general"
    elif worker == "leave" and not has_leave_intent:
        worker = "general"

    print(f"[Supervisor] Worker selected: {worker}")

    return {"worker": worker}


def math_agent(state: SupervisorWorkerState):
    query = state["query"]

    prompt = f"""
    Convert this request into a Python arithmetic expression.

    Return only the expression.

    Request: {query}
    """

    expression = llm.invoke(prompt).content.strip()

    print(f"[Math Agent] Expression: {expression}")

    try:
        result = calculator(expression)
    except Exception as e:
        result = f"Error: {e}"

    return {
        "expression": expression,
        "result": result
    }


def leaves_balance(state: SupervisorWorkerState):
    query = state["query"]

    prompt = f"""
    Extract the employee name from this request.

    Return only the employee name.

    Request: {query}
    """

    employee_name = llm.invoke(prompt).content.strip()

    print(f"[Leave Agent] Employee: {employee_name}")

    balance = get_leave_balance(employee_name)

    return {
        "employee_name": employee_name,
        "leave_balance": balance,
        "result": balance
    }


def general_agent(state: SupervisorWorkerState):
    prompt = f"""
    Answer the user's question clearly and helpfully.
    If it is ambiguous, briefly mention the assumption you are making.

    Question: {state['query']}
    """

    answer = llm.invoke(prompt).content.strip()

    print("[General Agent] Answer generated")

    return {"result": answer}