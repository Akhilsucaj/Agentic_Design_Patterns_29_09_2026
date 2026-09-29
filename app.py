import streamlit as st

from patterns.tool_using.graph import build_graph


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
def get_workflow():
    return build_graph()


if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None


with st.sidebar:
    st.markdown('<div class="sidebar-brand">Toolroom</div>', unsafe_allow_html=True)
    st.markdown("A small agent team for questions and calculations.")
    st.markdown('<div class="sidebar-kicker">Workflow</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="route-line"><span class="route-dot"></span>Reasoning agent</div>'
        '<div class="route-line"><span class="route-dot"></span>Math tool</div>'
        '<div class="route-line"><span class="route-dot"></span>General fallback</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="sidebar-kicker">Session</div>', unsafe_allow_html=True)
    st.caption(f"{len(st.session_state.messages) // 2} exchanges")
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


st.markdown('<div class="wordmark">Toolroom / Agentic assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">Reason, then respond.</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-note">A good answer starts by choosing the right tool.</div>',
    unsafe_allow_html=True,
)

if not st.session_state.messages:
    st.markdown('<div class="section-label">Start with a question</div>', unsafe_allow_html=True)
    examples = [
        "What is the square of the average of 10 and 5?",
        "Define artificial intelligence.",
        "Why do leaves change color in autumn?",
    ]
    columns = st.columns(3)
    for column, question in zip(columns, examples):
        with column:
            if st.button(question, use_container_width=True):
                st.session_state.pending_question = question
                st.rerun()


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and message.get("route") == "math":
            with st.expander("Calculation details"):
                st.code(message["expression"], language="python")
        elif message["role"] == "assistant" and message.get("route") == "general":
            st.caption("General response")


typed_question = st.chat_input("Ask a question")
question = st.session_state.pending_question or typed_question
st.session_state.pending_question = None

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Working through it..."):
                result = get_workflow().invoke({"question": question})
            answer = str(result.get("answer") or result.get("result") or "No answer was returned.")
            route = result.get("route", "general")
            st.markdown(answer)
            if route == "math":
                with st.expander("Calculation details"):
                    st.code(result.get("expression", ""), language="python")
            else:
                st.caption("General response")
        except Exception:
            answer = "I couldn't complete that request. Check your API key and try again."
            route = "error"
            st.error(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "route": route,
            "expression": result.get("expression", "") if route == "math" else "",
        }
    )
    st.rerun()