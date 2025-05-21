"""
Lynk.ai Feature Creator Agent

This module creates a LangGraph agent that helps users create Lynk.ai feature YAML files.
The agent supports creating four types of features: Metric, First-Last, Formula, and Field.
"""
import uuid

# LangChain imports
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

# LangGraph imports
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent
from langgraph.graph.graph import CompiledGraph
# from langchain_core.messages.utils import (
#     trim_messages, 
#     count_tokens_approximately
# )
# from langgraph.prebuilt.chat_agent_executor import AgentState

from src.tools import setup_tools
from src.prompt import SYSTEM_PROMPT
from langgraph.store.memory import InMemoryStore
from langgraph.utils.config import get_store 
from langmem import (
    create_manage_memory_tool,
    create_search_memory_tool
)


# def pre_model_hook_trim_messages(state):
#     trimmed_messages = trim_messages(
#         state["messages"],
#         strategy="last",
#         token_counter=count_tokens_approximately,
#         max_tokens=384,
#         start_on="human",
#         end_on=("human", "tool"),
#     )
#     # return {"messages": [RemoveMessage(REMOVE_ALL_MESSAGES)] + trimmed_messages}
#     return {"llm_input_messages": trimmed_messages}
    





store = InMemoryStore(
    index={
        "dims": 1536,
        "embed": "openai:text-embedding-3-small",
    }
) 

checkpointer = InMemorySaver()



def adapt_prompt(state):
    """Prepare the messages for the LLM."""
    
    store = get_store() 

    memories = store.search(
        ("Lynk_Agent", "{user_id}", "YAML_description")
    )

    memories_str = "\n".join([f"Memory {i+1}: {memory.values['content']}" for i, memory in enumerate(memories)])
    system_msg = SYSTEM_PROMPT.format(memories=memories_str)
    return [{"role": "system", "content": system_msg}, *state["messages"]]


def create_agent():
    """Create the Lynk.ai Feature Creator Agent."""
    
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
    )
    
    tools = setup_tools()
    tools.append(create_manage_memory_tool(("Lynk_Agent", "{user_id}", "YAML_description")))
    tools.append(create_search_memory_tool(("Lynk_Agent", "{user_id}", "YAML_description")))

    agent = create_react_agent(
        model=llm,
        tools=tools,
        checkpointer=checkpointer,
        store=store,
        prompt=adapt_prompt,
        # pre_model_hook=pre_model_hook_trim_messages,
    )

    return agent
    
    


def process_input(agent: CompiledGraph, user_input: str, session_id: str, user_id: str, last_message: bool = False):
    """Process user input and return a response."""
    
    # Initial state
    state = {
        "messages": [HumanMessage(content=user_input)],
    }
    
    # Run the agent with the input
    result = agent.invoke(state, {"configurable": {"thread_id": session_id, "user_id": user_id}})
    
    if last_message:
        # Extract the AI message from the result
        response = result["messages"][-1].content
    else:
        return result
    
    return response


if __name__ == "__main__":
    # Simple interactive console for testing
    print("Lynk.ai Feature Creator Agent")
    print("Type 'exit' to quit")
    
    session_id = str(uuid.uuid4())

    user_id = input("Enter your client name [TPC-H]: ") or "TPC-H"

    agent = create_agent()
    
    while True:
        user_input = input("\nUser: ")
        if user_input.lower() == "exit":
            break
        
        response = process_input(agent, user_input, session_id, user_id, last_message=False)
        if isinstance(response, str):
            print(f"\nAgent: {response}") 
        else:
            print("########################")
            for message in response["messages"]:
                message.pretty_print()
            print("########################")