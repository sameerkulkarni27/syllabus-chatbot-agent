from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
from agent.tools import initialize_tools
from agent.prompt import SYSTEM_PROMPT
from config import LLM_MODEL
import asyncio

async def run_agent(vector_store):
    """Run the interactive agent."""
    print("Syllabus RAG Chatbot Assistant")
    print("=" * 50)
    
    # Create agent with injected values in prompt
    agent = create_agent(
        model=LLM_MODEL,
        tools=initialize_tools(vector_store),
        system_prompt=SYSTEM_PROMPT,
        checkpointer=MemorySaver()
    )
        
    while True:
        user_input = input("You: ").strip()
        
        if not user_input:
            continue

        try:
            response = await agent.ainvoke(
                {"messages": [{"role": "user", "content": user_input}]},
                config={
                    "configurable": {
                        "thread_id": "syllabus_chat"
                    }
                }
            )
            
            ai_message = response["messages"][-1].content
            print(f"Agent: {ai_message}\n")
            
        except Exception as e:
            print(f"[AGENT ERROR] Failed to invoke LLM: {str(e)}\n")

if __name__ == "__main__":
    asyncio.run(run_agent())
