import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# PAGE
st.set_page_config(
    page_title="AI Fake Job Detector",
    layout="wide"
)

# CSS LOAD
with open("style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# SESSION
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# DATA
data = pd.read_csv("jobs.csv")

X = data["description"]
y = data["label"]

vectorizer = TfidfVectorizer()
X_vector = vectorizer.fit_transform(X)

model = LogisticRegression()
model.fit(X_vector, y)

# LOGIN PAGE
def login_page():

    col1, col2 = st.columns([1.2, 1])

    with col1:

        st.markdown("""
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

    with col2:

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
            "</div>",
            unsafe_allow_html=True
        )

# DASHBOARD
def dashboard():

    st.markdown("""
    <div class="dashboard-title">
        🛡 AI Fake Job Detection Dashboard
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="scan-box">
        <div class="scan-line"></div>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("📄 Analyze Job Description")

    job_text = st.text_area(
        "Paste Job Description Here"
    )

    if st.button("CHECK JOB"):

        input_data = vectorizer.transform([job_text])

        result = model.predict(input_data)[0]

        if result.lower() == "fake":

            st.error("⚠ Fake Job Detected")

        else:

            st.success("✅ Real Job Detected")

# MAIN
if st.session_state.logged_in:

    dashboard()

else:

    login_page()
