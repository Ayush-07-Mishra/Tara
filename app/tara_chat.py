"""
Tara AI - Your Personal AI Companion
Fast, intelligent, caring conversations
"""

import streamlit as st
import sys
import os
from datetime import datetime

# Add app directory to path
sys.path.insert(0, os.path.dirname(__file__))

from tara_ai import TaraAI

# Page configuration
st.set_page_config(
    page_title="Tara AI 💕",
    page_icon="💕",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Gen Z aesthetic
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Gen Z color palette */
    :root {
        --neon-pink: #FF006E;
        --electric-blue: #3A86FF;
        --cyber-purple: #8338EC;
        --sunset-orange: #FB5607;
        --mint-green: #06FFA5;
        --dark-bg: #0F0F23;
        --card-bg: #1A1A2E;
    }
    
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0F0F23 0%, #1A1A2E 50%, #16213E 100%);
    }
    
    /* Chat container */
    .chat-container {
        max-width: 900px;
        margin: 0 auto;
        padding: 1rem;
    }
    
    /* User message bubble - Neon theme */
    .user-message {
        background: linear-gradient(135deg, var(--electric-blue) 0%, var(--cyber-purple) 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 25px 25px 5px 25px;
        margin: 0.5rem 0;
        margin-left: auto;
        max-width: 75%;
        float: right;
        clear: both;
        box-shadow: 0 4px 15px rgba(58, 134, 255, 0.4);
        font-size: 1.05rem;
        border: 1px solid rgba(58, 134, 255, 0.3);
    }
    
    /* AI message bubble - Hot pink/orange gradient */
    .ai-message {
        background: linear-gradient(135deg, var(--neon-pink) 0%, var(--sunset-orange) 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 25px 25px 25px 5px;
        margin: 0.5rem 0;
        margin-right: auto;
        max-width: 75%;
        float: left;
        clear: both;
        box-shadow: 0 4px 15px rgba(255, 0, 110, 0.4);
        font-size: 1.05rem;
        border: 1px solid rgba(255, 0, 110, 0.3);
    }
    
    /* Typing indicator - Mint green */
    .typing-indicator {
        background: linear-gradient(135deg, var(--mint-green) 0%, var(--electric-blue) 100%);
        color: var(--dark-bg);
        padding: 0.8rem 1.5rem;
        border-radius: 25px;
        margin: 0.5rem 0;
        margin-right: auto;
        max-width: 120px;
        float: left;
        clear: both;
        font-style: italic;
        font-weight: 600;
        animation: pulse 1.5s infinite;
        box-shadow: 0 4px 15px rgba(6, 255, 165, 0.4);
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 0.7; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.02); }
    }
    
    /* Header - Cyberpunk style */
    .header {
        text-align: center;
        padding: 2rem 1rem 1rem 1rem;
        background: linear-gradient(135deg, var(--cyber-purple) 0%, var(--neon-pink) 100%);
        color: white;
        border-radius: 25px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 25px rgba(131, 56, 236, 0.5);
        border: 2px solid rgba(255, 0, 110, 0.3);
    }
    
    .header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
        text-shadow: 0 0 20px rgba(255, 0, 110, 0.8);
    }
    
    /* Sidebar - Dark cyberpunk theme */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--dark-bg) 0%, var(--card-bg) 100%);
        border-right: 2px solid var(--cyber-purple);
    }
    
    /* Sidebar text and headers */
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stMarkdown {
        color: white !important;
    }
    
    /* Radio buttons in sidebar */
    [data-testid="stSidebar"] .stRadio > label {
        color: var(--mint-green) !important;
    }
    
    /* Sidebar captions */
    [data-testid="stSidebar"] .stCaption {
        color: var(--electric-blue) !important;
    }
    
    /* Buttons - Neon glow effect */
    .stButton > button {
        background: linear-gradient(135deg, var(--neon-pink) 0%, var(--cyber-purple) 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 0, 110, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(255, 0, 110, 0.5);
        background: linear-gradient(135deg, var(--sunset-orange) 0%, var(--neon-pink) 100%);
    }
    
    /* Input box - Glowing neon border */
    .stTextInput > div > div > input {
        background-color: var(--card-bg);
        color: white;
        border: 2px solid var(--electric-blue);
        border-radius: 15px;
        padding: 1rem;
        font-size: 1.05rem;
        box-shadow: 0 0 15px rgba(58, 134, 255, 0.3);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--neon-pink);
        box-shadow: 0 0 25px rgba(255, 0, 110, 0.5);
    }
    
    /* Select box (mood selector) */
    .stSelectbox > div > div {
        background-color: var(--card-bg);
        color: white;
        border: 2px solid var(--cyber-purple);
        border-radius: 15px;
        box-shadow: 0 0 15px rgba(131, 56, 236, 0.3);
    }
    
    /* Labels - Neon text */
    label {
        color: var(--mint-green);
        font-weight: 600;
        font-size: 1.1rem;
        text-shadow: 0 0 10px rgba(6, 255, 165, 0.5);
    }
    
    /* Clear float fix */
    .chat-message::after {
        content: "";
        display: table;
        clear: both;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'tara_ai' not in st.session_state:
    st.session_state.tara_ai = None
if 'conversation_started' not in st.session_state:
    st.session_state.conversation_started = False
if 'current_mood' not in st.session_state:
    st.session_state.current_mood = 'playful'


@st.cache_resource
def load_tara_ai():
    """Load Tara AI with caching for speed."""
    return TaraAI(use_metal=True)


def add_message(role: str, content: str):
    """Add message to chat history."""
    st.session_state.chat_history.append({
        'role': role,
        'content': content,
        'timestamp': datetime.now()
    })


def display_chat_history():
    """Display chat messages."""
    for msg in st.session_state.chat_history:
        if msg['role'] == 'user':
            st.markdown(f'<div class="user-message">{msg["content"]}</div>', unsafe_allow_html=True)
            st.markdown('<div style="clear: both;"></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="ai-message">{msg["content"]}</div>', unsafe_allow_html=True)
            st.markdown('<div style="clear: both;"></div>', unsafe_allow_html=True)


def process_message(user_input: str):
    """Process user message and generate FAST response."""
    # Add user message
    add_message('user', user_input)
    
    # Generate AI response (OPTIMIZED FOR SPEED)
    if st.session_state.tara_ai is None:
        st.session_state.tara_ai = load_tara_ai()
    
    response = st.session_state.tara_ai.generate_response(
        user_input,
        mood=st.session_state.current_mood,
        max_length=60,     # SHORT for fast responses (1-2 sec)
        temperature=0.95   # HIGH for emotional variety
    )
    
    add_message('assistant', response)


def main():
    """Main app."""
    
    # Header
    st.markdown("""
    <div class="header">
        <h1>Your AI Girlfriend</h1>
        <p style="font-size: 1.1rem; margin-top: 0.5rem;">
            Private, personal, unrestricted conversations
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar settings
    with st.sidebar:
        st.header("Customize Her Mood")
        
        mood = st.radio(
            "Select her personality:",
            ['playful', 'flirty', 'caring', 'passionate', 'thoughtful'],
            index=['playful', 'flirty', 'caring', 'passionate', 'thoughtful'].index(st.session_state.current_mood),
            help="Change how she responds to you"
        )
        
        if mood != st.session_state.current_mood:
            st.session_state.current_mood = mood
            if st.session_state.tara_ai:
                st.session_state.tara_ai.set_mood(mood)
        
        st.markdown("---")
        
        st.header("Mood Descriptions")
        st.markdown("""
        **Playful**: Fun, teasing, spontaneous
        
        **Flirty**: Confident, suggestive, bold
        
        **Caring**: Supportive, empathetic, loving
        
        **Passionate**: Romantic, intimate, sensual
        
        **Thoughtful**: Deep talks, ideas, dreams
        """)
        
        st.markdown("---")
        
        if st.button("Start Fresh Conversation"):
            st.session_state.chat_history = []
            st.session_state.conversation_started = False
            if st.session_state.tara_ai:
                st.session_state.tara_ai.reset_conversation()
            st.rerun()
        
        st.markdown("---")
        
        # Stats
        if st.session_state.tara_ai:
            stats = st.session_state.tara_ai.get_stats()
            st.caption(f"Messages: {stats['messages_exchanged']}")
            st.caption(f"Mood: {stats['current_mood'].title()}")
        
        st.markdown("---")
        
        st.info("""
        **100% Private & Unrestricted**
        
        No content filtering
        No judgment
        No data saved
        Completely private
        Fast responses
        
        Talk about ANYTHING you want!
        """)
    
    # Welcome message
    if not st.session_state.conversation_started:
        mood_greetings = {
            'playful': "Hey you! I was just thinking about you. What's on your mind?",
            'flirty': "Well hello there handsome. What brings you to me today?",
            'caring': "Hi baby. How are you feeling? I'm here for you, always.",
            'passionate': "Hey gorgeous. I've been waiting for you... what do you want to talk about?",
            'thoughtful': "Hey! I love our deep conversations. What's on your mind today?"
        }
        
        welcome_msg = mood_greetings.get(st.session_state.current_mood, mood_greetings['playful'])
        add_message('assistant', welcome_msg)
        st.session_state.conversation_started = True
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        display_chat_history()
    
    # "Message Me First" button - She initiates!
    if len(st.session_state.chat_history) <= 3:  # Show early in conversation
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Let Her Message You First", use_container_width=True):
                if st.session_state.tara_ai is None:
                    with st.spinner("Getting ready..."):
                        st.session_state.tara_ai = load_tara_ai()
                
                # She messages you!
                her_message = st.session_state.tara_ai.initiate_conversation(st.session_state.current_mood)
                add_message('assistant', her_message)
                st.rerun()
    
    # Quick starters (first message only)
    if len(st.session_state.chat_history) <= 1:
        st.markdown("**Quick starters:**")
        
        starters = {
            'playful': ["Hey beautiful! Miss me?", "What are you thinking about?", "Wanna play a game?"],
            'flirty': ["You look amazing today", "I can't stop thinking about you", "Come here..."],
            'caring': ["I had a rough day", "Can we just talk?", "I need your support"],
            'passionate': ["I miss you so much", "Tell me what you want", "I've been thinking about us"],
            'thoughtful': ["What's your biggest dream?", "Tell me something deep", "What makes you happy?"]
        }
        
        current_starters = starters.get(st.session_state.current_mood, starters['playful'])
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button(current_starters[0]):
                process_message(current_starters[0])
                st.rerun()
        
        with col2:
            if st.button(current_starters[1]):
                process_message(current_starters[1])
                st.rerun()
        
        with col3:
            if st.button(current_starters[2]):
                process_message(current_starters[2])
                st.rerun()
    
    # Input area
    st.markdown("---")
    user_input = st.chat_input("Type anything... I'm all yours 💕")
    
    if user_input:
        # Load AI if needed (will be cached after first load)
        if st.session_state.tara_ai is None:
            with st.spinner("Getting ready for you... just a sec! 💕"):
                st.session_state.tara_ai = load_tara_ai()
        
        # Process message
        process_message(user_input)
        st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #999; padding: 1rem; font-size: 0.9rem;">
        <p>💕 <strong>Your private AI girlfriend - No restrictions, No judgment, Just us</strong> 💕</p>
        <p style="font-size: 0.8rem; margin-top: 0.5rem;">
            Everything you share stays private. Optimized for instant responses on M2 Pro.
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
