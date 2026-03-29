import streamlit as st
import requests
import time
import json
from datetime import datetime
 N MBVEJK
 \


# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Agentic Support",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Config ─────────────────────────────────────────────────────────────────
import os
API_BASE_URL = os.environ.get("API_BASE_URL") \
    or st.secrets.get("API_BASE_URL", "http://localhost:8000") \
    if hasattr(st, "secrets") else os.environ.get("API_BASE_URL", "http://localhost:8000")

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:ital,wght@0,400;0,500;1,400&display=swap');

/* ── Global Reset ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f !important;
    color: #e8e6e3 !important;
    font-family: 'DM Mono', monospace !important;
}

[data-testid="stSidebar"] {
    background: #0f0f18 !important;
    border-right: 1px solid #1e1e2e !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

/* ── Hero Header ── */
.hero-header {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: clamp(2rem, 5vw, 3.5rem);
    letter-spacing: -0.03em;
    line-height: 1.05;
    background: linear-gradient(135deg, #e8e6e3 0%, #a78bfa 40%, #60a5fa 80%, #34d399 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.25rem;
}

.hero-sub {
    font-family: 'DM Mono', monospace;
    font-size: 0.78rem;
    color: #4a4a6a;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 2rem;
}

/* ── Status Badge ── */
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.3rem 0.8rem;
    border-radius: 999px;
    font-size: 0.7rem;
    font-family: 'DM Mono', monospace;
    letter-spacing: 0.1em;
    font-weight: 500;
    border: 1px solid;
}
.status-online {
    background: rgba(52, 211, 153, 0.08);
    border-color: rgba(52, 211, 153, 0.3);
    color: #34d399;
}
.status-offline {
    background: rgba(239, 68, 68, 0.08);
    border-color: rgba(239, 68, 68, 0.3);
    color: #ef4444;
}
.status-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: currentColor;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}

/* ── Chat Container ── */
.chat-wrapper {
    max-height: 520px;
    overflow-y: auto;
    padding: 1rem 0;
    scrollbar-width: thin;
    scrollbar-color: #1e1e2e transparent;
}

/* ── Message Bubbles ── */
.msg-row {
    display: flex;
    gap: 0.75rem;
    margin-bottom: 1.25rem;
    animation: fadeUp 0.3s ease;
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}
.msg-row.user { flex-direction: row-reverse; }

.msg-avatar {
    width: 32px; height: 32px;
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.9rem;
    flex-shrink: 0;
    margin-top: 2px;
}
.avatar-user {
    background: linear-gradient(135deg, #a78bfa, #60a5fa);
}
.avatar-agent {
    background: linear-gradient(135deg, #1e1e2e, #2a2a3e);
    border: 1px solid #2e2e4e;
}

.msg-bubble {
    max-width: 75%;
    padding: 0.85rem 1.1rem;
    border-radius: 12px;
    font-size: 0.85rem;
    line-height: 1.65;
}
.bubble-user {
    background: linear-gradient(135deg, rgba(167, 139, 250, 0.15), rgba(96, 165, 250, 0.15));
    border: 1px solid rgba(167, 139, 250, 0.25);
    color: #e8e6e3;
    border-top-right-radius: 3px;
}
.bubble-agent {
    background: #111120;
    border: 1px solid #1e1e2e;
    color: #c8c6c3;
    border-top-left-radius: 3px;
}

.msg-meta {
    font-size: 0.65rem;
    color: #3a3a5a;
    margin-top: 0.35rem;
    font-family: 'DM Mono', monospace;
    letter-spacing: 0.05em;
}
.msg-row.user .msg-meta { text-align: right; }

/* ── Source Chips ── */
.source-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
    margin-top: 0.6rem;
}
.source-chip {
    padding: 0.2rem 0.55rem;
    background: rgba(96, 165, 250, 0.08);
    border: 1px solid rgba(96, 165, 250, 0.2);
    border-radius: 4px;
    font-size: 0.65rem;
    color: #60a5fa;
    letter-spacing: 0.05em;
}

/* ── Thinking Indicator ── */
.thinking-row {
    display: flex;
    gap: 0.75rem;
    margin-bottom: 1rem;
    animation: fadeUp 0.3s ease;
}
.thinking-bubble {
    background: #111120;
    border: 1px solid #1e1e2e;
    border-radius: 12px;
    border-top-left-radius: 3px;
    padding: 0.85rem 1.1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.78rem;
    color: #4a4a6a;
}
.dots span {
    display: inline-block;
    width: 5px; height: 5px;
    border-radius: 50%;
    background: #4a4a6a;
    animation: bounce 1.2s infinite;
}
.dots span:nth-child(2) { animation-delay: 0.2s; }
.dots span:nth-child(3) { animation-delay: 0.4s; }
@keyframes bounce {
    0%, 80%, 100% { transform: translateY(0); }
    40% { transform: translateY(-5px); }
}

/* ── Input Area ── */
[data-testid="stTextInput"] input {
    background: #111120 !important;
    border: 1px solid #1e1e2e !important;
    border-radius: 10px !important;
    color: #e8e6e3 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.85rem !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.2s ease !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #a78bfa !important;
    box-shadow: 0 0 0 3px rgba(167, 139, 250, 0.1) !important;
}
[data-testid="stTextInput"] input::placeholder { color: #3a3a5a !important; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #a78bfa, #60a5fa) !important;
    color: #0a0a0f !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.08em !important;
    padding: 0.55rem 1.2rem !important;
    transition: opacity 0.2s ease, transform 0.15s ease !important;
}
.stButton > button:hover {
    opacity: 0.85 !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Feedback buttons ── */
.feedback-row {
    display: flex;
    gap: 0.5rem;
    margin-top: 0.6rem;
}

/* ── Sidebar ── */
.sidebar-section {
    background: #111120;
    border: 1px solid #1e1e2e;
    border-radius: 10px;
    padding: 1rem;
    margin-bottom: 1rem;
}
.sidebar-title {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #4a4a6a;
    margin-bottom: 0.75rem;
}
.stat-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.4rem 0;
    border-bottom: 1px solid #1a1a2e;
    font-size: 0.75rem;
}
.stat-row:last-child { border-bottom: none; }
.stat-label { color: #4a4a6a; }
.stat-value { color: #a78bfa; font-weight: 500; }

/* ── Divider ── */
.custom-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #1e1e2e 20%, #1e1e2e 80%, transparent);
    margin: 1.5rem 0;
}

/* ── Agent tag ── */
.agent-tag {
    display: inline-block;
    font-size: 0.6rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 0.15rem 0.4rem;
    border-radius: 3px;
    margin-right: 0.4rem;
    font-weight: 600;
}
.tag-rag { background: rgba(52,211,153,0.12); color: #34d399; border: 1px solid rgba(52,211,153,0.25); }
.tag-llm { background: rgba(167,139,250,0.12); color: #a78bfa; border: 1px solid rgba(167,139,250,0.25); }
.tag-tool { background: rgba(251,191,36,0.12); color: #fbbf24; border: 1px solid rgba(251,191,36,0.25); }

/* ── Selectbox / Dropdown ── */
[data-testid="stSelectbox"] > div > div {
    background: #111120 !important;
    border: 1px solid #1e1e2e !important;
    border-radius: 8px !important;
    color: #e8e6e3 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.8rem !important;
}

/* ── Slider ── */
[data-testid="stSlider"] .stSlider > div { background: #1e1e2e !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #1e1e2e; border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: #2e2e4e; }

</style>
""", unsafe_allow_html=True)


# ─── Session State ───────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "messages": [],
        "session_id": f"sess_{int(time.time())}",
        "total_queries": 0,
        "positive_feedback": 0,
        "negative_feedback": 0,
        "api_status": None,
        "thinking": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# ─── API Helpers ─────────────────────────────────────────────────────────────
@st.cache_data(ttl=30)
def check_api_health():
    try:
        r = requests.get(f"{API_BASE_URL}/health", timeout=3)
        return r.status_code == 200
    except Exception:
        return False


def call_api(query: str, top_k: int = 3, mode: str = "rag"):
    try:
        payload = {"query": query, "top_k": top_k, "mode": mode,
                   "session_id": st.session_state.session_id}
        r = requests.post(f"{API_BASE_URL}/query", json=payload, timeout=30)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        return {"error": "Cannot connect to API. Is the backend running?"}
    except requests.exceptions.Timeout:
        return {"error": "Request timed out. The backend may be overloaded."}
    except Exception as e:
        return {"error": str(e)}


def send_feedback(query: str, answer: str, feedback: str):
    try:
        requests.post(f"{API_BASE_URL}/feedback", json={
            "query": query, "answer": answer,
            "feedback": feedback,
            "session_id": st.session_state.session_id
        }, timeout=5)
    except Exception:
        pass


# ─── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="hero-header" style="font-size:1.4rem;">⚡ AGENTSYS</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub" style="font-size:0.65rem;">INTELLIGENT SUPPORT CONSOLE</div>', unsafe_allow_html=True)

    # API Status
    is_online = check_api_health()
    st.session_state.api_status = is_online
    status_cls = "status-online" if is_online else "status-offline"
    status_txt = "BACKEND ONLINE" if is_online else "BACKEND OFFLINE"
    st.markdown(f'<div class="status-badge {status_cls}"><span class="status-dot"></span>{status_txt}</div>',
                unsafe_allow_html=True)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # Settings
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">⚙ Query Settings</div>', unsafe_allow_html=True)
    mode = st.selectbox("Mode", ["rag", "llm", "hybrid"], index=0,
                        help="rag = retrieval-augmented, llm = pure LLM, hybrid = both")
    top_k = st.slider("Top-K Documents", min_value=1, max_value=10, value=3,
                      help="Number of documents to retrieve")
    st.markdown('</div>', unsafe_allow_html=True)

    # Session Stats
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">📊 Session Stats</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="stat-row"><span class="stat-label">Queries</span><span class="stat-value">{st.session_state.total_queries}</span></div>
    <div class="stat-row"><span class="stat-label">👍 Helpful</span><span class="stat-value">{st.session_state.positive_feedback}</span></div>
    <div class="stat-row"><span class="stat-label">👎 Not helpful</span><span class="stat-value">{st.session_state.negative_feedback}</span></div>
    <div class="stat-row"><span class="stat-label">Session ID</span><span class="stat-value" style="font-size:0.6rem;">{st.session_state.session_id[-8:]}</span></div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Clear history
    if st.button("🗑 Clear History", use_container_width=True):
        st.session_state.messages = []
        st.session_state.total_queries = 0
        st.session_state.positive_feedback = 0
        st.session_state.negative_feedback = 0
        st.rerun()

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # Agent Legend
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">🤖 Agent Tags</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="display:flex;flex-direction:column;gap:0.4rem;font-size:0.72rem;color:#4a4a6a;">
        <div><span class="agent-tag tag-rag">RAG</span> Document retrieval</div>
        <div><span class="agent-tag tag-llm">LLM</span> Language model</div>
        <div><span class="agent-tag tag-tool">TOOL</span> External tools</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ─── Main Area ───────────────────────────────────────────────────────────────
col_main, col_gap = st.columns([1, 0.001])

with col_main:
    st.markdown('<div class="hero-header">Agentic Support System</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Powered by RAG · LangChain · FastAPI</div>', unsafe_allow_html=True)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # ── Chat History ──
    chat_html = '<div class="chat-wrapper" id="chat-container">'

    if not st.session_state.messages:
        chat_html += """
        <div style="text-align:center;padding:3rem 1rem;color:#2a2a4a;">
            <div style="font-size:2.5rem;margin-bottom:1rem;">⚡</div>
            <div style="font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;color:#3a3a5a;letter-spacing:-0.01em;">
                Ask anything about your docs
            </div>
            <div style="font-size:0.72rem;margin-top:0.5rem;color:#2a2a4a;">
                The agent will retrieve relevant context and generate an answer
            </div>
        </div>
        """
    else:
        for i, msg in enumerate(st.session_state.messages):
            ts = msg.get("timestamp", "")
            if msg["role"] == "user":
                chat_html += f"""
                <div class="msg-row user">
                    <div class="msg-avatar avatar-user">U</div>
                    <div>
                        <div class="msg-bubble bubble-user">{msg["content"]}</div>
                        <div class="msg-meta">{ts}</div>
                    </div>
                </div>
                """
            else:
                agent_tag = msg.get("agent", "rag").upper()
                tag_cls = f"tag-{msg.get('agent','rag')}"
                sources_html = ""
                if msg.get("sources"):
                    chips = "".join(f'<span class="source-chip">📄 {s}</span>'
                                    for s in msg["sources"][:4])
                    sources_html = f'<div class="source-chips">{chips}</div>'
                chat_html += f"""
                <div class="msg-row">
                    <div class="msg-avatar avatar-agent">A</div>
                    <div>
                        <div class="msg-bubble bubble-agent">
                            <span class="agent-tag {tag_cls}">{agent_tag}</span>
                            {msg["content"]}
                            {sources_html}
                        </div>
                        <div class="msg-meta">{ts} · msg #{i//2 + 1}</div>
                    </div>
                </div>
                """

    # Thinking indicator
    if st.session_state.thinking:
        chat_html += """
        <div class="thinking-row">
            <div class="msg-avatar avatar-agent">A</div>
            <div class="thinking-bubble">
                <span style="color:#3a3a5a;font-size:0.7rem;letter-spacing:0.05em;">THINKING</span>
                <span class="dots"><span></span><span></span><span></span></span>
            </div>
        </div>
        """

    chat_html += '</div>'
    st.markdown(chat_html, unsafe_allow_html=True)

    # Auto-scroll
    st.markdown("""
    <script>
        const c = document.getElementById('chat-container');
        if (c) c.scrollTop = c.scrollHeight;
    </script>
    """, unsafe_allow_html=True)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # ── Feedback for last response ──
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
        last_q = next((m["content"] for m in reversed(st.session_state.messages)
                       if m["role"] == "user"), "")
        last_a = st.session_state.messages[-1]["content"]

        st.markdown('<div style="font-size:0.7rem;color:#3a3a5a;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.5rem;">Was this helpful?</div>', unsafe_allow_html=True)
        fb_col1, fb_col2, fb_col3 = st.columns([0.12, 0.12, 1])
        with fb_col1:
            if st.button("👍", key="fb_pos", help="Helpful"):
                send_feedback(last_q, last_a, "positive")
                st.session_state.positive_feedback += 1
                st.toast("Thanks for the feedback!", icon="✅")
        with fb_col2:
            if st.button("👎", key="fb_neg", help="Not helpful"):
                send_feedback(last_q, last_a, "negative")
                st.session_state.negative_feedback += 1
                st.toast("Feedback noted. We'll improve.", icon="📝")

    # ── Input ──
    with st.form("query_form", clear_on_submit=True):
        input_col, btn_col = st.columns([5, 1])
        with input_col:
            user_input = st.text_input(
                "query",
                placeholder="Ask a question about your knowledge base...",
                label_visibility="collapsed"
            )
        with btn_col:
            submitted = st.form_submit_button("Send →", use_container_width=True)

    # ── Example Prompts ──
    st.markdown('<div style="font-size:0.65rem;color:#2a2a4a;letter-spacing:0.08em;text-transform:uppercase;margin:0.75rem 0 0.4rem;">Try asking:</div>', unsafe_allow_html=True)
    ex_col1, ex_col2, ex_col3 = st.columns(3)
    examples = [
        "How does the RAG pipeline work?",
        "What tools does the agent have?",
        "Explain the orchestrator graph",
    ]
    for col, ex in zip([ex_col1, ex_col2, ex_col3], examples):
        with col:
            if st.button(ex, use_container_width=True, key=f"ex_{ex[:10]}"):
                user_input = ex
                submitted = True

    # ── Handle Submission ──
    if submitted and user_input and user_input.strip():
        ts = datetime.now().strftime("%H:%M")
        st.session_state.messages.append({
            "role": "user",
            "content": user_input.strip(),
            "timestamp": ts
        })
        st.session_state.total_queries += 1
        st.session_state.thinking = True
        st.rerun()

# ── API Call (after rerun with thinking=True) ──
if st.session_state.thinking:
    last_user_msg = next(
        (m["content"] for m in reversed(st.session_state.messages) if m["role"] == "user"),
        None
    )
    if last_user_msg:
        with st.spinner(""):
            result = call_api(last_user_msg, top_k=top_k, mode=mode)

        ts = datetime.now().strftime("%H:%M")
        if "error" in result:
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"⚠️ {result['error']}",
                "timestamp": ts,
                "agent": "llm",
                "sources": []
            })
        else:
            answer = result.get("answer", result.get("response", "No answer returned."))
            sources = result.get("sources", result.get("source_documents", []))
            # Normalise sources to strings
            source_names = []
            for s in sources:
                if isinstance(s, str):
                    source_names.append(s)
                elif isinstance(s, dict):
                    source_names.append(s.get("source", s.get("title", "doc")))
                else:
                    source_names.append(str(s))

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "timestamp": ts,
                "agent": mode,
                "sources": source_names
            })

    st.session_state.thinking = False
    st.rerun()