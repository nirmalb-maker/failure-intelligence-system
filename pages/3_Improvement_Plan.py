import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from microplan_module import generate_microplan
from ui_utils import inject_premium_css

st.set_page_config(page_title="Improvement Plan", page_icon="📈", layout="wide")
inject_premium_css()

st.title("📈 Improvement Plan")
st.markdown("Your custom strategy to bounce back from the failure analyzer.")

st.divider()

if 'last_cluster' in st.session_state and st.session_state.last_cluster is not None:
    cluster = st.session_state.last_cluster
    failure_type = st.session_state.get('last_failure_type')
else:
    cluster = 0 # Default to 0 if not logged
    failure_type = None

plan_data = generate_microplan(cluster, failure_type)

col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.success(f"### 🎯 Target Issue: {plan_data['issue']}")
    st.info(f"**Explanation:** {plan_data['explanation']}")
with col_head2:
    with st.container(border=True):
        st.metric("Difficulty Score", f"{plan_data['difficulty_score']}/5", "-1 since last week", delta_color="inverse")

st.divider()

col_plan1, col_plan2 = st.columns(2)

with col_plan1:
    with st.container(border=True):
        st.markdown("### 📋 Implementation Steps")
        for i, step in enumerate(plan_data['plan']):
            st.markdown(f"**Step {i+1}:** {step}")

with col_plan2:
    with st.container(border=True):
        st.markdown("### ✅ Recommended Activities")
        st.markdown("Check them off as you go to increase your weekly habit score.")
        for i, activity in enumerate(plan_data['activities']):
            st.checkbox(f"{activity}", key=f"activity_{i}_{cluster}")

if st.session_state.last_cluster is None:
    st.warning("⚠️ No recent failure analyzed. Displaying a default plan. Please head to **Failure Analysis** to get a custom plan.")
