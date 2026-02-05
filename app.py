import streamlit as st
from llm_engine import get_ai_response, initialize_llm, regenerate_response
from database import Database
from pdf_generator import generate_user_guide_pdf
from web_search import search_web
from pathlib import Path
from langchain_core.messages import HumanMessage, AIMessage
import time
from datetime import datetime
import json
import base64

# Page config
st.set_page_config(
    page_title="ContextIQ - AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
@st.cache_resource
def get_database():
    return Database()

db = get_database()

# Initialize theme in session state (dark mode by default)
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "dark"

# Load CSS based on theme
css_file = "assets/style-dark.css" if st.session_state.theme_mode == "dark" else "assets/style-light.css"
css_path = Path(css_file)
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

# Additional CSS for new features
st.markdown("""
<style>
.action-button {
    display: inline-block;
    padding: 5px 10px;
    margin: 5px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 12px;
}
.copy-btn {
    background: #4CAF50;
    color: white;
}
.regenerate-btn {
    background: #2196F3;
    color: white;
}
.export-btn {
    background: #FF9800;
    color: white;
}
.conversation-item {
    padding: 10px;
    margin: 5px 0;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s;
}
.conversation-item:hover {
    background: rgba(102, 126, 234, 0.1);
}
.search-badge {
    display: inline-block;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 10px;
    margin-left: 5px;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    
    # Theme toggle
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("**Theme Mode**")
    with col2:
        theme_icon = "☀️" if st.session_state.theme_mode == "dark" else "🌙"
        if st.button(theme_icon, key="theme_toggle", help="Toggle theme"):
            st.session_state.theme_mode = "light" if st.session_state.theme_mode == "dark" else "dark"
            st.rerun()
    
    st.divider()
    
    # Model selection with proper names
    model_option = st.selectbox(
        "🤖 AI Model",
        [
            "llama-3.3-70b-versatile",
            "llama-3.1-70b-versatile", 
            "mixtral-8x7b-32768",
            "gemma2-9b-it"
        ],
        index=0,
        help="Choose the AI model for your conversation"
    )
    
    # Model descriptions
    model_info = {
        "llama-3.3-70b-versatile": "⭐ Most powerful - Best for complex tasks",
        "llama-3.1-70b-versatile": "🚀 Fast & reliable - Great all-rounder",
        "mixtral-8x7b-32768": "🎨 Creative - Excellent for writing",
        "gemma2-9b-it": "⚡ Quick - Fast responses"
    }
    st.caption(model_info.get(model_option, ""))
    
    # Temperature
    temperature = st.slider(
        "🌡️ Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.3,
        step=0.1,
        help="Lower = focused, Higher = creative"
    )
    
    # Max tokens
    max_tokens = st.slider(
        "📏 Max Length",
        min_value=512,
        max_value=4096,
        value=2048,
        step=512,
        help="Maximum response length"
    )
    
    # Web search toggle
    enable_web_search = st.checkbox(
        "🔍 Enable Web Search",
        value=False,
        help="Get real-time information from the web"
    )
    
    # Streaming toggle
    enable_streaming = st.checkbox(
        "💬 Streaming Responses",
        value=True,
        help="See responses as they're generated"
    )
    
    # System prompt
    with st.expander("🎯 System Prompt"):
        custom_system_prompt = st.text_area(
            "Customize AI behavior",
            value="You are ContextIQ, an intelligent and helpful AI assistant. Answer clearly, accurately, and concisely.",
            height=100
        )
    
    st.divider()
    
    # Conversation management
    st.markdown("### 💾 Conversations")
    
    # New conversation button
    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.lc_history = []
        st.session_state.current_conversation_id = None
        st.rerun()
    
    # Search conversations
    search_query = st.text_input("🔍 Search conversations", placeholder="Search...")
    
    # Load conversation history
    if search_query:
        conversations = db.search_conversations(search_query)
    else:
        conversations = db.get_all_conversations()
    
    # Display conversations
    if conversations:
        st.markdown("**Recent Chats:**")
        for conv in conversations[:10]:  # Show last 10
            col1, col2 = st.columns([4, 1])
            with col1:
                if st.button(
                    f"💬 {conv['title'][:25]}...", 
                    key=f"load_{conv['id']}",
                    use_container_width=True
                ):
                    # Load conversation
                    loaded = db.get_conversation(conv['id'])
                    if loaded:
                        st.session_state.messages = loaded['messages']
                        st.session_state.lc_history = []
                        for msg in loaded['messages']:
                            if msg['role'] == 'user':
                                st.session_state.lc_history.append(HumanMessage(content=msg['content']))
                            else:
                                st.session_state.lc_history.append(AIMessage(content=msg['content']))
                        st.session_state.current_conversation_id = conv['id']
                        st.rerun()
            with col2:
                if st.button("🗑️", key=f"del_{conv['id']}", help="Delete"):
                    db.delete_conversation(conv['id'])
                    st.rerun()
    
    st.divider()
    
    # Export conversation
    if st.session_state.get("messages"):
        st.markdown("### 📤 Export")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📄 TXT", use_container_width=True):
                # Export as text
                text_content = f"ContextIQ Conversation\nExported: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
                for msg in st.session_state.messages:
                    role = "You" if msg['role'] == 'user' else "ContextIQ"
                    text_content += f"{role}:\n{msg['content']}\n\n"
                
                st.download_button(
                    "💾 Download TXT",
                    text_content,
                    file_name=f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
        
        with col2:
            if st.button("📑 JSON", use_container_width=True):
                # Export as JSON
                json_content = json.dumps(st.session_state.messages, indent=2)
                st.download_button(
                    "💾 Download JSON",
                    json_content,
                    file_name=f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
    
    st.divider()
    
    # User Guide button - Generate PDF
    if st.button("📚 Download User Guide (PDF)", use_container_width=True):
        with st.spinner("Generating PDF..."):
            pdf_path = generate_user_guide_pdf()
            with open(pdf_path, "rb") as pdf_file:
                pdf_bytes = pdf_file.read()
                st.download_button(
                    label="💾 Download PDF Guide",
                    data=pdf_bytes,
                    file_name="ContextIQ_User_Guide.pdf",
                    mime="application/pdf"
                )
    
    # Stats
    st.divider()
    st.markdown("### 📊 Session Stats")
    if "messages" in st.session_state:
        user_msgs = len([m for m in st.session_state.messages if m["role"] == "user"])
        bot_msgs = len([m for m in st.session_state.messages if m["role"] == "assistant"])
        st.metric("Your Messages", user_msgs)
        st.metric("AI Responses", bot_msgs)
        
        # Total conversations in database
        total_convs = len(db.get_all_conversations())
        st.metric("Total Conversations", total_convs)
    
    st.divider()
    st.caption("⚡ Powered by Groq")
    st.caption("🔗 Built with LangChain")
    st.caption("📊 Tracked with LangSmith")
    st.caption("🚀 Hosted on Streamlit")

# Header
header_gradient = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)" if st.session_state.theme_mode == "dark" else "linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)"
st.markdown(f"""
<div style='text-align: center; padding: 20px 0;'>
    <h1 style='background: {header_gradient}; -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0;'>🤖 ContextIQ</h1>
    <p style='font-size: 18px; color: #888; margin-top: 5px;'>Your Intelligent AI Assistant with Web Search & Memory</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "lc_history" not in st.session_state:
    st.session_state.lc_history = []

if "llm_initialized" not in st.session_state:
    st.session_state.llm_initialized = False

if "current_model" not in st.session_state:
    st.session_state.current_model = None

if "current_conversation_id" not in st.session_state:
    st.session_state.current_conversation_id = None

if "regenerate_index" not in st.session_state:
    st.session_state.regenerate_index = None

# Initialize LLM
if not st.session_state.llm_initialized or st.session_state.current_model != model_option:
    try:
        with st.spinner("🔄 Initializing AI model..."):
            initialize_llm(
                model=model_option,
                temperature=temperature,
                max_tokens=max_tokens,
                system_prompt=custom_system_prompt,
                streaming=enable_streaming
            )
            st.session_state.llm_initialized = True
            st.session_state.current_model = model_option
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.info("💡 Make sure your GROQ_API_KEY is set in .streamlit/secrets.toml")
        st.code("""
# .streamlit/secrets.toml
GROQ_API_KEY = "your_api_key_here"
TAVILY_API_KEY = "your_tavily_key_here"  # Optional, for web search
LANGSMITH_API_KEY = "your_langsmith_key_here"  # Optional, for tracing
        """)
        st.stop()

# Display welcome message or chat history
if not st.session_state.messages:
    welcome_bg = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)" if st.session_state.theme_mode == "dark" else "linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)"
    st.markdown(f"""
    <div style='text-align: center; padding: 60px 20px; background: {welcome_bg}; border-radius: 15px; color: white; margin: 20px 0;'>
        <h2 style='margin-bottom: 20px;'>👋 Welcome to ContextIQ!</h2>
        <p style='font-size: 18px; margin-bottom: 30px;'>Your powerful AI assistant with advanced features</p>
        <div style='display: flex; justify-content: center; gap: 30px; flex-wrap: wrap;'>
            <div style='text-align: center;'>
                <div style='font-size: 32px; margin-bottom: 10px;'>💻</div>
                <div>Coding Help</div>
            </div>
            <div style='text-align: center;'>
                <div style='font-size: 32px; margin-bottom: 10px;'>🔍</div>
                <div>Web Search</div>
            </div>
            <div style='text-align: center;'>
                <div style='font-size: 32px; margin-bottom: 10px;'>💾</div>
                <div>Save History</div>
            </div>
            <div style='text-align: center;'>
                <div style='font-size: 32px; margin-bottom: 10px;'>💬</div>
                <div>Streaming</div>
            </div>
        </div>
        <p style='margin-top: 30px; font-size: 14px; opacity: 0.9;'>Download the User Guide PDF from the sidebar!</p>
    </div>
    """, unsafe_allow_html=True)
else:
    # Display chat messages with action buttons
    for i, msg in enumerate(st.session_state.messages):
        if msg["role"] == "user":
            st.markdown(
                f"""
                <div class='chat-bubble-user'>
                    <strong>You</strong><br/>
                    {msg['content']}
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            # Create columns for message and action buttons
            col1, col2 = st.columns([5, 1])
            
            with col1:
                # Show web search badge if used
                web_search_badge = ""
                if msg.get('web_search_used'):
                    web_search_badge = "<span class='search-badge'>🔍 Web Search</span>"
                
                st.markdown(
                    f"""
                    <div class='chat-bubble-bot'>
                        <strong>ContextIQ</strong> {web_search_badge}<br/>
                        {msg['content']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            with col2:
                # Copy button
                if st.button("📋", key=f"copy_{i}", help="Copy response"):
                    st.code(msg['content'], language=None)
                    st.success("✅ Copied!")
                
                # Regenerate button (only for last message)
                if i == len(st.session_state.messages) - 1:
                    if st.button("🔄", key=f"regen_{i}", help="Regenerate"):
                        st.session_state.regenerate_index = i
                        st.rerun()

# Handle regeneration
if st.session_state.regenerate_index is not None:
    idx = st.session_state.regenerate_index
    if idx > 0:
        # Get the user message that prompted this response
        user_msg = st.session_state.messages[idx - 1]['content']
        
        # Remove last AI response
        st.session_state.messages.pop()
        st.session_state.lc_history.pop()
        
        # Regenerate
        with st.spinner("🔄 Regenerating response..."):
            start_time = time.time()
            
            try:
                if enable_streaming:
                    stream_container = st.empty()
                    response = regenerate_response(
                        user_msg,
                        st.session_state.lc_history,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        system_prompt=custom_system_prompt,
                        streaming=True,
                        stream_container=stream_container
                    )
                else:
                    response = regenerate_response(
                        user_msg,
                        st.session_state.lc_history,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        system_prompt=custom_system_prompt,
                        streaming=False
                    )
                
                response_time = time.time() - start_time
                
                # Add new AI response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response,
                    "response_time": response_time,
                    "regenerated": True
                })
                st.session_state.lc_history.append(AIMessage(content=response))
                
            except Exception as e:
                error_msg = f"❌ Error regenerating: {str(e)}"
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg
                })
        
        st.session_state.regenerate_index = None
        st.rerun()

# Chat input
user_input = st.chat_input("💬 Ask me anything... (Enable web search for current info!)", key="user_input")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.lc_history.append(HumanMessage(content=user_input))
    
    # Determine if we should use web search
    use_web_search = enable_web_search
    
    # Generate AI response
    if enable_streaming:
        stream_container = st.empty()
        stream_container.markdown("🧠 Thinking...")
    
    with st.spinner("🧠 Processing..."):
        start_time = time.time()
        
        try:
            # Check if web search should be used
            if use_web_search:
                # Use web search
                from llm_engine import llm
                response = search_web(user_input, llm)
                web_search_used = True
            else:
                # Regular response
                if enable_streaming:
                    response = get_ai_response(
                        user_input,
                        st.session_state.lc_history,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        system_prompt=custom_system_prompt,
                        streaming=True,
                        stream_container=stream_container
                    )
                else:
                    response = get_ai_response(
                        user_input,
                        st.session_state.lc_history,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        system_prompt=custom_system_prompt,
                        streaming=False
                    )
                web_search_used = False
            
            response_time = time.time() - start_time
            
            # Add AI response
            st.session_state.messages.append({
                "role": "assistant",
                "content": response,
                "response_time": response_time,
                "web_search_used": web_search_used
            })
            st.session_state.lc_history.append(AIMessage(content=response))
            
            # Auto-save conversation
            if st.session_state.current_conversation_id is None:
                # Create new conversation
                title = user_input[:50] if len(user_input) <= 50 else user_input[:47] + "..."
                conv_id = db.create_conversation(title, model_option)
                st.session_state.current_conversation_id = conv_id
            
            # Update conversation
            db.update_conversation(
                st.session_state.current_conversation_id,
                st.session_state.messages
            )
            
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}\n\nPlease try again."
            st.session_state.messages.append({
                "role": "assistant",
                "content": error_msg
            })
    
    st.rerun()
