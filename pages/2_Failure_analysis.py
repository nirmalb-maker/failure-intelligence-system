import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from microplan_module import generate_microplan
from prediction_module import predict_failure_risk, predict_cluster
from ai_module import detect_failure_from_text
from ui_utils import inject_premium_css

st.set_page_config(page_title="Failure Analysis", page_icon="🔍", layout="wide")
inject_premium_css()

st.title("🔍 Failure Analysis")
st.markdown("Analyze a recent failure to understand its root cause and compute your future risk.")
st.divider()

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Detail Your Failure")
    with st.container(border=True):
        failure_description = st.text_area("Failure Description", placeholder="e.g. I ran out of time during the final exam and left 3 questions blank.", height=150)
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
        
        col_inp1, col_inp2 = st.columns(2)
        with col_inp1:
            prep_hours = st.number_input("Preparation Hours", min_value=0.0, value=10.0, step=1.0)
            result_score = st.number_input("Result Score (if applicable)", min_value=0, max_value=100, value=50)
        with col_inp2:
            confidence_level = st.slider("Confidence Level Before Task (1-10)", 1, 10, 5)
            emotional_state = st.slider("Emotional State After Result (1-10)", 1, 10, 5)
            
        structured_prep = st.selectbox("Did you follow a structured plan?", ["Yes, fully structured", "Partially structured", "No structured plan"])

        analyze_btn = st.button("🔍 Analyze Failure", use_container_width=True, type="primary")

with col2:
        # Use AI/NLP to detect cluster first
        ai_cluster, detection_source = detect_failure_from_text(failure_description, failure_type)
        
        if ai_cluster is not None:
            cluster = ai_cluster
            cluster_label = ["Confidence Issue", "Knowledge Gap", "Preparation Problem"][cluster]
        else:
            # Fallback to ML Model
            cluster, cluster_label = predict_cluster(prep_hours, confidence_level, structured_prep, result_score, emotional_state)
            detection_source = "ML prediction used"
        
        st.session_state.last_cluster = cluster
        st.session_state.last_confidence = confidence_level
        st.session_state.last_failure_type = failure_type
        st.session_state.last_description = failure_description
        st.session_state.total_failures_logged = st.session_state.get('total_failures_logged', 12) + 1
        st.session_state.failure_intelligence_score = st.session_state.get('failure_intelligence_score', 145) + 5
        
        habit_score = st.session_state.get('habit_score', 5)
        risk, category = predict_failure_risk(confidence_level, prep_hours, emotional_state, habit_score)
        st.session_state.failure_risk_score = risk
        
        st.success(f"🤖 Analysis Complete! ({detection_source})")
        
        with st.container(border=True):
            st.markdown("### ⚠️ Failure Risk Predictor")
            
            if category == "Low Risk":
                color = "green"
            elif category == "Medium Risk":
                color = "orange"
            else:
                color = "red"
                
            st.metric("Risk Percentage", f"{risk:.1f}%", category, delta_color="inverse" if category=="High Risk" else "normal")
            st.markdown(f"**Risk Label:** :{color}[**{category}**]")
            st.progress(risk / 100.0)

st.divider()

if 'last_cluster' in st.session_state and st.session_state.last_cluster is not None and analyze_btn:
    cluster = st.session_state.last_cluster
    
    explanations = {
        0: "Confidence Issue",
        1: "Knowledge Gap",
        2: "Preparation Problem"
    }
    
    root_causes = {
        0: "Anxiety might be clouding your judgment, preventing you from recalling information or acting effectively.",
        1: "There is a fundamental lack of understanding in the core material necessary for this task.",
        2: "You might be spending too much time on low-priority items or using an inefficient strategy."
    }
    
    st.success(f"### 🧠 Detected Issue: {explanations.get(cluster, 'Unknown')}")
    st.info(f"**Explanation:** {root_causes.get(cluster, '')}")
    
    with st.container(border=True):
        if cluster == 0:
            insight_text = "- 🎭 Imposter syndrome appearing at the wrong time\n- 🥶 Fear of failure causing freezing"
        elif cluster == 1:
            insight_text = "- 📚 Skipped foundational topics\n- ✏️ Insufficient practice of the core material"
        elif cluster == 2:
            insight_text = "- 🕒 Poor scheduling before the deadline\n- 📖 Passive learning or lack of a structured plan"
        else:
            insight_text = "Unknown pattern."
            
        st.warning(f"**💡 Insight (Possible Causes):**\n{insight_text}")
        
    st.markdown("---")
    st.info("Head over to the **Improvement Plan** page to see your tailored actionable steps.")
