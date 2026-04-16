import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from data_module import get_failure_statistics
from ui_utils import inject_premium_css

st.set_page_config(page_title="Intelligence Dashboard", page_icon="📊", layout="wide")
inject_premium_css()

st.title("📊 Intelligence Dashboard")
st.markdown("Here is a high-level overview of your failure intelligence journey.")

st.divider()

# Fetch dynamic real data
total_failures, avg_confidence, avg_prep = get_failure_statistics()
st.session_state.total_failures_logged = total_failures

col1, col2, col3, col4 = st.columns(4)
with col1:
    with st.container(border=True):
        st.metric("Failure Intelligence Score", f"{st.session_state.get('failure_intelligence_score', 145)}")
with col2:
    with st.container(border=True):
        risk_score = st.session_state.get('failure_risk_score', 45)
        st.metric("Failure Risk Score", f"{risk_score:.1f}/100", delta_color="inverse")
with col3:
    with st.container(border=True):
        st.metric("Total Failures", f"{total_failures:,}")
with col4:
    with st.container(border=True):
        growth = st.session_state.get('weekly_score', 70)
        st.metric("Weekly Growth", f"{growth}%", "+5%")

st.divider()

col_charts1, col_charts2 = st.columns([1.5, 1])

with col_charts1:
    with st.expander("📈 Weekly Growth Chart", expanded=True):
        st.markdown("#### Failure Intelligence Growth")
        weekly_data = pd.DataFrame({
            'Week': ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
            'Score': [100, 115, 130, st.session_state.get('failure_intelligence_score', 145)]
        })
        fig, ax = plt.subplots(figsize=(6, 3))
        sns.lineplot(data=weekly_data, x='Week', y='Score', marker='o', ax=ax, color='#1f77b4', linewidth=2.5)
        ax.set_ylim(80, 160)
        ax.set_ylabel("Score")
        sns.despine()
        st.pyplot(fig)

with col_charts2:
    with st.container(border=True):
        st.markdown("### ⚠️ Risk Predictor Panel")
        risk_score = st.session_state.get('failure_risk_score', 45)
        
        if risk_score <= 40:
            cat = "Low"
            col = "green"
        elif risk_score <= 70:
            cat = "Medium"
            col = "orange"
        else:
            cat = "High"
            col = "red"
            
        st.metric("Risk Percentage", f"{risk_score:.1f}%", cat, delta_color="inverse" if cat=="High" else "normal")
        st.markdown(f"**Risk Label:** :{col}[**{cat}**]")
        st.progress(risk_score / 100.0)
        
st.divider()

col_act1, col_act2 = st.columns([1, 1])

with col_act1:
    with st.expander("🔄 Recent Activity Summary", expanded=True):
        st.markdown("#### Latest Actions")
        st.markdown("- 📝 **Logged a new failure:** 'Physics Midterm' -> *Time Management*")
        st.markdown("- ✅ **Completed:** 'Pomodoro Technique' practice activity.")
        st.markdown("- 🤖 **Mentorship:** Reviewed 'Confidence Building' mentor advice.")
        st.markdown("- 🔥 **Streak:** Reached a 5-day habit compliance streak!")
        
with col_act2:
     with st.container(border=True):
         st.markdown("### 📅 Weekly Task Completion")
         st.progress(st.session_state.get('weekly_score', 70) / 100.0)
