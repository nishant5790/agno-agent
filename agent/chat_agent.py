"""
ChatAgent: Handles normal chat interactions.
"""
from agno.agent import Agent
from agno.models.google import Gemini

agent = Agent(
    model=Gemini(id="gemini-2.0-flash"),
    add_history_to_messages=True,
    num_history_responses=3,
    instructions="you are a helpful assitant which will answer the user question.",
    markdown=True,
)


# class ChatAgent:
#     def __init__(self):
#         pass

#     def run(self,message:str) -> str:
#         # Placeholder for chat logic, can be replaced with LLM integration
#         return agent.run(message=message, stream=True)




