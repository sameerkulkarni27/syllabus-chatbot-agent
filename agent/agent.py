from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from agent.tools import initialize_tools
from agent.prompt import SYSTEM_PROMPT
from config import LLM_MODEL, LLM_TEMPERATURE


async def run_agent(vector_store):
    """Run the interactive agent."""
    print("="*60)
    print("📚 Syllabus RAG Chatbot Assistant")
    print("="*60)
    print("Commands: 'quit' to exit\n")
    
    # Initialize LLM
    llm = ChatOpenAI(
        model=LLM_MODEL,
        temperature=LLM_TEMPERATURE
    )
    
    # Get tools
    tools = initialize_tools(vector_store)
    
    # Create prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    # Create agent
    agent = create_openai_tools_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)
    
    print(f"🤖 Agent ready (Model: {LLM_MODEL})\n")
    
    chat_history = []
        
    while True:
        user_input = input("You: ").strip()
        
        if not user_input:
            continue
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!")
            break
        
        print("\n🤔 Thinking...\n")
        
        try:
            response = await agent_executor.ainvoke({
                "input": user_input,
                "chat_history": chat_history
            })
            
            answer = response["output"]
            print(f"Agent: {answer}\n")
            
            # Update history
            chat_history.append(("human", user_input))
            chat_history.append(("ai", answer))
            
        except Exception as e:
            print(f"[AGENT ERROR] {str(e)}\n")


if __name__ == "__main__":
    print("Please run main.py to start the chatbot")