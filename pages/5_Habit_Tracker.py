import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from ui_utils import inject_premium_css

st.set_page_config(page_title="Habit Tracker", page_icon="📝", layout="wide")
inject_premium_css()

st.title("📝 Habit Tracker")
st.markdown("Build strong learning habits to minimize your future failure risk.")

st.divider()

if 'streak' not in st.session_state:
    st.session_state.streak = 5
if 'weekly_score' not in st.session_state:
    st.session_state.weekly_score = 70
if 'daily_score' not in st.session_state:
    st.session_state.daily_score = 0

col1, col2, col3 = st.columns(3)
with col1:
    with st.container(border=True):
        st.metric("🔥 Current Streak", f"{st.session_state.streak} Days", "+1 Day" if st.session_state.daily_score > 0 else "")
with col2:
    with st.container(border=True):
        st.metric("🌟 Daily Score", f"{st.session_state.daily_score}/15 points", "Logged today" if st.session_state.daily_score > 0 else "")
with col3:
    with st.container(border=True):
        st.metric("📅 Weekly Completion Score", f"{st.session_state.weekly_score}%", "+5%")

st.subheader("📝 Daily Task Checklist")
st.markdown("Mark your daily tasks. Consistent engagement drives your AI risk factor down over time.")

col_a, col_b = st.columns([2, 1])

with col_a:
    with st.container(border=True):
        st.markdown("### 📋 Tasks")
        study_done = st.checkbox("📘 Study Session Completed (2 hours)")
        activity_done = st.checkbox("🎯 Practice Activity Completed")
        review_done = st.checkbox("🔍 Mistake Review Completed")

with col_b:
    with st.container(border=True):
        st.markdown("### ⚡ Action")
        if st.button("Log Daily Tasks", use_container_width=True, type="primary"):
            completed = sum([study_done, activity_done, review_done]) * 5
            st.session_state.daily_score = completed
            st.session_state.weekly_score = min(100, st.session_state.weekly_score + (completed))
            
            st.session_state.habit_score = min(10, st.session_state.get('habit_score', 0) + (completed // 5))
            
            if completed == 15:
                st.session_state.streak += 1
                st.success("Perfect day! Streak increased. 🔥")
                st.balloons()
            elif completed > 0:
                st.success(f"Logged {completed} points.")
            else:
                st.warning("No tasks completed today.")
            
st.divider()

with st.container(border=True):
    st.subheader("🚀 Weekly Progress")
    st.progress(st.session_state.weekly_score / 100.0)
    st.write(f"**{st.session_state.weekly_score}%** of your weekly study goals met.")
