"""
Web search integration using Tavily API
"""
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
import streamlit as st

def initialize_search_tool():
    """Initialize Tavily search tool"""
    try:
        api_key = st.secrets.get("TAVILY_API_KEY", "")
        if not api_key:
            return None
        
        search = TavilySearchResults(
            max_results=3,
            api_key=api_key
        )
        return search
    except Exception as e:
        st.error(f"Search initialization error: {str(e)}")
        return None

def search_web(query: str, llm) -> str:
    """
    Perform web search and return formatted results
    """
    try:
        search_tool = initialize_search_tool()
        if not search_tool:
            return "⚠️ Web search is not configured. Please add TAVILY_API_KEY to secrets."
        
        # Create agent prompt
        template = """You are a helpful AI assistant with access to web search.
        
Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take (use 'tavily_search_results_json' to search)
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Available tools:
{tools}

Tool names: {tool_names}

Question: {input}
{agent_scratchpad}"""

        prompt = PromptTemplate.from_template(template)
        
        # Create agent
        tools = [search_tool]
        agent = create_react_agent(llm, tools, prompt)
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
            max_iterations=3,
            handle_parsing_errors=True
        )
        
        # Execute search
        result = agent_executor.invoke({"input": query})
        return result.get("output", "No results found.")
        
    except Exception as e:
        return f"⚠️ Search error: {str(e)}"

def format_search_results(results: list) -> str:
    """Format search results for display"""
    if not results:
        return "No results found."
    
    formatted = "🔍 **Web Search Results:**\n\n"
    for i, result in enumerate(results, 1):
        title = result.get('title', 'No title')
        url = result.get('url', '#')
        snippet = result.get('snippet', 'No description')
        
        formatted += f"**{i}. {title}**\n"
        formatted += f"{snippet}\n"
        formatted += f"🔗 [{url}]({url})\n\n"
    
    return formatted
