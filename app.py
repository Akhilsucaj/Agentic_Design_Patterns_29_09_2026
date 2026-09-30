import streamlit as st

from patterns.planner_executor.graph import build_graph as build_planner_graph
from patterns.tool_using.graph import build_graph as build_tool_using_graph


st.set_page_config(
    page_title="Toolroom | Agentic assistant",
    page_icon="T",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

    :root {
        --ink: #18332f;
        --muted: #6c7c76;
        --paper: #f5f6f0;
        --line: #dce4dc;
        --green: #176b58;
        --lime: #d9ef83;
        --coral: #d87c5f;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        color: var(--ink);
    }

    [data-testid="stAppViewContainer"] {
        background:
            linear-gradient(135deg, rgba(217, 239, 131, .16), transparent 38%),
            var(--paper);
    }

    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stSidebar"] {
        background: #183b34;
        border-right: 1px solid rgba(255,255,255,.09);
    }
    [data-testid="stSidebar"] * { color: #edf4e9; }
    [data-testid="stSidebar"] [data-testid="stButton"] button {
        background: transparent;
        border: 1px solid rgba(237,244,233,.25);
    }
    [data-testid="stSidebar"] [data-testid="stButton"] button:hover {
        border-color: var(--lime);
        color: var(--lime);
    }

    .block-container {
        max-width: 1020px;
        padding-top: 3.25rem;
        padding-bottom: 2.5rem;
    }
    .wordmark {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        color: var(--green);
    }
    .hero-title {
        max-width: 720px;
        margin: 14px 0 8px;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 52px;
        font-weight: 600;
        line-height: 1.08;
        color: var(--ink);
    }
    .hero-note {
        margin: 0 0 28px;
        color: var(--muted);
        font-size: 16px;
    }
    .section-label {
        margin: 25px 0 10px;
        color: var(--muted);
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.2px;
        text-transform: uppercase;
    }
    .sidebar-brand {
        padding: 8px 0 28px;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 20px;
        font-weight: 700;
    }
    .sidebar-kicker {
        margin: 26px 0 8px;
        color: #b8c9be;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 1.3px;
        text-transform: uppercase;
    }
    .route-line {
        padding: 9px 0;
        border-bottom: 1px solid rgba(237,244,233,.14);
        font-size: 13px;
    }
    .route-dot {
        display: inline-block;
        width: 7px;
        height: 7px;
        margin-right: 9px;
        border-radius: 50%;
        background: var(--lime);
    }
    [data-testid="stChatMessage"] {
        border: 1px solid var(--line);
        border-radius: 8px;
        background: rgba(255,255,255,.72);
    }
    [data-testid="stChatInput"] {
        border-color: #c9d7cd;
        border-radius: 8px;
        background: rgba(255,255,255,.92);
    }
    [data-testid="stChatInput"]:focus-within {
        border-color: var(--green);
        box-shadow: 0 0 0 1px var(--green);
    }
    [data-testid="stButton"] button {
        min-height: 42px;
        border-radius: 7px;
        border-color: #cbd9ce;
        color: var(--ink);
        font-weight: 600;
    }
    [data-testid="stButton"] button:hover {
        border-color: var(--green);
        color: var(--green);
    }
    @media (max-width: 700px) {
        .block-container { padding-top: 2rem; }
        .hero-title { font-size: 38px; }
        .hero-note { font-size: 14px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def get_tool_using_workflow():
    return build_tool_using_graph()


@st.cache_resource
def get_planner_executor_workflow():
    return build_planner_graph()


with st.sidebar:
    st.markdown('<div class="sidebar-brand">Toolroom</div>', unsafe_allow_html=True)
    pattern_label = st.radio(
        "Demonstration",
        ["Tool-using", "Planner-executor"],
        key="demo_pattern",
    )
    is_planner_executor = pattern_label == "Planner-executor"
    pattern_key = "planner_executor" if is_planner_executor else "tool_using"
    messages_key = "planner_messages" if is_planner_executor else "messages"
    pending_question_key = (
        "planner_pending_question" if is_planner_executor else "pending_question"
    )
    if messages_key not in st.session_state:
        st.session_state[messages_key] = []
    if pending_question_key not in st.session_state:
        st.session_state[pending_question_key] = None

    active_messages = st.session_state[messages_key]
    st.markdown(
        "A step-by-step planning demo."
        if is_planner_executor
        else "A small agent team for questions and calculations."
    )
    st.markdown('<div class="sidebar-kicker">Workflow</div>', unsafe_allow_html=True)
    workflow_steps = (
        ["Planner agent", "Executor agent"]
        if is_planner_executor
        else ["Reasoning agent", "Math tool", "General fallback"]
    )
    workflow_html = "".join(
        f'<div class="route-line"><span class="route-dot"></span>{step}</div>'
        for step in workflow_steps
    )
    st.markdown(workflow_html, unsafe_allow_html=True)
    st.markdown('<div class="sidebar-kicker">Session</div>', unsafe_allow_html=True)
    st.caption(f"{len(active_messages) // 2} exchanges")
    if st.button("Clear conversation", use_container_width=True):
        st.session_state[messages_key] = []
        st.rerun()


st.markdown('<div class="wordmark">Toolroom / Agentic assistant</div>', unsafe_allow_html=True)
hero_title = "Plan, then execute." if is_planner_executor else "Reason, then respond."
hero_note = (
    "Watch a planner break down a task and an executor work through each step."
    if is_planner_executor
    else "A good answer starts by choosing the right tool."
)
st.markdown(f'<div class="hero-title">{hero_title}</div>', unsafe_allow_html=True)
st.markdown(
    f'<div class="hero-note">{hero_note}</div>',
    unsafe_allow_html=True,
)

if not active_messages:
    sample_heading = "Try a task" if is_planner_executor else "Start with a question"
    st.markdown(f'<div class="section-label">{sample_heading}</div>', unsafe_allow_html=True)
    examples = (
        [
            "Create a 3-step plan to prepare for a technical interview.",
            "Plan a small neighborhood garden project.",
            "Create a beginner-friendly Python study plan.",
        ]
        if is_planner_executor
        else [
            "What is the square of the average of 10 and 5?",
            "Define artificial intelligence.",
            "Why do leaves change color in autumn?",
        ]
    )
    columns = st.columns(3)
    for example_index, (column, question) in enumerate(zip(columns, examples)):
        with column:
            if st.button(
                question,
                key=f"{pattern_key}_example_{example_index}",
                use_container_width=True,
            ):
                st.session_state[pending_question_key] = question
                st.rerun()


for message in active_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant":
            if message.get("pattern") == "planner_executor":
                with st.expander("Generated plan"):
                    for step in message.get("plan", []):
                        st.markdown(step)
                st.caption("Planner-executor response")
            elif message.get("route") == "math":
                with st.expander("Calculation details"):
                    st.code(message["expression"], language="python")
            elif message.get("route") == "general":
                st.caption("General response")


input_placeholder = "Describe a task to plan" if is_planner_executor else "Ask a question"
typed_question = st.chat_input(input_placeholder)
question = st.session_state[pending_question_key] or typed_question
st.session_state[pending_question_key] = None

if question:
    active_messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    result = {}
    plan = []
    with st.chat_message("assistant"):
        try:
            with st.spinner("Working through it..."):
                if is_planner_executor:
                    result = get_planner_executor_workflow().invoke({"task": question})
                    plan = result.get("plan", [])
                    answer = str(result.get("output") or "The executor returned no output.")
                    route = "planner_executor"
                else:
                    result = get_tool_using_workflow().invoke({"question": question})
                    answer = str(
                        result.get("answer")
                        or result.get("result")
                        or "No answer was returned."
                    )
                    route = result.get("route", "general")
            st.markdown(answer)
            if is_planner_executor:
                with st.expander("Generated plan"):
                    for step in plan:
                        st.markdown(step)
                st.caption("Planner-executor response")
            elif route == "math":
                with st.expander("Calculation details"):
                    st.code(result.get("expression", ""), language="python")
            else:
                st.caption("General response")
        except Exception:
            answer = "I couldn't complete that request. Check your API key and try again."
            route = "error"
            st.error(answer)

    active_messages.append(
        {
            "role": "assistant",
            "content": answer,
            "route": route,
            "pattern": pattern_key,
            "plan": plan,
            "expression": result.get("expression", "") if route == "math" else "",
        }
    )
    st.rerun()