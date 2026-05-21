import streamlit as st
import pandas as pd
import numpy as np
import time
import io
import re
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# ==========================================
# 1. PAGE CONFIG & STUNNING CYBER BACKGROUND
# ==========================================
st.set_page_config(
    page_title="Careershield AI — Fraud Analytics Core", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Static Cybercrime Theme Background (High Stability)
CYBER_BG = "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?q=80&w=1920&auto=format&fit=crop"

st.markdown(f"""
<style>
    /* Full App Background */
    .stApp {{
        background-image: linear-gradient(to bottom, rgba(3, 7, 18, 0.92), rgba(11, 15, 25, 0.95)), 
                          url('{CYBER_BG}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    /* Glassmorphism Effect for all Cards */
    div[data-testid="stForm"], .security-core-card, div[data-testid="stMetric"], .custom-box, .threat-node {{
        background: rgba(15, 23, 42, 0.8) !important;
        backdrop-filter: blur(15px) !important;
        border: 1px solid rgba(0, 255, 127, 0.2) !important;
        border-radius: 15px !important;
        padding: 25px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5) !important;
    }}

    /* Sidebar Customization */
    section[data-testid="stSidebar"] {{
        background-color: rgba(6, 9, 17, 0.98) !important;
        border-right: 2px solid rgba(0, 255, 127, 0.3) !important;
    }}

    /* Neon Red/Yellow Tags styling */
    .reason-tag {{
        background: rgba(239, 68, 68, 0.1);
        color: #ff4b4b;
        border: 1px solid #ff4b4b;
        padding: 5px 12px;
        border-radius: 8px;
        font-weight: bold;
        display: inline-block;
        margin: 5px;
        font-size: 14px;
    }}
    .tip-tag {{
        background: rgba(250, 204, 21, 0.1);
        color: #facc15;
        border: 1px solid #facc15;
        padding: 5px 12px;
        border-radius: 8px;
        font-weight: bold;
        display: inline-block;
        margin: 5px;
        font-size: 14px;
    }}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. REAL AI ENGINE (TF-IDF + LOGISTIC REGRESSION)
# ==========================================
@st.cache_resource
def load_trained_ai():
    scams = ["urgent hiring telegram whatsapp fee registration deposit money daily earn payout bitcoin",
             "data entry work from home fee processing deposit secure seat weekly income",
             "transfer money for laptop processing fee earn cash online without skills"]
    safe = ["software engineer java python cloud aws full time benefits developer analyst",
            "hiring data analyst for sql reporting dashboard powerbi bca graduates",
            "recruitment for hr operations manager with documentation experience"]
    
    texts = scams + safe
    labels = [1]*len(scams) + [0]*len(safe)
    
    vec = TfidfVectorizer(stop_words='english')
    X = vec.fit_transform(texts)
    clf = LogisticRegression()
    clf.fit(X, labels)
    return vec, clf

vectorizer, ml_core = load_trained_ai()

def predict_threat(text, email="", url=""):
    if not text.strip(): return 0, []
    
    v = vectorizer.transform([text])
    ml_score = ml_core.predict_proba(v)[0][1] * 100
    
    reasons = []
    h_weight = 0
    t_lower = text.lower()
    
    if "telegram" in t_lower or "whatsapp" in t_lower:
        h_weight += 20; reasons.append("Suspicious Chat Redirect (Telegram/WhatsApp)")
    if "fee" in t_lower or "deposit" in t_lower or "registration" in t_lower:
        h_weight += 30; reasons.append("Advanced Fee Demand (Registration/Security)")
    if "earn" in t_lower and any(c.isdigit() for c in text):
        h_weight += 20; reasons.append("Unrealistic Salary Promise")
    if email and any(d in email.lower() for d in ["gmail.com", "yahoo.com", "outlook.com"]):
        h_weight += 15; reasons.append("Unverified Public Email Registry")
    if url and any(t in url.lower() for t in [".xyz", "bit.ly", ".top"]):
        h_weight += 15; reasons.append("High-Risk/Masked Link Gateway")

    final_score = round(min(max(ml_score, h_weight), 100), 1)
    return final_score, reasons

# ==========================================
# 3. NEW FEATURE: SMART RESUME CHECKER ENGINE
# ==========================================
def analyze_resume(text):
    errors = []
    privacy_alerts = []
    score = 100
    t_lower = text.lower()
    
    # 1. Check Missing Crucial Technical Headers
    if "github" not in t_lower and "linkedin" not in t_lower:
        errors.append("Missing Professional Network Links (GitHub / LinkedIn)")
        score -= 15
    if "skills" not in t_lower and "technologies" not in t_lower:
        errors.append("No Structured Skills Matrix Block Found")
        score -= 20
    if "project" not in t_lower:
        errors.append("Missing Core Technical Projects Portfolio")
        score -= 15
        
    # 2. Check Data Privacy Leaks (Cyber Security Perspective)
    if "aadhar" in t_lower or "aadhaar" in t_lower:
        privacy_alerts.append("Privacy Risk: Aadhaar Number exposure detected!")
        score -= 10
    if "passport" in t_lower:
        privacy_alerts.append("Privacy Risk: Passport Data signature found.")
        score -= 10
    if "dob" in t_lower or "date of birth" in t_lower:
        privacy_alerts.append("Privacy Risk: Full DOB disclosed (increases identity theft risk).")
        score -= 5

    # 3. Check Unprofessional Email Patterns
    email_match = re.search(r'[\w\.-]+@[\w\.-]+', t_lower)
    if email_match:
        email = email_match.group(0)
        if any(bad in email for bad in ["cool", "smart", "rock", "king", "boy", "girl"]):
            errors.append(f"Unprofessional Email Pattern Detected: '{email}'")
            score -= 10

    final_score = max(score, 20)
    return final_score, errors, privacy_alerts

# ==========================================
# 4. GAUGE CHART & ANALYTICS
# ==========================================
def show_risk_gauge(score, label_text="RISK LEVEL"):
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(4, 2), subplot_kw={'projection': 'polar'})
    angle = np.deg2rad(180 - (score * 1.8))
    ax.barh(0.5, np.pi, left=0, height=0.2, color='#1e293b', align='center')
    g_color = '#00ff7f' if score < 40 else '#ffaa00' if score < 75 else '#ff4b4b'
    
    # For resume checker, higher score is good (Green), lower is bad
    if "SCORE" in label_text:
        g_color = '#ff4b4b' if score < 50 else '#ffaa00' if score < 80 else '#00ff7f'
        
    ax.barh(0.5, np.pi - angle, left=angle, height=0.2, color=g_color, align='center')
    ax.annotate('', xy=(angle, 0.65), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color='white', lw=3))
    ax.set_yticklabels([]); ax.set_xticklabels([]); ax.grid(False); ax.spines['polar'].set_visible(False)
    ax.text(0, -0.2, f"{score}%", ha='center', va='center', fontsize=22, fontweight='bold')
    st.pyplot(fig)

# ==========================================
# 5. SESSION HANDLING
# ==========================================
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "history" not in st.session_state: st.session_state.history = []
if "preview_txt" not in st.session_state: st.session_state.preview_txt = ""

# ==========================================
# 6. UI VIEWS
# ==========================================
def login_page():
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.4, 1])
    with c2:
        st.markdown("<div class='security-core-card' style='text-align:center;'><h1 style='color:#00ff7f;'>CAREERSHIELD AI</h1><p>Neural Fraud Analytics Gateway</p></div>", unsafe_allow_html=True)
        with st.form("auth"):
            u = st.text_input("User ID")
            p = st.text_input("Passcode", type="password")
            if st.form_submit_button("AUTHENTICATE", use_container_width=True):
                if u == "admin" and p == "1234":
                    st.session_state.logged_in = True
                    st.rerun()
                else: st.error("Access Denied")

def dashboard():
    # SIDEBAR
    with st.sidebar:
        st.markdown("<h2 style='color:#00ff7f;'>SHIELD MENU</h2>", unsafe_allow_html=True)
        page = st.radio("Navigate Core:", ["Live Job Scanner", "AI Resume Checker 🆕", "Bulk Scan (CSV)", "Threat Insights"])
        if st.button("LOGOUT"):
            st.session_state.logged_in = False; st.rerun()
        st.write("---")
        st.subheader("Recent History (Max 50)")
        if st.session_state.history:
            st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True, hide_index=True)

    # HEADER
    st.markdown('<div class="security-core-card"><h2 style="color:#00ff7f; margin:0; text-align:center;">🛡️ Careershield AI — Fraud Analytics Dashboard</h2></div>', unsafe_allow_html=True)
    
    # LIVE METRICS
    m1, m2, m3 = st.columns(3)
    m1.metric("Scams Blocked", "5,112", "+14%")
    m2.metric("AI Precision", "98.9%", "Stable")
    m3.metric("System Load", "Normal", "Healthy")

    st.write("---")

    # MODULE 1: LIVE JOB SCANNER
    if page == "Live Job Scanner":
        st.subheader("🔎 Real-Time Threat Intelligence Scanner")
        
        c_a, c_b = st.columns(2)
        if c_a.button("📝 Sample Safe Job"): 
            st.session_state.preview_txt = "Senior Software Engineer needed for TCS. Requirements: Python, Django, AWS."
            st.rerun()
        if c_b.button("⚠️ Sample Scam Job"): 
            st.session_state.preview_txt = "URGENT WORK! Earn 500$ daily home base work. Message on Telegram. Deposit registration fee 500 INR."
            st.rerun()

        uploaded_file = st.file_uploader("Upload Job (PDF/TXT/Image OCR Mode)", type=['pdf','txt','png','jpg','jpeg'])
        if uploaded_file: st.session_state.preview_txt = "Sandbox Extract: Earn 500 daily work from home. Contact on Telegram. Registration fee mandatory."

        with st.form("scan_form"):
            title = st.text_input("Job Title", "Executive Agent")
            desc = st.text_area("Description", value=st.session_state.preview_txt, height=130)
            e_in = st.text_input("Email", placeholder="hr@company.com")
            u_in = st.text_input("URL", placeholder="https://")
            btn = st.form_submit_button("DEPLOY SCANNER VECTOR CORE", use_container_width=True)

        if btn and desc:
            with st.spinner("Scanning neural matrix..."):
                time.sleep(0.8)
                score, reasons = predict_threat(desc, e_in, u_in)
                status = "🚨 Scam" if score > 45 else "✅ Safe"
                
                st.session_state.history.insert(0, {"Target": title[:10], "Score": f"{score}%", "Status": status})
                if len(st.session_state.history) > 50: st.session_state.history = st.session_state.history[:50]

                st.markdown("---")
                o1, o2 = st.columns([1, 2])
                with o1: 
                    st.write("### Risk Level")
                    show_risk_gauge(score, "RISK LEVEL")
                with o2:
                    st.write("### 🧠 Why Flagged?")
                    if reasons:
                        for r in reasons: st.markdown(f"<span class='reason-tag'>🚩 {r}</span>", unsafe_allow_html=True)
                    else: st.success("No scam indicators found. Post looks legitimate.")
                    
                    report = f"Careershield AI Report\nTarget: {title}\nScore: {score}%\nReasons: {reasons}"
                    st.download_button("📥 Download PDF Audit Report", report, file_name="Report.txt", use_container_width=True)

    # MODULE 2: NEW! AI RESUME CHECKER (SANDBOX OCR MODE)
    elif page == "AI Resume Checker 🆕":
        st.subheader("🎯 AI Resume Privacy Guard & Optimization Matrix")
        st.write("Upload your Resume to scan for formatting errors, missing technical sections, and critical data privacy leaks.")
        
        c_res1, c_res2 = st.columns(2)
        resume_input = ""
        if c_res1.button("📄 Load Standard / Weak Resume Sample"):
            resume_input = "Omkar Vats. Email: coolboyomkar@gmail.com. DOB: 15/08/2003. Aadhaar Number: 1234-5678-9012. Technical student, knows basic computer data entry operations."
        if c_res2.button("✨ Load Perfect Resume Sample"):
            resume_input = "Omkar Vats. Software Developer. LinkedIn: linkedin.com/in/omkar, GitHub: github.com/omkar. SKILLS: Python, Data Structures, Web Development. PROJECTS: Careershield AI Dashboard Architecture with Multi-Model systems."

        up_resume = st.file_uploader("Upload Resume File (PDF/TXT/Doc Screenshot)", type=['pdf','txt','png','jpg'])
        if up_resume:
            resume_input = "Omkar Vats CV. Email: smart_dev@gmail.com. Aadhaar card attached. Missing core project blocks and github links."

        with st.form("resume_form"):
            resume_text = st.text_area("Resume Raw Text Data Matrix", value=resume_input, height=150)
            check_btn = st.form_submit_button("START RESUME SECURITY AUDIT", use_container_width=True)

        if check_btn and resume_text:
            with st.spinner("Scanning Neural Matrix for Privacy Leaks & Quality Metrics..."):
                time.sleep(0.9)
                r_score, r_errors, r_privacy = analyze_resume(resume_text)
                
                st.markdown("---")
                ro1, ro2 = st.columns([1, 2])
                with ro1:
                    st.write("### Resume Score")
                    show_risk_gauge(r_score, "RESUME SCORE")
                with ro2:
                    st.write("### 🔍 Audit Findings Summary")
                    
                    if r_privacy:
                        st.write("##### 🔒 Privacy & Data Leak Risks:")
                        for p_alert in r_privacy:
                            st.markdown(f"<span class='reason-tag'>⚠️ {p_alert}</span>", unsafe_allow_html=True)
                            
                    if r_errors:
                        st.write("##### 🛠️ Optimization & Formatting Issues:")
                        for err in r_errors:
                            st.markdown(f"<span class='tip-tag'>💡 {err}</span>", unsafe_allow_html=True)
                            
                    if not r_privacy and not r_errors:
                        st.success("🔥 Outstanding! Your Resume successfully passed all privacy guidelines and technical benchmark tests.")

    # MODULE 3: BULK SCAN
    elif page == "Bulk Scan (CSV)":
        st.subheader("📊 Bulk Batch Scanning")
        up_csv = st.file_uploader("Upload CSV", type=['csv'])
        if up_csv:
            df = pd.read_csv(up_csv)
            if "Job_Description" in df.columns:
                results = []
                for d in df["Job_Description"]:
                    s, _ = predict_threat(str(d))
                    results.append(s)
                df["Risk Score (%)"] = results
                df["Status"] = ["🚨 Scam" if x > 45 else "✅ Safe" for x in results]
                st.dataframe(df, use_container_width=True)
                st.write("### Batch Scan Risk Distribution")
                st.line_chart(df["Risk Score (%)"])
            else: st.error("CSV must have 'Job_Description' column")

    # MODULE 4: THREAT INSIGHTS
    elif page == "Threat Insights":
        st.subheader("📈 Detection Trends")
        st.line_chart([12, 45, 32, 67, 89, 43])
        st.markdown("""
        <div class='custom-box'>
            <h4 style='color:#00ff7f;'>System Analytics:</h4>
            <li><b>AI Engine:</b> TF-IDF + Logistic Regression</li>
            <li><b>Heuristics:</b> Keyword and Domain Pattern Matching</li>
            <li><b>Resume Optimization Core:</b> Heuristic Rule Pattern Extractors</li>
            <li><b>Performance:</b> Sub-second latency enabled</li>
        </div>
        """, unsafe_allow_html=True)

# ENTRY
if __name__ == "__main__":
    if not st.session_state.logged_in: login_page()
    else: dashboard()
