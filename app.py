import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

st.set_page_config(page_title="AI Fake Job Detector", layout="wide")

# CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Model
data = pd.read_csv("jobs.csv")

X = data["description"]
y = data["label"]

vectorizer = TfidfVectorizer()
X_vector = vectorizer.fit_transform(X)

model = LogisticRegression()
model.fit(X_vector, y)

# LOGIN PAGE
def login_page():

    left, right = st.columns(2)

    with left:

        st.markdown("""
        <div class="security-box">
            <div class="shield"></div>

            <div class="security-title">
                AI Powered<br>
                Fake Job Detector
            </div>

            <div class="security-sub">
                Smart AI Protection For Safe Careers
            </div>
        </div>
        """, unsafe_allow_html=True)

    with right:

        st.markdown('<div class="form-box">', unsafe_allow_html=True)

        st.title("🔐 Login")

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

        st.markdown("</div>", unsafe_allow_html=True)

# DASHBOARD
def dashboard():

    st.title("🛡 AI Fake Job Detection Dashboard")

    job_text = st.text_area(
        "Enter Job Description"
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
