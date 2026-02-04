import streamlit as st
from llm_engine import get_ai_response, initialize_llm
from pathlib import Path
from langchain_core.messages import HumanMessage, AIMessage
import time
from datetime import datetime

# Page config
st.set_page_config(
    page_title="ContextIQ - AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
css_path = Path("assets/style.css")
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    
    # Model selection
    model_option = st.selectbox(
        "🤖 AI Model",
        [
            "llama-3.3-70b-versatile",
            "llama-3.1-70b-versatile", 
            "mixtral-8x7b-32768",
            "gemma2-9b-it"
        ],
        index=0,
        help="Llama 3.3 70B is most powerful"
    )
    
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
    
    # System prompt
    with st.expander("🎯 System Prompt"):
        custom_system_prompt = st.text_area(
            "Customize AI behavior",
            value="You are ContextIQ, an intelligent and helpful AI assistant. Answer clearly, accurately, and concisely.",
            height=100
        )
    
    st.divider()
    
    # Clear button
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.lc_history = []
        st.rerun()
    
    # Stats
    st.divider()
    st.markdown("### 📊 Session Stats")
    if "messages" in st.session_state:
        user_msgs = len([m for m in st.session_state.messages if m["role"] == "user"])
        bot_msgs = len([m for m in st.session_state.messages if m["role"] == "assistant"])
        st.metric("Your Messages", user_msgs)
        st.metric("AI Responses", bot_msgs)
    
    st.divider()
    st.caption("⚡ Powered by Groq")
    st.caption("🔗 Built with LangChain")
    st.caption("🚀 Hosted on Streamlit")

# Header
st.markdown("""
<div style='text-align: center; padding: 20px 0;'>
    <h1 style='color: #6366f1; margin-bottom: 0;'>🤖 ContextIQ</h1>
    <p style='font-size: 18px; color: #666; margin-top: 5px;'>Your Intelligent AI Assistant</p>
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

# Initialize LLM
if not st.session_state.llm_initialized or st.session_state.current_model != model_option:
    try:
        with st.spinner("🔄 Initializing AI model..."):
            initialize_llm(
                model=model_option,
                temperature=temperature,
                max_tokens=max_tokens,
                system_prompt=custom_system_prompt
            )
            st.session_state.llm_initialized = True
            st.session_state.current_model = model_option
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.info("💡 Make sure your GROQ_API_KEY is set in Streamlit secrets")
        st.stop()

# Display welcome message or chat history
if not st.session_state.messages:
    st.markdown("""
    <div style='text-align: center; padding: 60px 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; color: white; margin: 20px 0;'>
        <h2 style='margin-bottom: 20px;'>👋 Welcome to ContextIQ!</h2>
        <p style='font-size: 18px; margin-bottom: 30px;'>Your powerful AI assistant is ready to help</p>
        <div style='display: flex; justify-content: center; gap: 30px; flex-wrap: wrap;'>
            <div style='text-align: center;'>
                <div style='font-size: 32px; margin-bottom: 10px;'>💻</div>
                <div>Coding Help</div>
            </div>
            <div style='text-align: center;'>
                <div style='font-size: 32px; margin-bottom: 10px;'>✍️</div>
                <div>Writing</div>
            </div>
            <div style='text-align: center;'>
                <div style='font-size: 32px; margin-bottom: 10px;'>🔍</div>
                <div>Research</div>
            </div>
            <div style='text-align: center;'>
                <div style='font-size: 32px; margin-bottom: 10px;'>💡</div>
                <div>Ideas</div>
            </div>
        </div>
        <p style='margin-top: 30px; font-size: 14px; opacity: 0.9;'>Start chatting below!</p>
    </div>
    """, unsafe_allow_html=True)
else:
    # Display chat messages
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
            st.markdown(
                f"""
                <div class='chat-bubble-bot'>
                    <strong>ContextIQ</strong><br/>
                    {msg['content']}
                </div>
                """,
                unsafe_allow_html=True
            )

# Chat input
user_input = st.chat_input("💬 Ask me anything...", key="user_input")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.lc_history.append(HumanMessage(content=user_input))
    
    # Generate AI response
    with st.spinner("🧠 Thinking..."):
        start_time = time.time()
        
        try:
            response = get_ai_response(
                user_input,
                st.session_state.lc_history,
                temperature=temperature,
                max_tokens=max_tokens,
                system_prompt=custom_system_prompt
            )
            
            response_time = time.time() - start_time
            
            # Add AI response
            st.session_state.messages.append({
                "role": "assistant",
                "content": response,
                "response_time": response_time
            })
            st.session_state.lc_history.append(AIMessage(content=response))
            
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}\n\nPlease try again."
            st.session_state.messages.append({
                "role": "assistant",
                "content": error_msg
            })
    
    st.rerun()

# Footer
st.markdown("""
<div style='text-align: center; padding: 30px 0 10px 0; color: #888; font-size: 13px; border-top: 1px solid #eee; margin-top: 40px;'>
    <p>Built with ❤️ using Groq, LangChain & Streamlit</p>
    <p style='margin-top: 5px;'>⚡ Ultra-fast AI responses • 🎯 Multiple models • 🎨 Beautiful interface</p>
</div>
""", unsafe_allow_html=True)
