import base64
import json
import time
from datetime import datetime
from os import getenv

import streamlit as st
from agent.research_agent import DeepResearcherAgent

st.set_page_config(
    page_title="Deep Research Agent",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- HEADER ---
st.markdown(
    """
    <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 0;">
        <span style="font-size:2.5rem;">🔎</span>
        <div>
            <h1 style="margin-bottom: 0.2em;">Deep Research Agent</h1>
            <div style="font-size:1.1rem; color: #666;">
                Multi-stage AI workflow for comprehensive research, analysis, and reporting.
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.divider()

# --- SIDEBAR ---
with st.sidebar:
    st.header("How It Works")
    st.markdown(
        """
        **Deep Research Agent** uses a multi-stage AI workflow:
        1. **Searcher**: Finds and extracts information from the web.
        2. **Analyst**: Synthesizes and interprets the findings.
        3. **Writer**: Produces a clear, well-structured report.

        ---
        """
    )
    st.info(
        "Ask any research question in the chat below. The agent will search, analyze, and write a detailed report for you."
    )

    # Chat management buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🆕 New Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    with col2:
        if st.session_state.get("chat_history"):
            markdown_content = "# 🔎 Deep Research Agent - Chat History\n\n"
            for i, conversation in enumerate(st.session_state.chat_history, 1):
                markdown_content += f"## {conversation['question']}\n\n"
                markdown_content += f"{conversation['response']}\n\n"
                if i < len(st.session_state.chat_history):
                    markdown_content += "---\n\n"
            st.download_button(
                label="📥 Export Chat",
                data=markdown_content,
                file_name=f"deep_research_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown",
                use_container_width=True,
            )
        else:
            st.button("📥 Export Chat", use_container_width=True, disabled=True)

    st.markdown("---")
    st.caption("Built by DexterLab | Powered by Agno & Streamlit")

# --- SESSION STATE ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "trigger_research" not in st.session_state:
    st.session_state.trigger_research = None

# --- CHAT HISTORY ---
if st.session_state.chat_history:
    st.subheader("💬 Chat History")
    for i, conversation in enumerate(st.session_state.chat_history):
        with st.container():
            with st.chat_message("user"):
                st.write(conversation["question"])
            with st.chat_message("assistant"):
                st.markdown(conversation["response"])
                st.caption(f"Research completed at: {conversation['timestamp']}")
            if i < len(st.session_state.chat_history) - 1:
                st.divider()

# --- CHAT INPUT ---
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
        with st.status("Executing research plan...", expanded=True) as status:
            # PHASE 1: Researching
            phase1_msg = "🧠 **Phase 1: Researching** - Finding and extracting relevant information from the web..."
            status.write(phase1_msg)
            research_content = agent.searcher.run(user_input)
            # PHASE 2: Analyzing
            phase2_msg = "🔬 **Phase 2: Analyzing** - Synthesizing and interpreting the research findings..."
            status.write(phase2_msg)
            analysis = agent.analyst.run(research_content.content)
            # PHASE 3: Writing Report
            phase3_msg = "✍️ **Phase 3: Writing Report** - Producing a final, polished report..."
            status.write(phase3_msg)
            report_iterator = agent.writer.run(analysis.content, stream=True)
        # Collect the full report
        full_report = ""
        report_container = st.empty()
        with st.spinner("🤔 Thinking..."):
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