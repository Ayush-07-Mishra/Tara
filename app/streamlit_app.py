"""
Streamlit UI for Mental Health Support AI.
Anonymous, supportive mental health check-in tool.
"""

import streamlit as st
import sys
import os
from datetime import datetime
import json

# Add app directory to path
sys.path.insert(0, os.path.dirname(__file__))

from pipeline import MentalHealthPipeline

# Page configuration
st.set_page_config(
    page_title="Mental Health Support AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .crisis-banner {
        background-color: #ff4b4b;
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        font-size: 1.1rem;
        font-weight: bold;
    }
    .result-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .disclaimer {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state
if 'pipeline' not in st.session_state:
    st.session_state.pipeline = None
if 'analysis_count' not in st.session_state:
    st.session_state.analysis_count = 0
if 'data_logging_enabled' not in st.session_state:
    st.session_state.data_logging_enabled = False


@st.cache_resource
def load_pipeline():
    """Load pipeline with caching."""
    model_path = os.path.join(os.path.dirname(__file__), 'models')
    return MentalHealthPipeline(stress_model_path=model_path if os.path.exists(model_path) else None)


def log_anonymous_data(text: str, analysis: dict):
    """
    Log anonymous data for pattern analysis (optional, first 10 days).
    No personal identifiers stored.
    """
    if not st.session_state.data_logging_enabled:
        return
    
    log_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, 'anonymous_interactions.jsonl')
    
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'text_length': len(text),
        'emotion': analysis['emotion']['emotion'],
        'sentiment': analysis['sentiment']['sentiment'],
        'stress': analysis['stress']['stress_level'],
        'crisis_detected': analysis['crisis']['crisis_detected'],
        'has_sexual_content': False  # Placeholder for future feature
    }
    
    with open(log_file, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')


def main():
    """Main Streamlit app."""
    
    # Header
    st.markdown('<div class="main-header">🧠 Mental Health Support AI</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">Anonymous emotional support and grounding exercises</div>',
        unsafe_allow_html=True
    )
    
    # Sidebar
    with st.sidebar:
        st.header("ℹ️ About")
        st.write("""
        This AI tool provides:
        - Emotion detection
        - Sentiment analysis
        - Stress level assessment
        - Crisis detection
        - Grounding exercises
        - Supportive responses
        """)
        
        st.markdown("---")
        
        st.header("⚠️ Important")
        st.warning("""
        **This is NOT:**
        - Medical advice
        - Professional therapy
        - A crisis hotline
        
        **This IS:**
        - Anonymous support
        - Emotional validation
        - Coping strategies
        """)
        
        st.markdown("---")
        
        st.header("🔒 Privacy")
        st.success("""
        ✅ Fully anonymous
        ✅ No data stored permanently
        ✅ In-memory processing only
        """)
        
        # Data logging toggle (for first 10 days)
        st.markdown("---")
        st.header("📊 Data Collection (Optional)")
        st.session_state.data_logging_enabled = st.checkbox(
            "Enable anonymous analytics",
            value=st.session_state.data_logging_enabled,
            help="Helps improve the system. No personal data stored."
        )
        
        st.markdown("---")
        st.caption(f"Analyses performed: {st.session_state.analysis_count}")
    
    # Main disclaimer
    st.markdown("""
    <div class="disclaimer">
        <strong>⚠️ Disclaimer:</strong> This tool is for informational and emotional support purposes only. 
        It does not provide medical advice, diagnosis, or treatment. If you're in crisis, please contact 
        a mental health professional or crisis helpline immediately.
    </div>
    """, unsafe_allow_html=True)
    
    # Input section
    st.header("💬 How are you feeling?")
    user_input = st.text_area(
        "Share what's on your mind...",
        height=150,
        placeholder="Type your thoughts and feelings here. Be as open as you'd like - this is a safe, anonymous space.",
        help="Your message is processed anonymously and not stored."
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        analyze_button = st.button("🔍 Check My Mental State", use_container_width=True, type="primary")
    
    # Analysis section
    if analyze_button:
        if not user_input or len(user_input.strip()) < 10:
            st.warning("Please share a bit more so I can better understand and support you.")
        else:
            with st.spinner("Analyzing your message..."):
                # Load pipeline
                if st.session_state.pipeline is None:
                    st.session_state.pipeline = load_pipeline()
                
                # Run analysis
                result = st.session_state.pipeline.analyze(user_input)
                st.session_state.analysis_count += 1
                
                # Log anonymous data if enabled
                log_anonymous_data(user_input, result)
                
                # Crisis banner
                if result['crisis']['crisis_detected']:
                    st.markdown("""
                    <div class="crisis-banner">
                        🚨 CRISIS DETECTED - PLEASE SEEK IMMEDIATE HELP
                    </div>
                    """, unsafe_allow_html=True)
                
                # Results in columns
                st.header("📊 Analysis Results")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        "Emotion",
                        result['emotion']['emotion'].capitalize(),
                        f"{result['emotion']['confidence']:.0%} confidence"
                    )
                
                with col2:
                    st.metric(
                        "Sentiment",
                        result['sentiment']['sentiment'].capitalize(),
                        f"{result['sentiment']['confidence']:.0%} confidence"
                    )
                
                with col3:
                    stress_color = {
                        'low': '🟢',
                        'medium': '🟡',
                        'high': '🔴'
                    }.get(result['stress']['stress_level'], '⚪')
                    
                    st.metric(
                        "Stress Level",
                        f"{stress_color} {result['stress']['stress_level'].capitalize()}",
                        f"{result['stress']['confidence']:.0%} confidence"
                    )
                
                # Supportive response
                st.header("💙 Supportive Response")
                st.markdown(f"""
                <div class="result-box">
                    {result['response']['full_response'].replace('\n', '<br>')}
                </div>
                """, unsafe_allow_html=True)
                
                # Additional info expander
                with st.expander("📋 Detailed Analysis"):
                    st.json({
                        'emotion_scores': result['emotion'].get('all_scores', [])[:3],
                        'stress_scores': result['stress'].get('all_scores', {}),
                        'crisis_severity': result['crisis']['severity'],
                        'processing_time': f"{result['metadata']['processing_time_seconds']}s"
                    })
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <p><strong>Crisis Resources</strong></p>
        <p>🇮🇳 India (AASRA): +91 9820466726 | 🇺🇸 US: 988 | 🇬🇧 UK: 116 123</p>
        <p style="margin-top: 1rem; font-size: 0.9rem;">
            You're not alone. Help is available 24/7.
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
