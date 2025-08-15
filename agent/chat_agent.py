"""
ChatAgent: Handles normal chat interactions.
"""
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.duckduckgo import DuckDuckGoTools

agent = Agent(
    model=Gemini(id="gemini-2.0-flash"),
    add_history_to_messages=True,
    num_history_responses=3,
    instructions="you are a helpful assitant which will answer the user question.",
    markdown=True,
    show_tool_calls=False,
)





