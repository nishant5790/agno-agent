import base64
import json
import time
from datetime import datetime
from os import getenv

import streamlit as st
from agent.research_agent import DeepResearcherAgent
from agent.chat_agent import agent
from agent.youtube_agent import  youtube_agent


st.set_page_config(
    page_title="Aion AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --- HEADER ---
st.markdown(
    """
    <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 0;">
        <span style="font-size:2.5rem;">🤖</span>
        <div>
            <h1 style="margin-bottom: 0.2em;">Aion AI</h1>
            <div style="font-size:1.1rem; color: #666;">
                Multi-agent AI system for research, chat, and youtube analyser.
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.divider()


# --- SIDEBAR ---
with st.sidebar:
    st.header("Aion Agents")
    st.markdown(
        """
        **Aion AI** offers:
        1. **Research Agent**: Multi-stage AI workflow for research and reporting.
        2. **Chat Agent**: Normal chat with AI.
        3. **Youtube Analyser**: For analysing youtube video .
        ---
        """
    )
    st.info("Choose a tab above to interact with different agents.")
    st.markdown("---")
    st.caption("Built by DexterLab")


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
    st.subheader("💬 Chat Agent")
    st.caption("Chat with the AI agent.")
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
                    st.caption(f"Chat at: {conversation['timestamp']}")
                if i < len(st.session_state.chat_tab_history) - 1:
                    st.divider()
    chat_input = st.chat_input("Type your message...")
    if chat_input:
        try:
            chat_response = agent.run(chat_input,stream=True)
            full_report = ""
            report_container = st.empty()
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
    st.subheader("� Deep Research Agent")
    st.caption("Multi-stage AI workflow for comprehensive research, analysis, and reporting.")
    # Chat history for research agent
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

# --- Youtube Analyser Tab ---
with tab3:
    st.subheader("� Youtube Analyser")
    st.caption("Paste a YouTube link below and get an AI-powered analysis of the video.")
    youtube_link = st.text_input("Enter YouTube video link...")
    if youtube_link:
        try:
            with st.spinner("Analyzing video..."):
                analysis_result = youtube_agent.run(youtube_link,stream=True)

                full_report = ""
                report_container = st.empty()
                for chunk in  analysis_result:
                    if chunk.content:
                        full_report += chunk.content
                        report_container.markdown(full_report)
                # st.markdown(analysis_result)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")