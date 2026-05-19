import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# ---------------- PAGE ----------------
st.set_page_config(page_title="Fake Job Detector", layout="centered")

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- BACKGROUND CSS ----------------
st.markdown("""
<style>

/* JOB / CAREER BACKGROUND */
.stApp {
    background-image: url("https://images.unsplash.com/photo-1521737604893-d14cc237f11d");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}

/* DARK OVERLAY */
.stApp::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    height: 100%;
    width: 100%;
    background: rgba(0,0,0,0.6);
    z-index: 0;
}

/* CONTENT ABOVE BACKGROUND */
.block-container {
    position: relative;
    z-index: 2;
}

/* LOGIN BOX */
.login-box {
    background: rgba(255,255,255,0.08);
    padding: 25px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
    width: 350px;
    margin: auto;
    margin-top: 80px;
    color: white;
}

/* BUTTON */
.stButton>button {
    width: 100%;
    background: #00ffd5;
    color: black;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# ---------------- ML MODEL ----------------
@st.cache_resource
def load_model():
    data = pd.read_csv("jobs.csv")

    X = data["description"]
    y = data["label"]

    vectorizer = TfidfVectorizer()
    X_vec = vectorizer.fit_transform(X)

    model = LogisticRegression()
    model.fit(X_vec, y)

    return vectorizer, model

vectorizer, model = load_model()

# ---------------- LOGIN ----------------
def login():
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)

    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Wrong Credentials")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- MAIN APP ----------------
def main_app():
    st.title("🧠 AI Fake Job Detector")

    job_text = st.text_area("Enter Job Description")

    if st.button("Check"):
        input_data = vectorizer.transform([job_text])
        result = model.predict(input_data)[0]

        if result.lower() == "fake":
            st.error("❌ FAKE JOB")
        else:
            st.success("✅ REAL JOB")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

# ---------------- ROUTING ----------------
if st.session_state.logged_in:
    main_app()
else:
    login()
