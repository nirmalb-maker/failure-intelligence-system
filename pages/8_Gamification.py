import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from gamification_module import calculate_level, get_progress_to_next_level
from ui_utils import inject_premium_css

st.set_page_config(page_title="Gamification", page_icon="🎮", layout="wide")
inject_premium_css()

st.title("🎮 Learning Gamification")
st.markdown("Level up your learning by consistently analyzing failures and taking action!")

st.divider()

score = st.session_state.get('failure_intelligence_score', 145)
streak = st.session_state.get('streak', 5)

level = calculate_level(score)
progress = get_progress_to_next_level(score)

col1, col2, col3 = st.columns(3)
with col1:
    with st.container(border=True):
        st.metric("Failure Intelligence Score", score)
with col2:
    with st.container(border=True):
        st.metric("Current Level", level)
with col3:
    with st.container(border=True):
        st.metric("Achievement Streak", f"{streak} Days", "🔥")

st.divider()

col_prog1, col_prog2 = st.columns([2, 1])

with col_prog1:
    with st.container(border=True):
        st.subheader(f"Progress to Next Level")
        st.progress(progress)
        st.markdown(f"**{(progress * 100):.1f}%** progress toward the next tier.")
        
        if level == "Master":
            st.success("You have reached the highest level! Keep up the great work.")

with col_prog2:
    with st.expander("🏅 Level System Details", expanded=True):
        st.markdown("- **Beginner**: 0 - 49 pts")
        st.markdown("- **Learner**: 50 - 99 pts")
        st.markdown("- **Improver**: 100 - 199 pts")
        st.markdown("- **Master**: 200+ pts")

st.divider()

with st.container(border=True):
    st.subheader("🏆 Achievements")
    col_ach1, col_ach2, col_ach3 = st.columns(3)
    with col_ach1:
        st.success("✔️ First Failure Logged")
    with col_ach2:
        if streak >= 5:
            st.info("🔥 5-Day Streak Reached")
        else:
            st.warning("🔒 5-Day Streak (Locked)")
    with col_ach3:
        if score >= 100:
            st.info("🎓 Improver Status Reached")
        else:
            st.warning("🔒 Improver Status (Locked)")
