import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from ai_module import generate_openai_mentor_response
from mentor_module import generate_ai_advice
from ui_utils import inject_premium_css

st.set_page_config(page_title="AI Mentor", page_icon="🤖", layout="wide")
inject_premium_css()

st.title("🤖 AI Mentor Chat")
st.markdown("Your personal AI advisor powered by OpenAI to guide you through your failure recovery.")

st.divider()

if 'last_cluster' not in st.session_state or st.session_state.last_cluster is None:
    st.warning("No recent failure analyzed. Please go to 'Failure Analysis' first.")
    
    with st.chat_message("assistant"):
        st.write("I'm here to help, but I need to know what went wrong. Please analyze a failure first.")
    
    st.divider()
    st.subheader("General Advice")
    default_advice = generate_ai_advice(0, "Other", "", 5)
    with st.container(border=True):
        st.info(f"**Advice:** {default_advice['advice']}")
        st.success(f"**Motivation:** {default_advice['motivation']}")
        st.warning("**Suggested Improvements:**")
        for idx, sugg in enumerate(default_advice.get("learning_suggestions", [])):
            st.write(f"- {sugg}")
    st.stop()

cluster = st.session_state.last_cluster
failure_type = st.session_state.get('last_failure_type', 'Other')
description = st.session_state.get('last_description', '')
confidence = st.session_state.get('last_confidence', 5)

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
    initial_msg = f"Hello! I reviewed your recent failure analysis ({failure_type}). Let's break this down together. How are you feeling about it right now?"
    st.session_state.chat_history.append({"role": "assistant", "content": initial_msg})

# Optional Enhancements: Suggested Questions Buttons
st.markdown("<p style='font-size: 0.9em; color: #94a3b8; margin-bottom: 0px;'>Suggested Topics:</p>", unsafe_allow_html=True)
col1, col2, col3, _ = st.columns([2, 2, 2, 3])
suggested_q = None
with col1:
    if st.button("Why did I fail?", use_container_width=True):
        suggested_q = "Can you help me understand deeply why I failed based on my description?"
with col2:
    if st.button("How to improve fast?", use_container_width=True):
        suggested_q = "What are the most actionable and fastest ways I can improve next time?"
with col3:
    if st.button("Resume/Interview Help", use_container_width=True):
        suggested_q = "Can you provide tips for my resume and upcoming interviews to avoid this failure?"

st.divider()

# Display chat messages from history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Chat Input
user_input = st.chat_input("Ask your AI Mentor a question...")

if suggested_q and not user_input:
    user_input = suggested_q

if user_input:
    # Add user message to state
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
        
    # Memory management: keep last 10 messages
    if len(st.session_state.chat_history) > 10:
        st.session_state.chat_history = st.session_state.chat_history[-10:]

    with st.chat_message("assistant"):
        response, success = generate_openai_mentor_response(
            st.session_state.chat_history,
            cluster,
            failure_type,
            description
        )
        
        if success:
            try:
                full_response = st.write_stream(response)
            except AttributeError:
                # Fallback if st.write_stream is not available in an older Streamlit version
                message_placeholder = st.empty()
                full_response = ""
                for chunk in response:
                    content = chunk.choices[0].delta.content
                    if content:
                        full_response += content
                        message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
        else:
            if response == "API key not configured":
                st.error("API key not configured")
                full_response = "API key not configured"
            else:
                st.warning("OpenAI API streaming failed or is unavailable. Falling back to default assistant.")
                st.error(f"Error detail: {response}")
                fallback_data = generate_ai_advice(cluster, failure_type, description, confidence)
                full_response = f"**Fallback Advice:**\n\n{fallback_data['advice']}\n\n**Next Steps:**\n"
                for s in fallback_data.get('learning_suggestions', []):
                    full_response += f"\n- {s}"
                full_response += f"\n\n**Motivation:**\n{fallback_data['motivation']}"
                st.markdown(full_response)

        # Add assistant message to state
        st.session_state.chat_history.append({"role": "assistant", "content": full_response})

