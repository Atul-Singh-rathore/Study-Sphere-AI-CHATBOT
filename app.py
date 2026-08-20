import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq Client
try:
    if GROQ_API_KEY:
        client = Groq(api_key=GROQ_API_KEY)
    else:
        st.error("🔒 Configuration Error: GROQ_API_KEY is missing from the secure vault (.env).")
except Exception as e:
    st.error(f"Initialization Error: {e}")

# Premium Page Configuration
st.set_page_config(
    page_title="StudySphere Nexus - Advanced AI Learning", 
    page_icon="⚡",
    layout="wide"
)

# Custom Premium Glassmorphism UI Styling
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #f8fafc;
    }
    .stButton>button {
        background: linear-gradient(45deg, #4f46e5, #06b6d4);
        color: black;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(6, 182, 212, 0.4);
    }
    .sidebar .sidebar-content {
        background-color: #0f172a;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR CONTROL PANEL ---
with st.sidebar:
    st.image("https://img.icons8.com/fluent/96/000000/artificial-intelligence.png", width=80)
    st.markdown("## 🧠 StudySphere Core Settings")
    st.caption("Control your AI tutor's cognitive engine parameters.")
    
    st.markdown("---")
    
    # Model Selection Capability
    ai_model = st.selectbox(
        "Select AI Engine",
        ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"],
        index=0
    )
    
    # Creativity slider (Temperature)
    creativity = st.slider("Tutor Creativity (Temperature)", 0.0, 1.0, 0.7, step=0.1)
    
    st.markdown("---")
    
    # Control Actions
    if st.button("🔄 Reset Nexus Session"):
        st.session_state.messages = []
        st.rerun()

# --- MAIN INTERACTION INTERFACE ---
st.title("⚡ StudySphere Nexus")
st.markdown("##### *Next-Gen Autonomous AI Learning System*")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages with premium style formatting
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Quick Starter Cards (if chat history is empty)
if not st.session_state.messages:
    st.markdown("### 🚀 Quick Start Modules")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🧬 Quantum Physics Basics"):
            st.session_state.messages.append({"role": "user", "content": "Explain Quantum Physics using a simple analogy."})
            st.rerun()
    with col2:
        if st.button("💻 Optimize Python Code"):
            st.session_state.messages.append({"role": "user", "content": "Show me how to optimize Python loops for heavy data."})
            st.rerun()

# Handle Dynamic User Input
if prompt := st.chat_input("Transmit message to studysphere..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        # Dynamic Streamlined Generation
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are StudySphere Nexus, a premium, hyper-intelligent elite AI tutor. "
                        "Format your answers with professional markdown, use bold headings, "
                        "and structured bullet points to deliver highly readable academic insights."
                    ),
                },
                *st.session_state.messages
            ],
            model=ai_model,
            temperature=creativity
        )
        
        response_text = chat_completion.choices[0].message.content
        
        with st.chat_message("assistant"):
            st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})
        
    except Exception as e:
        st.error(f"❌ Core Exception Occurred: {e}")