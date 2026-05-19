import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="Fake Job Detection", layout="wide")

# Background CSS
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #dbeafe, #f8fafc);
}
.big-title {
    text-align: center;
    font-size: 42px;
    color: #0f172a;
    font-weight: bold;
}
.footer {
    text-align: center;
    color: gray;
    margin-top: 50px;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Analysis", "About"])

# Load dataset
data = pd.read_csv("jobs.csv")

X = data["description"]
y = data["label"]

vectorizer = TfidfVectorizer()
X_vector = vectorizer.fit_transform(X)

model = LogisticRegression()
model.fit(X_vector, y)

# Home Page
if page == "Home":
    st.markdown('<p class="big-title">AI Fake Job Detection System</p>', unsafe_allow_html=True)
    st.write("This project detects whether a job posting is real or fake using machine learning.")

    job_text = st.text_area("Enter Job Description")

    uploaded_file = st.file_uploader("Or upload text file", type=["txt"])

    if uploaded_file is not None:
        job_text = uploaded_file.read().decode("utf-8")
        st.text_area("Uploaded Content", job_text, height=200)

    if st.button("Check"):
        if job_text.strip() == "":
            st.warning("Please enter job description")
        else:
            input_data = vectorizer.transform([job_text])
            result = model.predict(input_data)[0]

            if result.lower() == "fake":
                st.error("⚠ This Job Posting Seems FAKE")
            else:
                st.success("✅ This Job Posting Seems REAL")

# Analysis Page
elif page == "Analysis":
    st.subheader("Dataset Analysis")

    counts = data["label"].value_counts()

    fig, ax = plt.subplots()
    ax.bar(counts.index, counts.values)
    ax.set_xlabel("Job Type")
    ax.set_ylabel("Count")
    ax.set_title("Real vs Fake Jobs")

    st.pyplot(fig)

# About Page
elif page == "About":
    st.subheader("Project Details")
    st.write("Project Name: Fake Job Detection System")
    st.write("Technology: Python, Streamlit, Machine Learning")
    st.write("Algorithm: Logistic Regression")

# Footer
st.markdown('<div class="footer">Made by BCA Final Year Student</div>', unsafe_allow_html=True)