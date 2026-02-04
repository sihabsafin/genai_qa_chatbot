from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
import streamlit as st
import os

# Global LLM instance
llm = None
current_config = {}

def initialize_llm(
    model: str = "llama-3.3-70b-versatile",
    temperature: float = 0.3,
    max_tokens: int = 2048,
    system_prompt: str = None
):
    """Initialize the Groq LLM with specified parameters"""
    global llm, current_config
    
    # Get API key from Streamlit secrets
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except:
        raise ValueError(
            "GROQ_API_KEY not found in Streamlit secrets. "
            "Please add it in your Streamlit Cloud dashboard."
        )
    
    try:
        # Initialize Groq LLM
        llm = ChatGroq(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            groq_api_key=api_key,
            streaming=False,
            max_retries=2,
            request_timeout=30,
        )
        
        current_config = {
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "system_prompt": system_prompt
        }
        
        return True
        
    except Exception as e:
        raise Exception(f"Failed to initialize LLM: {str(e)}")

def get_prompt_template(system_prompt: str = None):
    """Create prompt template with optional custom system prompt"""
    default_prompt = (
        "You are ContextIQ, an intelligent, professional, and helpful AI assistant. "
        "Answer clearly, concisely, and accurately. Provide detailed explanations when needed. "
        "Use proper formatting with markdown when appropriate. "
        "If you are unsure about something, honestly say you do not know."
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt or default_prompt),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])
    
    return prompt

def get_ai_response(
    user_input: str,
    chat_history: list,
    temperature: float = None,
    max_tokens: int = None,
    system_prompt: str = None
) -> str:
    """Generate AI response with conversation history"""
    global llm
    
    if llm is None:
        raise RuntimeError("LLM not initialized. Please restart the app.")
    
    try:
        # Update LLM settings if provided
        if temperature is not None and temperature != current_config.get("temperature"):
            llm.temperature = temperature
        
        if max_tokens is not None and max_tokens != current_config.get("max_tokens"):
            llm.max_tokens = max_tokens
        
        # Get prompt template
        prompt = get_prompt_template(system_prompt)
        
        # Format messages with history
        messages = prompt.format_messages(
            history=chat_history[:-1],  # Exclude current user message
            input=user_input
        )
        
        # Invoke LLM
        response = llm.invoke(messages)
        return response.content
        
    except Exception as e:
        error_str = str(e).lower()
        
        # Provide helpful error messages
        if "rate_limit" in error_str or "rate limit" in error_str:
            return (
                "⚠️ **Rate Limit Reached**\n\n"
                "Please wait a moment and try again. Groq has generous free tier limits, "
                "but they do apply per minute."
            )
        elif "api_key" in error_str or "authentication" in error_str:
            return (
                "⚠️ **API Key Issue**\n\n"
                "Please check that your GROQ_API_KEY is correctly set in Streamlit secrets."
            )
        elif "timeout" in error_str:
            return (
                "⚠️ **Request Timeout**\n\n"
                "The request took too long. Please try again or select a different model."
            )
        else:
            return f"⚠️ **Error**: {str(e)}\n\nPlease try again or contact support if the issue persists."
