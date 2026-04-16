import streamlit as st

st.set_page_config(
    page_title="Failure Intelligence System",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

from ui_utils import inject_premium_css
inject_premium_css()

# 1. SESSION CONTROL
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "app_started" not in st.session_state:
    st.session_state.app_started = False
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "user_age" not in st.session_state:
    st.session_state.user_age = 0

# Global state initialization
if "failure_intelligence_score" not in st.session_state:
    st.session_state.failure_intelligence_score = 145
if "total_failures_logged" not in st.session_state:
    st.session_state.total_failures_logged = 12
if "last_cluster" not in st.session_state:
    st.session_state.last_cluster = None
if "last_confidence" not in st.session_state:
    st.session_state.last_confidence = 5
if "streak" not in st.session_state:
    st.session_state.streak = 5
if "weekly_score" not in st.session_state:
    st.session_state.weekly_score = 70
if "habit_score" not in st.session_state:
    st.session_state.habit_score = 7  # Scale 1-10
if "failure_risk_score" not in st.session_state:
    st.session_state.failure_risk_score = 45

BG_IMG_URL = "https://www.drjimtaylor.com/4.0/wp-content/uploads/2020/10/success-failure.png"

def set_background_css():
    css = f"""
    <style>
    .stApp {{
        background-image: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), url("{BG_IMG_URL}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    /* Glassmorphism Card */
    .glass-card {{
        background: rgba(30, 30, 40, 0.5);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 40px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        color: white;
    }}
    [data-testid="stSidebar"] {{
        display: none;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


if not st.session_state.logged_in:
    # 2. LOGIN PAGE (FIRST SCREEN)
    set_background_css()

    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    # 3. LOGIN UI (CENTER CARD)
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: white; margin-bottom: 25px;'>Sign In</h2>", unsafe_allow_html=True)
        
        # 4. INPUT FIELDS
        name = st.text_input("Name", key="login_name", placeholder="Enter your name")
        age = st.number_input("Age", min_value=0, max_value=120, key="login_age", step=1)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 5. BUTTON
        if st.button("Enter App", use_container_width=True, type="primary"):
            # 6. VALIDATION
            if not name.strip():
                st.warning("Please enter your name.")
            elif age <= 0:
                st.warning("Please enter a valid age.")
            else:
                # 7. STORE USER DATA
                st.session_state.logged_in = True
                st.session_state.user_name = name
                st.session_state.user_age = age
                st.rerun()
                
        st.markdown('</div>', unsafe_allow_html=True)

elif not st.session_state.app_started:
    # 8. AFTER LOGIN → LANDING PAGE
    set_background_css()
    
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        st.markdown("<br><br><br><br>", unsafe_allow_html=True)
        # 10. PERSONALIZATION
        st.markdown(f"<h3 style='text-align: center; color: #a0a0fb;'>Welcome, {st.session_state.user_name} 👋</h3>", unsafe_allow_html=True)
        
        # 9. LANDING PAGE DESIGN
        st.markdown("<h1 style='text-align: center; font-size: 3.5rem; font-weight: bold; color: white; margin-bottom: 0;'>Failure Intelligence System</h1>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center; color: #d0d0d0; margin-top: 10px; margin-bottom: 40px;'>Transform failures into structured growth using AI & ML</h4>", unsafe_allow_html=True)
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            if st.button("Start Analysis", use_container_width=True, type="primary"):
                # 11. NAVIGATION
                st.session_state.app_started = True
                st.rerun()

else:
    # EXPLORE FULL APP (DASHBOARD)
    
    # 12. LOGOUT BUTTON
    st.sidebar.title("Navigation Hub")
    st.sidebar.info("Select a module to proceed.")
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**User:** {st.session_state.user_name}")
    if st.sidebar.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.app_started = False
        st.session_state.user_name = ""
        st.session_state.user_age = 0
        st.rerun()

    st.title("🧠 Failure Intelligence System")
    st.markdown("### Executive Failure Analytics Dashboard")
    st.write("Convert operational and academic failures into structured, actionable insights using adaptive AI.")

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.info("💡 **Tip:** Start by logging a recent failure in the **Failure Analysis** tab.")
    with col2:
        st.success("📈 **Goal:** Maintain your daily streak in the **Habit Tracker** to reduce your risk score.")
