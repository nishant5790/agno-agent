import base64
import json
import time
from datetime import datetime
from os import getenv

import streamlit as st
from agent.research_agent import DeepResearcherAgent
from agent.chat_agent import agent
from agent.youtube_agent import  youtube_agent

st.markdown(
    """
    <style>
    /* Custom Expander Styling */
    [data-testid="stExpander"] {
        background: linear-gradient(90deg, #e0e7ff 0%, #fdf2f8 100%) !important;
        color: #22223b !important;
        border-radius: 10px !important;
        box-shadow: 0 2px 8px rgba(99,102,241,0.08);
        margin-bottom: 1em;
        border: 1.5px solid #6366f1;
    }
    [data-testid="stExpander"] .streamlit-expanderHeader {
        color: #6366f1 !important;
        font-weight: bold;
        font-size: 1.1em;
        font-family: 'Montserrat', 'Segoe UI', 'Arial', sans-serif;
    }
    /* Chat message visibility */
    [data-testid="stChatMessage"] {
        background: #fdf2f8 !important;
        color: #22223b !important;
        border-radius: 8px !important;
        border: 1.5px solid #e0e7ff;
        margin-bottom: 0.5em;
        box-shadow: 0 1px 4px rgba(99,102,241,0.08);
    }
    body, .stApp {
        background: linear-gradient(135deg, #f8f4f6 0%, #e0e7ff 100%);
    }
    .main-header {
        background: #6366f1;
        color: white;
        border-radius: 12px;
        padding: 1.5em 2em;
        margin-bottom: 1em;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        font-family: 'Montserrat', 'Segoe UI', 'Arial', sans-serif;
    }
    .sidebar-content {
        background: #6366f1;
        color: white !important;
        border-radius: 12px;
        padding: 1em 1em;
        margin-top: 1em;
        font-family: 'Montserrat', 'Segoe UI', 'Arial', sans-serif;
    }
    .stTabs [data-baseweb="tab"] {
        background: #e0e7ff;
        color: #6366f1;
        font-weight: bold;
        border-radius: 8px 8px 0 0;
        font-family: 'Montserrat', 'Segoe UI', 'Arial', sans-serif;
        font-size: 1.15em;
        letter-spacing: 1px;
        text-shadow: 0 1px 2px #c7d2fe;
        transition: background 0.2s, color 0.2s;
    }
    .stTabs [aria-selected="true"] {
        background: #6366f1;
        color: #fff;
        font-size: 1.22em;
        text-shadow: 0 2px 6px #6366f1;
    }
    .stButton>button {
        background: #6366f1;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        border: none;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
        transition: background 0.2s;
        font-family: 'Montserrat', 'Segoe UI', 'Arial', sans-serif;
    }
    .stButton>button:hover {
        background: #4f46e5;
    }
    .stTextInput>div>input {
    border-radius: 12px !important;
    border: 2.5px solid #6366f1 !important;
    background: #fff !important;
    color: #22223b !important;
    font-family: 'Montserrat', 'Segoe UI', 'Arial', sans-serif;
    font-size: 1.18em !important;
    box-shadow: 0 2px 8px rgba(99,102,241,0.12);
    padding: 0.7em 1.2em !important;
    }
    .stChatInput>div>input {
        border-radius: 10px !important;
        border: 2px solid #6366f1 !important;
        background: #fff !important;
        color: #22223b !important;
        font-family: 'Montserrat', 'Segoe UI', 'Arial', sans-serif;
        font-size: 1.15em !important;
        box-shadow: 0 2px 8px rgba(99,102,241,0.10);
        padding: 0.5em 1em !important;
    }
    .stCaption {
        color: #6366f1;
        font-family: 'Montserrat', 'Segoe UI', 'Arial', sans-serif;
        font-size: 1.05em;
    }
    .stInfo {
        background: #e0e7ff;
        color: #6366f1;
        border-radius: 8px;
        font-family: 'Montserrat', 'Segoe UI', 'Arial', sans-serif;
    }
    .catchy-tab-header {
        font-family: 'Montserrat', 'Segoe UI', 'Arial', sans-serif;
        font-size: 2em;
        font-weight: 700;
        letter-spacing: 2px;
        color: #6366f1;
        text-shadow: 0 2px 8px #c7d2fe;
        margin-bottom: 0.2em;
    }
    .catchy-tab-caption {
        font-family: 'Montserrat', 'Segoe UI', 'Arial', sans-serif;
        font-size: 1.15em;
        color: #6366f1;
        margin-bottom: 0.5em;
        text-shadow: 0 1px 4px #bae6fd;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.set_page_config(
    page_title="Aion AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --- HEADER ---
st.markdown(
    """
    <div class="main-header">
        <div style="display: flex; align-items: center; gap: 18px;">
            <span style="font-size:3rem;">🤖</span>
            <div>
                <h1 style="margin-bottom: 0.2em;">Aion AI</h1>
                <div style="font-size:1.2rem; color: #e0e7ff;">
                    <b>Multi-agent AI system</b> for research, chat, and YouTube analysis.
                </div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.divider()


# --- SIDEBAR ---
with st.sidebar:
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.header("🤖 Aion Agents")
    st.markdown(
        """
        <ul style='font-size:1.1em;'>
        <li>🧠 <b>Research Agent</b>: Multi-stage AI workflow for research and reporting.</li>
        <li>💬 <b>Chat Agent</b>: Chat with AI in real time.</li>
        <li>📺 <b>YouTube Analyser</b>: Analyze YouTube videos with AI.</li>
        </ul>
        """,
        unsafe_allow_html=True,
    )
    st.info("Choose a tab above to interact with different agents.")
    st.markdown("---")
    st.caption("Built by DexterLab 🧑‍💻")
    st.markdown('</div>', unsafe_allow_html=True)


# --- SESSION STATE ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "chat_tab_history" not in st.session_state:
    st.session_state.chat_tab_history = []
if "trigger_research" not in st.session_state:
    st.session_state.trigger_research = None

# --- MAIN TABS ---
tab1, tab2, tab3 = st.tabs([ "Chat Agent","Research Agent", "Youtube Analyser"])

# --- Chat Agent Tab ---
with tab1:
    st.markdown('<div class="catchy-tab-header">💬 Chat Agent</div>', unsafe_allow_html=True)
    st.markdown('<div class="catchy-tab-caption">Chat with the AI agent. <span style="color:#6366f1;">Ask anything!</span></div>', unsafe_allow_html=True)
    st.markdown("<hr style='border:1px solid #6366f1;'>", unsafe_allow_html=True)
    st.markdown('<div style="margin: 1em 0 0.5em 0; font-weight: 600; color: #6366f1; font-size: 1.1em;">Your Message:</div>', unsafe_allow_html=True)
    if st.session_state.chat_tab_history:
        st.subheader("Chat History")
        clear_chat = st.button("Clear Chat History", key="clear_chat_tab")
        if clear_chat:
            st.session_state.chat_tab_history = []
            st.rerun()
        for i, conversation in enumerate(st.session_state.chat_tab_history):
            with st.container():
                with st.chat_message("user"):
                    st.write(conversation["question"])
                with st.chat_message("assistant"):
                    st.markdown(conversation["response"])
                    st.caption(f"🕒 Chat at: <span style='color:#06b6d4;'>{conversation['timestamp']}</span>", unsafe_allow_html=True)
                if i < len(st.session_state.chat_tab_history) - 1:
                    st.divider()
    chat_input = st.chat_input("Type your message...")
    if chat_input:
        try:
            chat_response = agent.run(chat_input,stream=True)
            full_report = ""
            report_container = st.empty()
            with st.spinner("💡 AI is thinking..."):
                for chunk in  chat_response:
                    if chunk.content:
                        full_report += chunk.content
                        report_container.markdown(full_report)
            chat_conversation = {
                "question": chat_input,
                "response": full_report,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            st.session_state.chat_tab_history.append(chat_conversation)
            st.rerun()
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")


# --- Research Agent Tab ---
with tab2:
    st.markdown('<div class="catchy-tab-header">🧠 Deep Research Agent</div>', unsafe_allow_html=True)
    st.markdown('<div class="catchy-tab-caption">Multi-stage AI workflow for <span style="color:#6366f1;">comprehensive research</span>, <span style="color:#6366f1;">analysis</span>, and <span style="color:#6366f1;">reporting</span>.</div>', unsafe_allow_html=True)
    st.markdown("<hr style='border:1px solid #6366f1;'>", unsafe_allow_html=True)
    # Chat history for research agent
    if st.session_state.chat_history:
        st.subheader("💬 Chat History")
        for i, conversation in enumerate(st.session_state.chat_history):
            with st.container():
                with st.chat_message("user"):
                    st.write(conversation["question"])
                with st.chat_message("assistant"):
                    st.markdown(conversation["response"])
                    st.caption(f"✅ Research completed at: <span style='color:#facc15;'>{conversation['timestamp']}</span>", unsafe_allow_html=True)
                if i < len(st.session_state.chat_history) - 1:
                    st.divider()
    user_input = st.chat_input("Ask a research question...")
    if st.session_state.trigger_research:
        user_input = st.session_state.trigger_research
        st.session_state.trigger_research = None
        with st.chat_message("user"):
            st.write(user_input)
    if user_input:
        try:
            agent = DeepResearcherAgent()
            current_conversation = {
                "question": user_input,
                "response": "",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            with st.status("🚀 Executing research plan...", expanded=True) as status:
                # PHASE 1: Researching
                phase1_msg = "🧠 <b>Phase 1: Researching</b> - Finding and extracting relevant information from the web..."
                status.write(phase1_msg)
                research_content = agent.searcher.run(user_input)
                st.progress(33, text="Phase 1/3: Researching...")
                # PHASE 2: Analyzing
                phase2_msg = "🔬 <b>Phase 2: Analyzing</b> - Synthesizing and interpreting the research findings..."
                status.write(phase2_msg)
                analysis = agent.analyst.run(research_content.content)
                st.progress(66, text="Phase 2/3: Analyzing...")
                # PHASE 3: Writing Report
                phase3_msg = "✍️ <b>Phase 3: Writing Report</b> - Producing a final, polished report..."
                status.write(phase3_msg)
                report_iterator = agent.writer.run(analysis.content, stream=True)
                st.progress(100, text="Phase 3/3: Writing Report...")
            # Collect the full report
            full_report = ""
            report_container = st.empty()
            with st.spinner("🤔 AI is preparing your research report..."):
                for chunk in report_iterator:
                    if chunk.content:
                        full_report += chunk.content
                        report_container.markdown(full_report)
            # Store the complete conversation
            current_conversation["response"] = full_report
            st.session_state.chat_history.append(current_conversation)
            st.rerun()
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# --- Youtube Analyser Tab ---
with tab3:
    st.markdown('<div class="catchy-tab-header">📺 Youtube Analyser</div>', unsafe_allow_html=True)
    st.markdown('<div class="catchy-tab-caption">Paste a YouTube link below and get an AI-powered analysis of the video.</div>', unsafe_allow_html=True)
    st.markdown("<hr style='border:1px solid #6366f1;'>", unsafe_allow_html=True)
    with st.expander("🔎 How does it work?", expanded=False):
        st.write("Paste a YouTube link and let the AI analyze the video content, summary, and insights.")
    st.markdown('<div style="margin: 1em 0 0.5em 0; font-weight: 600; color: #6366f1; font-size: 1.1em;">YouTube Video Link:</div>', unsafe_allow_html=True)
    # st.text_input("Enter YouTube video link...")
    youtube_link = st.text_input("Enter YouTube video link...")
   
    # st.markdown('</div>', unsafe_allow_html=True)
    if youtube_link:
        try:
            with st.spinner("🔍 Analyzing video..."):
                analysis_result = youtube_agent.run(youtube_link,stream=True)
                full_report = ""
                report_container = st.empty()
                for chunk in  analysis_result:
                    if chunk.content:
                        full_report += chunk.content
                        report_container.markdown(full_report)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")