import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt

# PAGE
st.set_page_config(
    page_title="AI Fake Job Detector",
    layout="wide"
)

# LOAD CSS
def load_css():

    with open("style.css") as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()

# SESSION
if "logged_in" not in st.session_state:

    st.session_state.logged_in = False

# MODEL
@st.cache_resource
def load_model():

    data = pd.read_csv("jobs.csv")

    X = data["description"]

    y = data["label"]

    vectorizer = TfidfVectorizer()

    X_vec = vectorizer.fit_transform(X)

    model = LogisticRegression()

    model.fit(X_vec, y)

    return vectorizer, model, data

vectorizer, model, data = load_model()

# LOGIN PAGE
def login_page():

    st.markdown("""
    <div class="login-container">
    st.markdown("""
<div class="login-container">

    <div class="security-box">

        <div class="shield"></div>

        <div class="security-title">
            AI Powered<br>
            Fake Job Detector
        </div>

        <div class="security-sub">
            Smart AI Protection For Safe Careers & Trusted Hiring
        </div>

    </div>
""", unsafe_allow_html=True)

        
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="form-box glass">',
        unsafe_allow_html=True
    )

    st.title("🔐 Secure Login")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("LOGIN"):

        if username == "admin" and password == "1234":

            st.session_state.logged_in = True
            st.rerun()

        else:

            st.error("Wrong Credentials")

    st.markdown(
        "</div></div>",
        unsafe_allow_html=True
    )

        

# DASHBOARD
def dashboard():

    st.markdown(
        '<div class="dashboard-bg">',
        unsafe_allow_html=True
    )

    st.sidebar.title("🛡 AI Security")

    page = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "Live Scan",
            "Analytics",
            "Logout"
        ]
    )

    # HOME
    if page == "Dashboard":

        st.title("📊 AI Threat Dashboard")

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.markdown("""
            <div class="metric-card">
            <h2>1,248</h2>
            <p>Total Scans</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:

            st.markdown("""
            <div class="metric-card">
            <h2>842</h2>
            <p>Fake Jobs</p>
            </div>
            """, unsafe_allow_html=True)

        with col3:

            st.markdown("""
            <div class="metric-card">
            <h2>406</h2>
            <p>Safe Jobs</p>
            </div>
            """, unsafe_allow_html=True)

        with col4:

            st.markdown("""
            <div class="metric-card">
            <h2>98%</h2>
            <p>Accuracy</p>
            </div>
            """, unsafe_allow_html=True)

    # LIVE SCAN
    elif page == "Live Scan":

        st.title("🛰 Live Job Scan")

        job_text = st.text_area(
            "Paste Job Description"
        )

        st.markdown("""
        <div class="scan-box">
            <div class="scan-line"></div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Analyze Threat"):

            input_data = vectorizer.transform([job_text])

            result = model.predict(input_data)[0]

            if result.lower() == "fake":

                st.error(
                    "❌ HIGH RISK JOB DETECTED"
                )

            else:

                st.success(
                    "✅ SAFE JOB DETECTED"
                )

            st.subheader("Risk Meter")

            st.markdown("""
            <div class="risk-meter"></div>
            """, unsafe_allow_html=True)

    # ANALYTICS
    elif page == "Analytics":

        st.title("📈 Threat Analytics")

        label_counts = data["label"].value_counts()

        fig, ax = plt.subplots()

        ax.pie(
            label_counts,
            labels=label_counts.index,
            autopct="%1.1f%%"
        )

        st.pyplot(fig)

    # LOGOUT
    elif page == "Logout":

        st.session_state.logged_in = False

        st.rerun()

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

# ROUTING
if st.session_state.logged_in:

    dashboard()

else:

    login_page()
