import streamlit as st
import pandas as pd
import os
from datetime import datetime

import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from ui_utils import inject_premium_css

st.set_page_config(page_title="Reflection Journal", page_icon="📓", layout="wide")
inject_premium_css()

st.title("📓 Reflection Journal")
st.markdown("Document what you learned from this failure. Self-reflection is highly correlated with reduced future mistakes.")

st.divider()

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv_path = os.path.join(base_dir, "data", "reflections.csv")

col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("Write a Reflection")
    with st.form("reflection_form", border=True):
        failure_desc = st.text_input("Failure Summary (Keywords)", placeholder="e.g. Physics Midterm")
        failure_type = st.selectbox(
            "Failure Type",
            [
                "Exam",
                "Interview",
                "Hackathon",
                "Internship / Job Application",
                "Other"
            ]
        )
        reflection = st.text_area("What did you learn from this failure?", placeholder="I learned that I need to start studying at least a week in advance.", height=150)
        
        submitted = st.form_submit_button("💾 Save Reflection", use_container_width=True)
        
        if submitted:
            if reflection and failure_desc:
                new_data = {
                    "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Failure Description": failure_desc,
                    "Failure Type": failure_type,
                    "Confidence Level": st.session_state.get("last_confidence", 5), 
                    "Cluster": st.session_state.get("last_cluster", 0),
                    "Reflection": reflection
                }
                new_df = pd.DataFrame([new_data])
                if os.path.exists(csv_path):
                    new_df.to_csv(csv_path, mode='a', header=False, index=False)
                else:
                    new_df.to_csv(csv_path, index=False)
                    
                st.success("Reflection saved successfully.")
            else:
                st.error("Please fill in the summary and reflection fields.")

with col2:
    st.subheader("Previous Reflections")
    try:
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            if not df.empty:
                st.dataframe(df, use_container_width=True, height=350)
            else:
                st.info("No reflections found. Start logging to see them here!")
        else:
            st.info("No reflection data file found yet.")
    except Exception as e:
        st.error(f"Error loading reflections: {e}")
