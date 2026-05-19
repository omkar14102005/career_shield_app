import streamlit as st
import pandas as pd
st.markdown("""
<style>

/* FULL BACKGROUND IMAGE */
.stApp {
    background-image: url("https://images.unsplash.com/photo-1557683316-973673baf926");
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
}

/* LOGIN BOX */
.block-container {
    position: relative;
    z-index: 2;
}

</style>
""", unsafe_allow_html=True)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Fake Job Detector", layout="centered")

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "login"

# ---------------- SIMPLE USER DB (temporary) ----------------
users = {"admin": "1234"}

# ---------------- ML MODEL ----------------
@st.cache_resource
def load_model():
    data = pd.read_csv("jobs.csv")

    X = data["description"]
    y = data["label"]

    vectorizer = TfidfVectorizer()
    X_vector = vectorizer.fit_transform(X)

    model = LogisticRegression()
    model.fit(X_vector, y)

    return vectorizer, model

vectorizer, model = load_model()

# ---------------- CSS ANIMATION ----------------
st.markdown("""
<style>
body {
    background: linear-gradient(120deg,#0f2027,#203a43,#2c5364);
}

.box {
    padding: 25px;
    border-radius: 15px;
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(10px);
    color: white;
    animation: fadeIn 1s ease-in-out;
}

@keyframes fadeIn {
    from {opacity: 0; transform: translateY(20px);}
    to {opacity: 1; transform: translateY(0);}
}

h1 {
    color: #00ffd5;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOGIN ----------------
def login():
    st.markdown("<div class='box'>", unsafe_allow_html=True)

    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.success("Login Successful 🚀")
        else:
            st.error("Invalid Credentials")

    if st.button("Go to Signup"):
        st.session_state.page = "signup"

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- SIGNUP ----------------
def signup():
    st.markdown("<div class='box'>", unsafe_allow_html=True)

    st.title("📝 Signup")

    new_user = st.text_input("Create Username")
    new_pass = st.text_input("Create Password", type="password")

    if st.button("Create Account"):
        users[new_user] = new_pass
        st.success("Account created! Now login")

    if st.button("Go to Login"):
        st.session_state.page = "login"

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- ML APP ----------------
def main_app():
    st.markdown("<div class='box'>", unsafe_allow_html=True)

    st.title("🚀 AI Fake Job Detection")

    job_text = st.text_area("Enter Job Description")

    if st.button("Check"):
        input_data = vectorizer.transform([job_text])
        result = model.predict(input_data)[0]

        if result.lower() == "fake":
            st.error("❌ Prediction: FAKE JOB")
        else:
            st.success("✅ Prediction: REAL JOB")

    if st.button("Logout"):
        st.session_state.logged_in = False

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- ROUTING ----------------
if st.session_state.logged_in:
    main_app()
else:
    if st.session_state.page == "login":
        login()
    else:
        signup()
