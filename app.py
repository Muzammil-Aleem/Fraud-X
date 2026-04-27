# import streamlit as st
# import joblib
# import numpy as np
# import pytesseract
# from PIL import Image
# import pytesseract
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# st.markdown("### AI-Powered Transaction & Message Verification System")
# st.markdown("---")

# st.title("FraudX — AI Security System")

# # Load models
# fraud_model = joblib.load("models/fraud_model.pkl")
# fake_model = joblib.load("models/fake_model.pkl")
# vectorizer = joblib.load("models/vectorizer.pkl")
# otp_model = joblib.load("models/otp_model.pkl")
# otp_vectorizer = joblib.load("models/otp_vectorizer.pkl")

# menu = st.sidebar.selectbox(
#     "Choose Feature",
#     ["Fraud Detection", "Fake News Detection", "OTP Screenshot Detection"]
# )

# # ---------------- FRAUD ----------------
# if menu == "Fraud Detection":
#     st.header("Credit Card Fraud Detection")

#     amount = st.number_input("Transaction Amount")

#     if st.button("Predict Fraud"):
#         input_data = np.zeros((1, 30))
#         input_data[0][0] = amount

#         prediction = fraud_model.predict(input_data)[0]

#         probs = fraud_model.predict_proba(input_data)[0]
#         fraud_probability = probs[1] * 100
#         st.subheader("Transaction Risk Score")

#         st.progress(int(fraud_probability))
#         st.write(f"Fraud Probability: {fraud_probability:.2f}%")
#         st.subheader("AI Transaction Analysis")

#         reasons = []

#         if fraud_probability > 70:
#             reasons.append("Transaction pattern strongly deviates from normal behavior.")

#         if amount > 50000:
#             reasons.append("High-value transaction detected.")

#         if fraud_probability > 40:
#             reasons.append("Model detected anomaly in transaction features.")

#         for r in reasons:
#             st.write("✔", r)

#         if fraud_probability > 70:
#             st.error("🚨 HIGH FRAUD RISK")
#         elif fraud_probability > 40:
#             st.warning("⚠ Suspicious Transaction")
#         else:
#             st.success("✅ Transaction Appears Normal")

# # ---------------- FAKE NEWS ----------------
# if menu == "Fake News Detection":
#     st.header("Fake News Detection")

#     news = st.text_area("Enter News Text")

#     if st.button("Analyze"):
#         vec = vectorizer.transform([news])
#         prediction = fake_model.predict(vec)[0]

#         probs = fake_model.predict_proba(vec)[0]
#         fake_index = list(fake_model.classes_).index(0)
#         misinfo_score = probs[fake_index] * 100
#         st.subheader("Misinformation Risk")

#         st.progress(int(misinfo_score))
#         st.write(f"Misinformation Probability: {misinfo_score:.2f}%")
#         st.subheader("Content Analysis")

#         trigger_words = ["shocking", "breaking", "secret", "exposed",
#                         "they don't want you to know", "miracle", "100% proof"]

#         found_triggers = [w for w in trigger_words if w in news.lower()]

#         if found_triggers:
#             st.warning("Manipulative Language Detected:")
#             for t in found_triggers:
#                 st.write("•", t)
#         else:
#             st.write("No sensational language detected.")
#         st.subheader("AI Explanation")

#         explain = []

#         if misinfo_score > 60:
#             explain.append("Article structure resembles known misinformation patterns.")

#         if len(found_triggers) > 0:
#             explain.append("Emotionally manipulative wording detected.")

#         if len(news.split()) < 80:
#             explain.append("Very short articles are often unreliable.")

#         for e in explain:
#             st.write("✔", e)

#         if misinfo_score > 70:
#             st.error("🚨 Likely Fake News")
#         elif misinfo_score > 40:
#             st.warning("⚠ Needs Verification")
#         else:
#             st.success("✅ Appears Credible")

# if menu == "OTP Screenshot Detection":
#     st.header("Upload OTP Screenshot")

#     uploaded_file = st.file_uploader("Upload Image", type=["png","jpg","jpeg"])

#     if uploaded_file is not None:
#         image = Image.open(uploaded_file)

#         st.image(image, caption="Uploaded Screenshot")

#         # OCR Extract Text
#         extracted_text = pytesseract.image_to_string(image)

#         st.subheader("Extracted Text:")
#         st.write(extracted_text)
#         st.subheader("Behavioral Analysis")

#         red_flags = ["urgent", "click", "link", "verify", "share", "blocked",
#                     "suspend", "prize", "call now", "confirm", "account"]

#         found_flags = [word for word in red_flags if word in extracted_text.lower()]
#         if found_flags:
#             st.warning("Suspicious Language Detected:")
#             for flag in found_flags:
#                 st.write(f"• {flag}")
#         else:
#             st.write("No strong phishing indicators detected.")

#         # Predict
#         vec = otp_vectorizer.transform([extracted_text])
#         # Prediction
#         prediction = otp_model.predict(vec)[0]

#         # Get probability score
#         probs = otp_model.predict_proba(vec)[0]
#         fake_index = list(otp_model.classes_).index("fake")
#         risk_score = probs[fake_index] * 100

#         st.subheader("Fraud Risk Score")

#         st.progress(int(risk_score))
#         st.write(f"Risk Level: {risk_score:.2f}%")

#         if risk_score > 70:
#             st.error("🚨 HIGH RISK: Likely Scam")
#         elif risk_score > 40:
#             st.warning("⚠ MEDIUM RISK: Suspicious Message")
#         else:
#             st.success("✅ LOW RISK: Appears Legitimate")
#         st.subheader("AI Explanation")

#         explanations = []

#         if risk_score > 60:
#             explanations.append("Message uses manipulation patterns.")

#         if len(found_flags) > 0:
#             explanations.append("Contains known phishing keywords.")

#         if "otp" in extracted_text.lower():
#             explanations.append("Requests sensitive authentication information.")

#         for exp in explanations:
#             st.write("✔", exp)
#         st.subheader("User Feedback")

#         feedback = st.radio("Was this analysis helpful?", ["Yes", "No"])

#         if feedback == "Yes":
#             st.success("Thank you. Your feedback improves usability.")
#         else:
#             st.info("We will use this to improve detection.")


# import streamlit as st
# import joblib
# import numpy as np
# import pytesseract
# from PIL import Image

# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# # ─── PAGE CONFIG ────────────────────────────────────────────────────────────────
# st.set_page_config(
#     page_title="FraudX — AI Security System",
#     page_icon="🛡️",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # ─── GLOBAL STYLES ──────────────────────────────────────────────────────────────
# st.markdown("""
# <style>
# @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

# /* ── Reset & Base ── */
# *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

# html, body, .stApp {
#     background-color: #080C14 !important;
#     color: #E2E8F2 !important;
#     font-family: 'Syne', sans-serif !important;
# }

# /* ── Hide default Streamlit chrome ── */
# #MainMenu, footer, header { visibility: hidden; }
# .stDeployButton { display: none; }
# .block-container {
#     padding: 2rem 2.5rem !important;
#     max-width: 1100px !important;
# }

# /* ── Sidebar ── */
# [data-testid="stSidebar"] {
#     background: #0B1120 !important;
#     border-right: 1px solid rgba(0,210,255,0.12) !important;
# }
# [data-testid="stSidebar"] * { font-family: 'Syne', sans-serif !important; }

# .sidebar-brand {
#     padding: 2rem 1.5rem 1rem;
#     border-bottom: 1px solid rgba(0,210,255,0.1);
#     margin-bottom: 1.5rem;
# }
# .sidebar-brand h1 {
#     font-size: 1.8rem;
#     font-weight: 800;
#     letter-spacing: -0.5px;
#     background: linear-gradient(135deg, #00D2FF 0%, #7B61FF 100%);
#     -webkit-background-clip: text;
#     -webkit-text-fill-color: transparent;
#     background-clip: text;
# }
# .sidebar-brand p {
#     font-family: 'DM Mono', monospace !important;
#     font-size: 0.65rem;
#     color: #4A5568;
#     letter-spacing: 2px;
#     text-transform: uppercase;
#     margin-top: 0.25rem;
# }
# .sidebar-status {
#     margin: 0 1.5rem 1.5rem;
#     padding: 0.75rem 1rem;
#     background: rgba(0,210,255,0.06);
#     border: 1px solid rgba(0,210,255,0.15);
#     border-radius: 8px;
#     font-family: 'DM Mono', monospace !important;
#     font-size: 0.7rem;
#     color: #00D2FF;
#     letter-spacing: 1px;
# }
# .status-dot {
#     display: inline-block;
#     width: 7px; height: 7px;
#     background: #00FF87;
#     border-radius: 50%;
#     margin-right: 6px;
#     animation: pulse 2s infinite;
# }
# @keyframes pulse {
#     0%,100% { opacity:1; box-shadow:0 0 0 0 rgba(0,255,135,0.4); }
#     50% { opacity:0.7; box-shadow:0 0 0 5px rgba(0,255,135,0); }
# }

# /* ── Selectbox ── */
# [data-testid="stSelectbox"] label {
#     font-family: 'DM Mono', monospace !important;
#     font-size: 0.65rem !important;
#     letter-spacing: 2px !important;
#     text-transform: uppercase !important;
#     color: #4A5568 !important;
#     padding: 0 1.5rem;
# }
# [data-testid="stSelectbox"] > div > div {
#     background: rgba(255,255,255,0.04) !important;
#     border: 1px solid rgba(255,255,255,0.1) !important;
#     border-radius: 8px !important;
#     color: #E2E8F2 !important;
#     font-family: 'Syne', sans-serif !important;
#     margin: 0 1rem;
# }
# [data-testid="stSelectbox"] > div > div:focus-within {
#     border-color: rgba(0,210,255,0.5) !important;
#     box-shadow: 0 0 0 3px rgba(0,210,255,0.1) !important;
# }

# /* ── Page header ── */
# .page-header {
#     margin-bottom: 2.5rem;
#     padding-bottom: 1.5rem;
#     border-bottom: 1px solid rgba(255,255,255,0.07);
# }
# .page-header .badge {
#     display: inline-block;
#     font-family: 'DM Mono', monospace;
#     font-size: 0.62rem;
#     letter-spacing: 3px;
#     text-transform: uppercase;
#     color: #00D2FF;
#     background: rgba(0,210,255,0.1);
#     border: 1px solid rgba(0,210,255,0.25);
#     padding: 4px 12px;
#     border-radius: 100px;
#     margin-bottom: 0.75rem;
# }
# .page-header h2 {
#     font-size: 2.2rem;
#     font-weight: 800;
#     letter-spacing: -1px;
#     line-height: 1.1;
#     color: #F0F4FF;
# }
# .page-header p {
#     font-family: 'DM Mono', monospace;
#     font-size: 0.78rem;
#     color: #4A5568;
#     margin-top: 0.5rem;
#     letter-spacing: 0.5px;
# }

# /* ── Cards ── */
# .glass-card {
#     background: rgba(255,255,255,0.03);
#     border: 1px solid rgba(255,255,255,0.08);
#     border-radius: 16px;
#     padding: 1.75rem;
#     margin-bottom: 1.25rem;
#     transition: border-color 0.3s;
# }
# .glass-card:hover { border-color: rgba(0,210,255,0.2); }

# .card-label {
#     font-family: 'DM Mono', monospace;
#     font-size: 0.62rem;
#     letter-spacing: 2.5px;
#     text-transform: uppercase;
#     color: #4A5568;
#     margin-bottom: 0.75rem;
# }

# /* ── Inputs ── */
# [data-testid="stNumberInput"] label,
# [data-testid="stTextArea"] label,
# [data-testid="stFileUploader"] label {
#     font-family: 'DM Mono', monospace !important;
#     font-size: 0.68rem !important;
#     letter-spacing: 2px !important;
#     text-transform: uppercase !important;
#     color: #4A5568 !important;
# }
# [data-testid="stNumberInput"] input,
# [data-testid="stTextArea"] textarea {
#     background: rgba(255,255,255,0.04) !important;
#     border: 1px solid rgba(255,255,255,0.1) !important;
#     border-radius: 10px !important;
#     color: #E2E8F2 !important;
#     font-family: 'DM Mono', monospace !important;
#     font-size: 0.95rem !important;
# }
# [data-testid="stNumberInput"] input:focus,
# [data-testid="stTextArea"] textarea:focus {
#     border-color: rgba(0,210,255,0.5) !important;
#     box-shadow: 0 0 0 3px rgba(0,210,255,0.08) !important;
# }
# [data-testid="stTextArea"] textarea {
#     min-height: 160px !important;
#     line-height: 1.6 !important;
#     font-size: 0.85rem !important;
# }

# /* ── Button ── */
# .stButton > button {
#     width: 100% !important;
#     background: linear-gradient(135deg, #00D2FF 0%, #7B61FF 100%) !important;
#     color: #080C14 !important;
#     font-family: 'Syne', sans-serif !important;
#     font-weight: 700 !important;
#     font-size: 0.85rem !important;
#     letter-spacing: 1.5px !important;
#     text-transform: uppercase !important;
#     border: none !important;
#     border-radius: 10px !important;
#     padding: 0.75rem 1.5rem !important;
#     cursor: pointer !important;
#     transition: all 0.2s !important;
#     margin-top: 0.5rem !important;
# }
# .stButton > button:hover {
#     transform: translateY(-2px) !important;
#     box-shadow: 0 8px 30px rgba(0,210,255,0.3) !important;
#     filter: brightness(1.05) !important;
# }
# .stButton > button:active { transform: translateY(0) !important; }

# /* ── Progress bar ── */
# [data-testid="stProgress"] > div > div > div > div {
#     background: linear-gradient(90deg, #00D2FF, #7B61FF) !important;
#     border-radius: 100px !important;
# }
# [data-testid="stProgress"] > div > div {
#     background: rgba(255,255,255,0.06) !important;
#     border-radius: 100px !important;
#     height: 10px !important;
# }

# /* ── Risk score display ── */
# .risk-row {
#     display: flex;
#     align-items: center;
#     gap: 1rem;
#     margin-bottom: 0.5rem;
# }
# .risk-label {
#     font-family: 'DM Mono', monospace;
#     font-size: 0.62rem;
#     letter-spacing: 2px;
#     text-transform: uppercase;
#     color: #4A5568;
#     white-space: nowrap;
# }
# .risk-value {
#     font-family: 'DM Mono', monospace;
#     font-size: 2rem;
#     font-weight: 500;
#     letter-spacing: -1px;
# }
# .risk-high  { color: #FF4D6D; }
# .risk-med   { color: #FFB347; }
# .risk-low   { color: #00FF87; }

# /* ── Alert banners ── */
# .alert-box {
#     border-radius: 12px;
#     padding: 1.1rem 1.4rem;
#     font-size: 0.88rem;
#     font-weight: 600;
#     display: flex;
#     align-items: center;
#     gap: 0.75rem;
#     margin-top: 1rem;
#     letter-spacing: 0.3px;
# }
# .alert-danger  { background:rgba(255,77,109,0.12); border:1px solid rgba(255,77,109,0.35); color:#FF4D6D; }
# .alert-warning { background:rgba(255,179,71,0.12); border:1px solid rgba(255,179,71,0.35); color:#FFB347; }
# .alert-success { background:rgba(0,255,135,0.1);   border:1px solid rgba(0,255,135,0.3);   color:#00FF87; }

# /* ── Reason chips ── */
# .reason-chip {
#     display: inline-flex;
#     align-items: center;
#     gap: 6px;
#     background: rgba(255,255,255,0.04);
#     border: 1px solid rgba(255,255,255,0.09);
#     border-radius: 8px;
#     padding: 0.5rem 0.85rem;
#     font-size: 0.8rem;
#     color: #A0AEC0;
#     margin: 0.25rem 0.25rem 0.25rem 0;
#     font-family: 'DM Mono', monospace;
# }
# .reason-chip .dot { color: #00D2FF; font-size: 0.9rem; }

# /* ── Keyword flag chips ── */
# .flag-chip {
#     display: inline-flex;
#     align-items: center;
#     gap: 5px;
#     background: rgba(255,179,71,0.1);
#     border: 1px solid rgba(255,179,71,0.25);
#     border-radius: 6px;
#     padding: 0.3rem 0.7rem;
#     font-size: 0.75rem;
#     color: #FFB347;
#     margin: 0.2rem 0.2rem 0.2rem 0;
#     font-family: 'DM Mono', monospace;
#     letter-spacing: 0.5px;
# }

# /* ── Divider ── */
# .h-divider {
#     border: none;
#     border-top: 1px solid rgba(255,255,255,0.07);
#     margin: 1.5rem 0;
# }

# /* ── Extracted text box ── */
# .extracted-box {
#     background: rgba(255,255,255,0.03);
#     border: 1px solid rgba(255,255,255,0.09);
#     border-radius: 10px;
#     padding: 1rem 1.25rem;
#     font-family: 'DM Mono', monospace;
#     font-size: 0.78rem;
#     color: #7A8FA6;
#     line-height: 1.7;
#     max-height: 180px;
#     overflow-y: auto;
#     white-space: pre-wrap;
#     word-break: break-word;
# }

# /* ── Radio ── */
# [data-testid="stRadio"] label {
#     font-family: 'DM Mono', monospace !important;
#     font-size: 0.72rem !important;
#     letter-spacing: 1.5px !important;
#     text-transform: uppercase !important;
#     color: #4A5568 !important;
# }
# [data-testid="stRadio"] div[role="radiogroup"] label {
#     font-family: 'DM Mono', monospace !important;
#     font-size: 0.82rem !important;
#     text-transform: none !important;
#     letter-spacing: 0.5px !important;
#     color: #A0AEC0 !important;
# }

# /* ── File uploader ── */
# [data-testid="stFileUploader"] section {
#     background: rgba(255,255,255,0.02) !important;
#     border: 2px dashed rgba(0,210,255,0.2) !important;
#     border-radius: 12px !important;
#     transition: border-color 0.3s !important;
# }
# [data-testid="stFileUploader"] section:hover {
#     border-color: rgba(0,210,255,0.45) !important;
#     background: rgba(0,210,255,0.03) !important;
# }

# /* ── Scrollbar ── */
# ::-webkit-scrollbar { width: 6px; }
# ::-webkit-scrollbar-track { background: transparent; }
# ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 3px; }
# ::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.2); }
# </style>
# """, unsafe_allow_html=True)


# # ─── SIDEBAR ────────────────────────────────────────────────────────────────────
# with st.sidebar:
#     st.markdown("""
#     <div class="sidebar-brand">
#         <h1>FraudX</h1>
#         <p>AI Security System</p>
#     </div>
#     <div class="sidebar-status">
#         <span class="status-dot"></span> All models online
#     </div>
#     """, unsafe_allow_html=True)

#     menu = st.selectbox(
#         "MODULE SELECT",
#         ["Fraud Detection", "Fake News Detection", "OTP Screenshot Detection"]
#     )

#     st.markdown("<hr style='border:none;border-top:1px solid rgba(255,255,255,0.07);margin:1.5rem'>", unsafe_allow_html=True)
#     st.markdown("""
#     <div style="padding:0 1.5rem;font-family:'DM Mono',monospace;font-size:0.62rem;
#                 letter-spacing:1.5px;color:#2D3748;line-height:2;">
#         <div style="text-transform:uppercase;margin-bottom:0.5rem;color:#4A5568;">Models Loaded</div>
#         ✓ &nbsp;fraud_model.pkl<br>
#         ✓ &nbsp;fake_model.pkl<br>
#         ✓ &nbsp;otp_model.pkl<br>
#         ✓ &nbsp;vectorizer.pkl
#     </div>
#     """, unsafe_allow_html=True)


# # ─── LOAD MODELS ────────────────────────────────────────────────────────────────
# @st.cache_resource
# def load_models():
#     fraud_model    = joblib.load("models/fraud_model.pkl")
#     fake_model     = joblib.load("models/fake_model.pkl")
#     vectorizer     = joblib.load("models/vectorizer.pkl")
#     otp_model      = joblib.load("models/otp_model.pkl")
#     otp_vectorizer = joblib.load("models/otp_vectorizer.pkl")
#     return fraud_model, fake_model, vectorizer, otp_model, otp_vectorizer

# fraud_model, fake_model, vectorizer, otp_model, otp_vectorizer = load_models()


# # ─── HELPER: risk colour class ──────────────────────────────────────────────────
# def risk_class(pct):
#     if pct > 70:  return "risk-high"
#     if pct > 40:  return "risk-med"
#     return "risk-low"

# def alert_class(pct):
#     if pct > 70:  return "alert-danger"
#     if pct > 40:  return "alert-warning"
#     return "alert-success"

# def alert_icon(pct):
#     if pct > 70:  return "🚨"
#     if pct > 40:  return "⚠️"
#     return "✅"

# def alert_text(pct, mode):
#     if mode == "fraud":
#         if pct > 70:  return "HIGH FRAUD RISK — Do not proceed."
#         if pct > 40:  return "Suspicious transaction — manual review advised."
#         return "Transaction appears normal."
#     if mode == "news":
#         if pct > 70:  return "Likely Fake News — verify before sharing."
#         if pct > 40:  return "Needs verification — cross-check sources."
#         return "Content appears credible."
#     if mode == "otp":
#         if pct > 70:  return "HIGH RISK — Likely a scam message."
#         if pct > 40:  return "MEDIUM RISK — Suspicious message."
#         return "LOW RISK — Appears legitimate."


# # ════════════════════════════════════════════════════════════════════════════════
# # MODULE 1 — FRAUD DETECTION
# # ════════════════════════════════════════════════════════════════════════════════
# if menu == "Fraud Detection":
#     st.markdown("""
#     <div class="page-header">
#         <div class="badge">MODULE 01</div>
#         <h2>Credit Card<br>Fraud Detection</h2>
#         <p>// REAL-TIME TRANSACTION RISK SCORING VIA RANDOM FOREST</p>
#     </div>
#     """, unsafe_allow_html=True)

#     col_input, col_result = st.columns([1, 1], gap="large")

#     with col_input:
#         st.markdown('<div class="glass-card">', unsafe_allow_html=True)
#         st.markdown('<div class="card-label">Transaction Parameters</div>', unsafe_allow_html=True)
#         amount = st.number_input("Transaction Amount (PKR / USD)", min_value=0.0, step=100.0)
#         predict_clicked = st.button("⚡ Run Fraud Analysis")
#         st.markdown('</div>', unsafe_allow_html=True)

#     with col_result:
#         if predict_clicked:
#             input_data = np.zeros((1, 30))
#             input_data[0][0] = amount
#             prediction = fraud_model.predict(input_data)[0]
#             probs = fraud_model.predict_proba(input_data)[0]
#             fraud_prob = probs[1] * 100

#             rc = risk_class(fraud_prob)
#             ac = alert_class(fraud_prob)

#             st.markdown(f"""
#             <div class="glass-card">
#                 <div class="card-label">Risk Score</div>
#                 <div class="risk-value {rc}">{fraud_prob:.1f}<span style="font-size:1rem;color:#4A5568">%</span></div>
#             </div>
#             """, unsafe_allow_html=True)

#             st.progress(int(fraud_prob))

#             st.markdown(f"""
#             <div class="alert-box {ac}">
#                 {alert_icon(fraud_prob)}&nbsp;&nbsp;{alert_text(fraud_prob, 'fraud')}
#             </div>
#             """, unsafe_allow_html=True)

#             reasons = []
#             if fraud_prob > 70:
#                 reasons.append("Pattern deviates from normal behaviour")
#             if amount > 50000:
#                 reasons.append("High-value transaction flagged")
#             if fraud_prob > 40:
#                 reasons.append("Anomaly detected in feature space")

#             if reasons:
#                 st.markdown('<hr class="h-divider">', unsafe_allow_html=True)
#                 st.markdown('<div class="card-label">Analysis Signals</div>', unsafe_allow_html=True)
#                 chips = "".join(
#                     f'<span class="reason-chip"><span class="dot">◈</span>{r}</span>'
#                     for r in reasons
#                 )
#                 st.markdown(chips, unsafe_allow_html=True)
#         else:
#             st.markdown("""
#             <div class="glass-card" style="min-height:200px;display:flex;flex-direction:column;
#                          justify-content:center;align-items:center;gap:0.5rem;opacity:0.4;">
#                 <div style="font-size:2.5rem;">🛡️</div>
#                 <div style="font-family:'DM Mono',monospace;font-size:0.7rem;
#                             letter-spacing:2px;color:#4A5568;text-transform:uppercase;">
#                     Awaiting input
#                 </div>
#             </div>
#             """, unsafe_allow_html=True)


# # ════════════════════════════════════════════════════════════════════════════════
# # MODULE 2 — FAKE NEWS DETECTION
# # ════════════════════════════════════════════════════════════════════════════════
# elif menu == "Fake News Detection":
#     st.markdown("""
#     <div class="page-header">
#         <div class="badge">MODULE 02</div>
#         <h2>Fake News<br>Detection</h2>
#         <p>// TF-IDF + LOGISTIC REGRESSION MISINFORMATION CLASSIFIER</p>
#     </div>
#     """, unsafe_allow_html=True)

#     col_input, col_result = st.columns([1, 1], gap="large")

#     with col_input:
#         st.markdown('<div class="glass-card">', unsafe_allow_html=True)
#         st.markdown('<div class="card-label">Article / News Content</div>', unsafe_allow_html=True)
#         news = st.text_area("Paste news text below", placeholder="Enter full article or headline here…")
#         analyze_clicked = st.button("🔍 Analyze Content")
#         st.markdown('</div>', unsafe_allow_html=True)

#     with col_result:
#         if analyze_clicked and news.strip():
#             vec = vectorizer.transform([news])
#             prediction = fake_model.predict(vec)[0]
#             probs = fake_model.predict_proba(vec)[0]
#             fake_index = list(fake_model.classes_).index(0)
#             misinfo_score = probs[fake_index] * 100

#             trigger_words = ["shocking", "breaking", "secret", "exposed",
#                              "they don't want you to know", "miracle", "100% proof"]
#             found_triggers = [w for w in trigger_words if w in news.lower()]

#             rc = risk_class(misinfo_score)
#             ac = alert_class(misinfo_score)

#             st.markdown(f"""
#             <div class="glass-card">
#                 <div class="card-label">Misinformation Score</div>
#                 <div class="risk-value {rc}">{misinfo_score:.1f}<span style="font-size:1rem;color:#4A5568">%</span></div>
#             </div>
#             """, unsafe_allow_html=True)

#             st.progress(int(misinfo_score))

#             st.markdown(f"""
#             <div class="alert-box {ac}">
#                 {alert_icon(misinfo_score)}&nbsp;&nbsp;{alert_text(misinfo_score, 'news')}
#             </div>
#             """, unsafe_allow_html=True)

#             if found_triggers:
#                 st.markdown('<hr class="h-divider">', unsafe_allow_html=True)
#                 st.markdown('<div class="card-label">Manipulative Language Detected</div>', unsafe_allow_html=True)
#                 chips = "".join(f'<span class="flag-chip">⚠ {t}</span>' for t in found_triggers)
#                 st.markdown(chips, unsafe_allow_html=True)

#             explain = []
#             if misinfo_score > 60:
#                 explain.append("Article structure resembles misinformation patterns")
#             if found_triggers:
#                 explain.append("Emotionally manipulative wording present")
#             if len(news.split()) < 80:
#                 explain.append("Very short articles are often unreliable")

#             if explain:
#                 st.markdown('<hr class="h-divider">', unsafe_allow_html=True)
#                 st.markdown('<div class="card-label">Analysis Signals</div>', unsafe_allow_html=True)
#                 chips = "".join(
#                     f'<span class="reason-chip"><span class="dot">◈</span>{e}</span>'
#                     for e in explain
#                 )
#                 st.markdown(chips, unsafe_allow_html=True)

#         elif analyze_clicked and not news.strip():
#             st.markdown("""
#             <div class="alert-box alert-warning">⚠️&nbsp;&nbsp;Please enter some text to analyze.</div>
#             """, unsafe_allow_html=True)
#         else:
#             st.markdown("""
#             <div class="glass-card" style="min-height:200px;display:flex;flex-direction:column;
#                          justify-content:center;align-items:center;gap:0.5rem;opacity:0.4;">
#                 <div style="font-size:2.5rem;">📰</div>
#                 <div style="font-family:'DM Mono',monospace;font-size:0.7rem;
#                             letter-spacing:2px;color:#4A5568;text-transform:uppercase;">
#                     Awaiting input
#                 </div>
#             </div>
#             """, unsafe_allow_html=True)


# # ════════════════════════════════════════════════════════════════════════════════
# # MODULE 3 — OTP SCREENSHOT DETECTION
# # ════════════════════════════════════════════════════════════════════════════════
# elif menu == "OTP Screenshot Detection":
#     st.markdown("""
#     <div class="page-header">
#         <div class="badge">MODULE 03</div>
#         <h2>OTP Screenshot<br>Phishing Detector</h2>
#         <p>// OCR EXTRACTION + NLP SCAM CLASSIFICATION</p>
#     </div>
#     """, unsafe_allow_html=True)

#     col_upload, col_result = st.columns([1, 1], gap="large")

#     with col_upload:
#         st.markdown('<div class="glass-card">', unsafe_allow_html=True)
#         st.markdown('<div class="card-label">Upload Screenshot</div>', unsafe_allow_html=True)
#         uploaded_file = st.file_uploader("Drag & drop or click to browse", type=["png", "jpg", "jpeg"])

#         if uploaded_file:
#             image = Image.open(uploaded_file)
#             st.image(image, caption="Uploaded Screenshot", use_container_width=True)

#         st.markdown('</div>', unsafe_allow_html=True)

#     with col_result:
#         if uploaded_file:
#             extracted_text = pytesseract.image_to_string(image)

#             st.markdown('<div class="glass-card">', unsafe_allow_html=True)
#             st.markdown('<div class="card-label">OCR — Extracted Text</div>', unsafe_allow_html=True)
#             st.markdown(
#                 f'<div class="extracted-box">{extracted_text if extracted_text.strip() else "No text detected."}</div>',
#                 unsafe_allow_html=True
#             )
#             st.markdown('</div>', unsafe_allow_html=True)

#             red_flags = ["urgent", "click", "link", "verify", "share", "blocked",
#                          "suspend", "prize", "call now", "confirm", "account"]
#             found_flags = [w for w in red_flags if w in extracted_text.lower()]

#             vec = otp_vectorizer.transform([extracted_text])
#             prediction = otp_model.predict(vec)[0]
#             probs = otp_model.predict_proba(vec)[0]
#             fake_index = list(otp_model.classes_).index("fake")
#             risk_score = probs[fake_index] * 100

#             rc = risk_class(risk_score)
#             ac = alert_class(risk_score)

#             st.markdown(f"""
#             <div class="glass-card">
#                 <div class="card-label">Fraud Risk Score</div>
#                 <div class="risk-value {rc}">{risk_score:.1f}<span style="font-size:1rem;color:#4A5568">%</span></div>
#             </div>
#             """, unsafe_allow_html=True)

#             st.progress(int(risk_score))

#             st.markdown(f"""
#             <div class="alert-box {ac}">
#                 {alert_icon(risk_score)}&nbsp;&nbsp;{alert_text(risk_score, 'otp')}
#             </div>
#             """, unsafe_allow_html=True)

#             if found_flags:
#                 st.markdown('<hr class="h-divider">', unsafe_allow_html=True)
#                 st.markdown('<div class="card-label">Phishing Keywords Detected</div>', unsafe_allow_html=True)
#                 chips = "".join(f'<span class="flag-chip">⚠ {f}</span>' for f in found_flags)
#                 st.markdown(chips, unsafe_allow_html=True)

#             explanations = []
#             if risk_score > 60:
#                 explanations.append("Message uses known manipulation patterns")
#             if found_flags:
#                 explanations.append("Contains phishing keywords")
#             if "otp" in extracted_text.lower():
#                 explanations.append("Requests sensitive authentication code")

#             if explanations:
#                 st.markdown('<hr class="h-divider">', unsafe_allow_html=True)
#                 st.markdown('<div class="card-label">Analysis Signals</div>', unsafe_allow_html=True)
#                 chips = "".join(
#                     f'<span class="reason-chip"><span class="dot">◈</span>{e}</span>'
#                     for e in explanations
#                 )
#                 st.markdown(chips, unsafe_allow_html=True)

#             st.markdown('<hr class="h-divider">', unsafe_allow_html=True)
#             st.markdown('<div class="card-label">Was this analysis helpful?</div>', unsafe_allow_html=True)
#             feedback = st.radio("", ["👍  Yes, accurate", "👎  No, incorrect"], label_visibility="collapsed")
#             if feedback == "👍  Yes, accurate":
#                 st.markdown('<div class="alert-box alert-success">✅&nbsp;&nbsp;Thank you. Your feedback improves the model.</div>', unsafe_allow_html=True)
#             else:
#                 st.markdown('<div class="alert-box" style="background:rgba(123,97,255,0.1);border:1px solid rgba(123,97,255,0.3);color:#7B61FF;">💜&nbsp;&nbsp;Noted — we\'ll use this to improve detection accuracy.</div>', unsafe_allow_html=True)

#         else:
#             st.markdown("""
#             <div class="glass-card" style="min-height:300px;display:flex;flex-direction:column;
#                          justify-content:center;align-items:center;gap:0.75rem;opacity:0.4;">
#                 <div style="font-size:3rem;">📲</div>
#                 <div style="font-family:'DM Mono',monospace;font-size:0.7rem;
#                             letter-spacing:2px;color:#4A5568;text-transform:uppercase;">
#                     Upload a screenshot to begin
#                 </div>
#             </div>
#             """, unsafe_allow_html=True)




# import streamlit as st
# import joblib
# import numpy as np
# import pytesseract
# from PIL import Image

# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# # ─── PAGE CONFIG ────────────────────────────────────────────────────────────────
# st.set_page_config(
#     page_title="FraudX — AI Security",
#     page_icon="🛡",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # ─── STYLES ─────────────────────────────────────────────────────────────────────
# st.markdown("""
# <style>
# @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

# /* ══ Base ══ */
# html, body, .stApp {
#     background: #F7F8FC !important;
#     font-family: 'IBM Plex Sans', sans-serif !important;
#     color: #1A1D27 !important;
# }
# #MainMenu, footer, header, .stDeployButton { visibility: hidden; display: none; }
# .block-container {
#     padding: 2.5rem 2.8rem 3rem !important;
#     max-width: 1160px !important;
# }

# /* ══ Sidebar ══ */
# [data-testid="stSidebar"] {
#     background: #12151F !important;
#     border-right: none !important;
# }
# [data-testid="stSidebar"] > div { padding-top: 0 !important; }
# section[data-testid="stSidebar"] * { font-family: 'IBM Plex Sans', sans-serif !important; }

# .brand-block {
#     padding: 2rem 1.75rem 1.5rem;
#     border-bottom: 1px solid rgba(255,255,255,0.07);
#     margin-bottom: 1.25rem;
# }
# .brand-shield { font-size: 2rem; margin-bottom: 0.5rem; display: block; }
# .brand-name {
#     font-family: 'Playfair Display', serif;
#     font-size: 1.75rem;
#     font-weight: 700;
#     color: #FFFFFF;
#     letter-spacing: -0.5px;
#     line-height: 1;
# }
# .brand-tag {
#     font-family: 'IBM Plex Mono', monospace;
#     font-size: 0.58rem;
#     color: #4A5568;
#     letter-spacing: 3px;
#     text-transform: uppercase;
#     margin-top: 4px;
# }
# .online-pill {
#     display: inline-flex;
#     align-items: center;
#     gap: 6px;
#     background: rgba(16,185,129,0.15);
#     border: 1px solid rgba(16,185,129,0.3);
#     border-radius: 100px;
#     padding: 4px 12px;
#     font-family: 'IBM Plex Mono', monospace;
#     font-size: 0.6rem;
#     color: #10B981;
#     letter-spacing: 1.5px;
#     margin: 0 1.75rem 1.25rem;
# }
# .pulse-dot {
#     width: 6px; height: 6px;
#     background: #10B981;
#     border-radius: 50%;
#     animation: blink 2s ease-in-out infinite;
# }
# @keyframes blink {
#     0%,100% { opacity:1; }
#     50% { opacity:0.3; }
# }

# /* ══ Sidebar selectbox ══ */
# [data-testid="stSidebar"] [data-testid="stSelectbox"] label {
#     font-family: 'IBM Plex Mono', monospace !important;
#     font-size: 0.58rem !important;
#     color: #4A5568 !important;
#     letter-spacing: 2.5px !important;
#     text-transform: uppercase !important;
#     padding: 0 1.75rem !important;
# }
# [data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div {
#     background: rgba(255,255,255,0.06) !important;
#     border: 1px solid rgba(255,255,255,0.12) !important;
#     border-radius: 10px !important;
#     color: #E2E8F0 !important;
#     font-family: 'IBM Plex Sans', sans-serif !important;
#     margin: 0 1.25rem !important;
#     font-size: 0.88rem !important;
# }

# .model-list {
#     margin: 1.25rem 1.75rem 0;
#     padding-top: 1.25rem;
#     border-top: 1px solid rgba(255,255,255,0.07);
# }
# .model-list-title {
#     font-family: 'IBM Plex Mono', monospace;
#     font-size: 0.57rem;
#     color: #4A5568;
#     letter-spacing: 2.5px;
#     text-transform: uppercase;
#     margin-bottom: 0.75rem;
# }
# .model-item {
#     display: flex;
#     align-items: center;
#     gap: 8px;
#     padding: 5px 0;
#     font-family: 'IBM Plex Mono', monospace;
#     font-size: 0.65rem;
#     color: #718096;
#     letter-spacing: 0.5px;
# }
# .model-check { color: #10B981; font-size: 0.7rem; }

# /* ══ Page Header ══ */
# .page-head { margin-bottom: 2.25rem; }
# .module-tag {
#     font-family: 'IBM Plex Mono', monospace;
#     font-size: 0.6rem;
#     letter-spacing: 3px;
#     text-transform: uppercase;
#     color: #6366F1;
#     background: rgba(99,102,241,0.08);
#     border: 1px solid rgba(99,102,241,0.2);
#     padding: 4px 12px;
#     border-radius: 100px;
#     display: inline-block;
#     margin-bottom: 0.75rem;
# }
# .page-head h1 {
#     font-family: 'Playfair Display', serif !important;
#     font-size: 2.4rem !important;
#     font-weight: 700 !important;
#     color: #0F1117 !important;
#     letter-spacing: -1px !important;
#     line-height: 1.15 !important;
#     margin: 0 !important;
# }
# .page-head p {
#     font-family: 'IBM Plex Mono', monospace !important;
#     font-size: 0.7rem !important;
#     color: #94A3B8 !important;
#     margin-top: 6px !important;
#     letter-spacing: 0.5px !important;
# }

# /* ══ Cards ══ */
# .card {
#     background: #FFFFFF;
#     border: 1px solid #E8ECF4;
#     border-radius: 16px;
#     padding: 1.75rem;
#     box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 4px 16px rgba(0,0,0,0.03);
#     margin-bottom: 1rem;
# }
# .card-label {
#     font-family: 'IBM Plex Mono', monospace;
#     font-size: 0.58rem;
#     letter-spacing: 2.5px;
#     text-transform: uppercase;
#     color: #94A3B8;
#     margin-bottom: 1rem;
# }
# .card-divider {
#     border: none;
#     border-top: 1px solid #EEF1F8;
#     margin: 1.25rem 0;
# }

# /* ══ Inputs ══ */
# [data-testid="stNumberInput"] label,
# [data-testid="stTextArea"] label,
# [data-testid="stFileUploader"] label {
#     font-family: 'IBM Plex Mono', monospace !important;
#     font-size: 0.62rem !important;
#     letter-spacing: 2px !important;
#     text-transform: uppercase !important;
#     color: #64748B !important;
#     margin-bottom: 6px !important;
# }
# [data-testid="stNumberInput"] input {
#     background: #F8FAFF !important;
#     border: 1.5px solid #E2E8F0 !important;
#     border-radius: 10px !important;
#     color: #1A1D27 !important;
#     font-family: 'IBM Plex Mono', monospace !important;
#     font-size: 1rem !important;
# }
# [data-testid="stNumberInput"] input:focus {
#     border-color: #6366F1 !important;
#     box-shadow: 0 0 0 3px rgba(99,102,241,0.1) !important;
#     background: #FFFFFF !important;
# }
# [data-testid="stTextArea"] textarea {
#     background: #F8FAFF !important;
#     border: 1.5px solid #E2E8F0 !important;
#     border-radius: 10px !important;
#     color: #1A1D27 !important;
#     font-family: 'IBM Plex Sans', sans-serif !important;
#     font-size: 0.9rem !important;
#     line-height: 1.6 !important;
#     min-height: 160px !important;
# }
# [data-testid="stTextArea"] textarea:focus {
#     border-color: #6366F1 !important;
#     box-shadow: 0 0 0 3px rgba(99,102,241,0.1) !important;
#     background: #FFFFFF !important;
# }
# [data-testid="stTextArea"] textarea::placeholder { color: #CBD5E1 !important; }

# /* ══ Button ══ */
# .stButton > button {
#     width: 100% !important;
#     background: #0F1117 !important;
#     color: #FFFFFF !important;
#     font-family: 'IBM Plex Sans', sans-serif !important;
#     font-weight: 600 !important;
#     font-size: 0.82rem !important;
#     letter-spacing: 0.8px !important;
#     border: none !important;
#     border-radius: 10px !important;
#     padding: 0.72rem 1.5rem !important;
#     cursor: pointer !important;
#     transition: all 0.2s ease !important;
#     margin-top: 0.5rem !important;
# }
# .stButton > button:hover {
#     background: #1E2236 !important;
#     transform: translateY(-1px) !important;
#     box-shadow: 0 8px 24px rgba(15,17,23,0.18) !important;
# }

# /* ══ Progress bar ══ */
# [data-testid="stProgress"] > div > div {
#     background: #EEF1F8 !important;
#     border-radius: 100px !important;
#     height: 8px !important;
# }
# [data-testid="stProgress"] > div > div > div > div {
#     border-radius: 100px !important;
#     height: 8px !important;
# }

# /* ══ Risk score ══ */
# .risk-score-block {
#     display: flex;
#     align-items: baseline;
#     gap: 6px;
#     margin-bottom: 10px;
# }
# .risk-score-num {
#     font-family: 'Playfair Display', serif;
#     font-size: 3.2rem;
#     font-weight: 700;
#     line-height: 1;
#     letter-spacing: -2px;
# }
# .risk-score-pct {
#     font-family: 'IBM Plex Mono', monospace;
#     font-size: 0.85rem;
#     color: #94A3B8;
# }
# .score-high { color: #DC2626; }
# .score-med  { color: #D97706; }
# .score-low  { color: #059669; }

# /* ══ Verdict ══ */
# .verdict {
#     display: flex;
#     align-items: flex-start;
#     gap: 10px;
#     padding: 0.85rem 1.1rem;
#     border-radius: 10px;
#     font-family: 'IBM Plex Sans', sans-serif;
#     font-size: 0.84rem;
#     font-weight: 500;
#     margin-top: 1rem;
#     line-height: 1.4;
#     color: #1A1D27;
# }
# .verdict-icon { font-size: 1rem; margin-top: 1px; flex-shrink: 0; }
# .verdict-danger  { background:#FEF2F2; border:1px solid #FECACA; }
# .verdict-danger .verdict-text  { color: #991B1B; }
# .verdict-warning { background:#FFFBEB; border:1px solid #FDE68A; }
# .verdict-warning .verdict-text { color: #92400E; }
# .verdict-success { background:#ECFDF5; border:1px solid #A7F3D0; }
# .verdict-success .verdict-text { color: #065F46; }

# /* ══ Signal chips ══ */
# .signals-wrap { display:flex; flex-wrap:wrap; gap:6px; margin-top:0.25rem; }
# .signal-chip {
#     display: inline-flex;
#     align-items: center;
#     gap: 6px;
#     background: #F8FAFF;
#     border: 1px solid #E2E8F0;
#     border-radius: 8px;
#     padding: 5px 10px;
#     font-family: 'IBM Plex Sans', sans-serif;
#     font-size: 0.75rem;
#     color: #475569;
# }
# .signal-dot { width:6px; height:6px; border-radius:50%; background:#6366F1; flex-shrink:0; }

# /* ══ Flag chips ══ */
# .flag-chip {
#     display: inline-flex;
#     align-items: center;
#     gap: 5px;
#     background: #FFFBEB;
#     border: 1px solid #FDE68A;
#     border-radius: 6px;
#     padding: 4px 9px;
#     font-family: 'IBM Plex Mono', monospace;
#     font-size: 0.68rem;
#     color: #92400E;
#     font-weight: 500;
#     margin: 2px 2px 2px 0;
# }

# /* ══ OCR text box ══ */
# .ocr-box {
#     background: #F8FAFF;
#     border: 1px solid #E2E8F0;
#     border-radius: 10px;
#     padding: 1rem 1.1rem;
#     font-family: 'IBM Plex Mono', monospace;
#     font-size: 0.75rem;
#     color: #475569;
#     line-height: 1.8;
#     max-height: 160px;
#     overflow-y: auto;
#     white-space: pre-wrap;
#     word-break: break-word;
# }

# /* ══ Placeholder ══ */
# .placeholder-card {
#     background: #FFFFFF;
#     border: 1.5px dashed #E2E8F0;
#     border-radius: 16px;
#     padding: 3rem 2rem;
#     display: flex;
#     flex-direction: column;
#     align-items: center;
#     justify-content: center;
#     gap: 10px;
#     min-height: 220px;
# }
# .placeholder-icon { font-size: 2.5rem; opacity: 0.2; }
# .placeholder-text {
#     font-family: 'IBM Plex Mono', monospace;
#     font-size: 0.62rem;
#     letter-spacing: 2px;
#     text-transform: uppercase;
#     color: #CBD5E1;
# }

# /* ══ File uploader ══ */
# [data-testid="stFileUploader"] section {
#     background: #F8FAFF !important;
#     border: 2px dashed #C7D2E8 !important;
#     border-radius: 12px !important;
# }
# [data-testid="stFileUploader"] section:hover {
#     border-color: #6366F1 !important;
#     background: rgba(99,102,241,0.02) !important;
# }
# [data-testid="stFileUploader"] section p,
# [data-testid="stFileUploader"] section span,
# [data-testid="stFileUploader"] section small {
#     color: #64748B !important;
#     font-family: 'IBM Plex Sans', sans-serif !important;
# }

# /* ══ Radio ══ */
# [data-testid="stRadio"] > label {
#     font-family: 'IBM Plex Mono', monospace !important;
#     font-size: 0.62rem !important;
#     letter-spacing: 2px !important;
#     text-transform: uppercase !important;
#     color: #94A3B8 !important;
# }
# [data-testid="stRadio"] div[role="radiogroup"] > label {
#     font-family: 'IBM Plex Sans', sans-serif !important;
#     font-size: 0.84rem !important;
#     text-transform: none !important;
#     letter-spacing: 0 !important;
#     color: #475569 !important;
# }

# /* ══ Scrollbar ══ */
# ::-webkit-scrollbar { width: 4px; }
# ::-webkit-scrollbar-track { background: transparent; }
# ::-webkit-scrollbar-thumb { background: #E2E8F0; border-radius: 2px; }
# </style>
# """, unsafe_allow_html=True)


# # ─── SIDEBAR ────────────────────────────────────────────────────────────────────
# with st.sidebar:
#     st.markdown("""
#     <div class="brand-block">
#         <span class="brand-shield">🛡</span>
#         <div class="brand-name">FraudX</div>
#         <div class="brand-tag">AI Security System</div>
#     </div>
#     <div class="online-pill">
#         <span class="pulse-dot"></span> Systems Online
#     </div>
#     """, unsafe_allow_html=True)

#     menu = st.selectbox(
#         "ACTIVE MODULE",
#         ["Fraud Detection", "Fake News Detection", "OTP Screenshot Detection"]
#     )

#     st.markdown("""
#     <div class="model-list">
#         <div class="model-list-title">Loaded Models</div>
#         <div class="model-item"><span class="model-check">✓</span> fraud_model.pkl</div>
#         <div class="model-item"><span class="model-check">✓</span> fake_model.pkl</div>
#         <div class="model-item"><span class="model-check">✓</span> otp_model.pkl</div>
#         <div class="model-item"><span class="model-check">✓</span> vectorizer.pkl</div>
#         <div class="model-item"><span class="model-check">✓</span> otp_vectorizer.pkl</div>
#     </div>
#     """, unsafe_allow_html=True)


# # ─── LOAD MODELS ────────────────────────────────────────────────────────────────
# @st.cache_resource
# def load_models():
#     fraud_model    = joblib.load("models/fraud_model.pkl")
#     fake_model     = joblib.load("models/fake_model.pkl")
#     vectorizer     = joblib.load("models/vectorizer.pkl")
#     otp_model      = joblib.load("models/otp_model.pkl")
#     otp_vectorizer = joblib.load("models/otp_vectorizer.pkl")
#     return fraud_model, fake_model, vectorizer, otp_model, otp_vectorizer

# fraud_model, fake_model, vectorizer, otp_model, otp_vectorizer = load_models()


# # ─── HELPERS ────────────────────────────────────────────────────────────────────
# def score_class(p):
#     if p > 70: return "score-high"
#     if p > 40: return "score-med"
#     return "score-low"

# def progress_color(p):
#     if p > 70: return "#DC2626"
#     if p > 40: return "#D97706"
#     return "#059669"

# def inject_progress(value, color):
#     st.markdown(f"""
#     <style>
#     [data-testid="stProgress"] > div > div > div > div {{
#         background: {color} !important;
#     }}
#     </style>
#     """, unsafe_allow_html=True)
#     st.progress(int(value))

# def verdict_html(p, mode):
#     tiers = {
#         "fraud": {
#             "high": ("verdict-danger",  "🚨", "High Fraud Risk — Do not proceed with this transaction."),
#             "med":  ("verdict-warning", "⚠️", "Suspicious Transaction — Manual review is recommended."),
#             "low":  ("verdict-success", "✅", "Transaction Appears Normal — No significant risk detected."),
#         },
#         "news": {
#             "high": ("verdict-danger",  "🚨", "Likely Fake News — Do not share without fact-checking."),
#             "med":  ("verdict-warning", "⚠️", "Needs Verification — Cross-check with trusted sources."),
#             "low":  ("verdict-success", "✅", "Content Appears Credible — No strong misinformation signals."),
#         },
#         "otp": {
#             "high": ("verdict-danger",  "🚨", "High Risk — This message is very likely a scam."),
#             "med":  ("verdict-warning", "⚠️", "Medium Risk — Treat this message with caution."),
#             "low":  ("verdict-success", "✅", "Low Risk — Message appears legitimate."),
#         },
#     }
#     tier = "high" if p > 70 else ("med" if p > 40 else "low")
#     cls, icon, text = tiers[mode][tier]
#     return f'<div class="verdict {cls}"><span class="verdict-icon">{icon}</span><span class="verdict-text">{text}</span></div>'


# # ════════════════════════════════════════════════════════════════════════════════
# # MODULE 1 — FRAUD DETECTION
# # ════════════════════════════════════════════════════════════════════════════════
# if menu == "Fraud Detection":
#     st.markdown("""
#     <div class="page-head">
#         <span class="module-tag">Module 01</span>
#         <h1>Credit Card<br>Fraud Detection</h1>
#         <p>// Real-time transaction risk scoring · Random Forest Classifier</p>
#     </div>
#     """, unsafe_allow_html=True)

#     col_l, col_r = st.columns([1, 1], gap="large")

#     with col_l:
#         st.markdown('<div class="card">', unsafe_allow_html=True)
#         st.markdown('<div class="card-label">Transaction Parameters</div>', unsafe_allow_html=True)
#         amount = st.number_input("Transaction Amount", min_value=0.0, step=500.0, format="%.2f")
#         clicked = st.button("Run Fraud Analysis →")
#         st.markdown('</div>', unsafe_allow_html=True)

#     with col_r:
#         if clicked:
#             input_data = np.zeros((1, 30))
#             input_data[0][0] = amount
#             probs = fraud_model.predict_proba(input_data)[0]
#             fraud_prob = probs[1] * 100

#             sc = score_class(fraud_prob)
#             pc = progress_color(fraud_prob)

#             st.markdown('<div class="card">', unsafe_allow_html=True)
#             st.markdown('<div class="card-label">Risk Score</div>', unsafe_allow_html=True)
#             st.markdown(f"""
#             <div class="risk-score-block">
#                 <span class="risk-score-num {sc}">{fraud_prob:.1f}</span>
#                 <span class="risk-score-pct">% fraud probability</span>
#             </div>
#             """, unsafe_allow_html=True)
#             inject_progress(fraud_prob, pc)
#             st.markdown(verdict_html(fraud_prob, "fraud"), unsafe_allow_html=True)

#             reasons = []
#             if fraud_prob > 70:
#                 reasons.append("Pattern strongly deviates from normal behaviour")
#             if amount > 50000:
#                 reasons.append("High-value transaction detected")
#             if fraud_prob > 40:
#                 reasons.append("Model detected anomaly in feature space")

#             if reasons:
#                 st.markdown('<hr class="card-divider"><div class="card-label">Analysis Signals</div>', unsafe_allow_html=True)
#                 chips = "".join(
#                     f'<span class="signal-chip"><span class="signal-dot"></span>{r}</span>'
#                     for r in reasons
#                 )
#                 st.markdown(f'<div class="signals-wrap">{chips}</div>', unsafe_allow_html=True)

#             st.markdown('</div>', unsafe_allow_html=True)
#         else:
#             st.markdown("""
#             <div class="placeholder-card">
#                 <div class="placeholder-icon">📊</div>
#                 <div class="placeholder-text">Awaiting transaction input</div>
#             </div>
#             """, unsafe_allow_html=True)


# # ════════════════════════════════════════════════════════════════════════════════
# # MODULE 2 — FAKE NEWS DETECTION
# # ════════════════════════════════════════════════════════════════════════════════
# elif menu == "Fake News Detection":
#     st.markdown("""
#     <div class="page-head">
#         <span class="module-tag">Module 02</span>
#         <h1>Fake News<br>Detection</h1>
#         <p>// TF-IDF vectorisation · Logistic Regression misinformation classifier</p>
#     </div>
#     """, unsafe_allow_html=True)

#     col_l, col_r = st.columns([1, 1], gap="large")

#     with col_l:
#         st.markdown('<div class="card">', unsafe_allow_html=True)
#         st.markdown('<div class="card-label">Article Content</div>', unsafe_allow_html=True)
#         news = st.text_area("Paste news article or headline", placeholder="Enter the full article or headline to analyze…")
#         clicked = st.button("Analyze Content →")
#         st.markdown('</div>', unsafe_allow_html=True)

#     with col_r:
#         if clicked and news.strip():
#             vec = vectorizer.transform([news])
#             probs = fake_model.predict_proba(vec)[0]
#             fake_index = list(fake_model.classes_).index(0)
#             misinfo = probs[fake_index] * 100

#             trigger_words = ["shocking", "breaking", "secret", "exposed",
#                              "they don't want you to know", "miracle", "100% proof"]
#             found = [w for w in trigger_words if w in news.lower()]

#             sc = score_class(misinfo)
#             pc = progress_color(misinfo)

#             st.markdown('<div class="card">', unsafe_allow_html=True)
#             st.markdown('<div class="card-label">Misinformation Score</div>', unsafe_allow_html=True)
#             st.markdown(f"""
#             <div class="risk-score-block">
#                 <span class="risk-score-num {sc}">{misinfo:.1f}</span>
#                 <span class="risk-score-pct">% misinformation probability</span>
#             </div>
#             """, unsafe_allow_html=True)
#             inject_progress(misinfo, pc)
#             st.markdown(verdict_html(misinfo, "news"), unsafe_allow_html=True)

#             if found:
#                 st.markdown('<hr class="card-divider"><div class="card-label">Manipulative Language Detected</div>', unsafe_allow_html=True)
#                 chips = "".join(f'<span class="flag-chip">⚠ {t}</span>' for t in found)
#                 st.markdown(f'<div style="margin-top:4px">{chips}</div>', unsafe_allow_html=True)

#             explain = []
#             if misinfo > 60:
#                 explain.append("Article structure resembles known misinformation patterns")
#             if found:
#                 explain.append("Emotionally manipulative language detected")
#             if len(news.split()) < 80:
#                 explain.append("Very short articles are often unreliable")

#             if explain:
#                 st.markdown('<hr class="card-divider"><div class="card-label">Analysis Signals</div>', unsafe_allow_html=True)
#                 chips = "".join(
#                     f'<span class="signal-chip"><span class="signal-dot"></span>{e}</span>'
#                     for e in explain
#                 )
#                 st.markdown(f'<div class="signals-wrap">{chips}</div>', unsafe_allow_html=True)

#             st.markdown('</div>', unsafe_allow_html=True)

#         elif clicked and not news.strip():
#             st.markdown("""
#             <div class="verdict verdict-warning" style="margin-top:0">
#                 <span class="verdict-icon">⚠️</span>
#                 <span class="verdict-text" style="color:#92400E">Please enter some text to analyze.</span>
#             </div>
#             """, unsafe_allow_html=True)
#         else:
#             st.markdown("""
#             <div class="placeholder-card">
#                 <div class="placeholder-icon">📰</div>
#                 <div class="placeholder-text">Awaiting article input</div>
#             </div>
#             """, unsafe_allow_html=True)


# # ════════════════════════════════════════════════════════════════════════════════
# # MODULE 3 — OTP SCREENSHOT DETECTION
# # ════════════════════════════════════════════════════════════════════════════════
# elif menu == "OTP Screenshot Detection":
#     st.markdown("""
#     <div class="page-head">
#         <span class="module-tag">Module 03</span>
#         <h1>OTP Screenshot<br>Phishing Detector</h1>
#         <p>// Tesseract OCR extraction · NLP scam classification</p>
#     </div>
#     """, unsafe_allow_html=True)

#     col_l, col_r = st.columns([1, 1], gap="large")

#     with col_l:
#         st.markdown('<div class="card">', unsafe_allow_html=True)
#         st.markdown('<div class="card-label">Upload Screenshot</div>', unsafe_allow_html=True)
#         uploaded = st.file_uploader("Drag & drop or click to browse", type=["png", "jpg", "jpeg"])
#         if uploaded:
#             image = Image.open(uploaded)
#             st.image(image, caption="Uploaded Screenshot", use_container_width=True)
#         st.markdown('</div>', unsafe_allow_html=True)

#     with col_r:
#         if uploaded:
#             image = Image.open(uploaded)
#             extracted = pytesseract.image_to_string(image)

#             st.markdown('<div class="card">', unsafe_allow_html=True)
#             st.markdown('<div class="card-label">OCR — Extracted Text</div>', unsafe_allow_html=True)
#             display_text = extracted.strip() if extracted.strip() else "No readable text detected."
#             st.markdown(f'<div class="ocr-box">{display_text}</div>', unsafe_allow_html=True)
#             st.markdown('</div>', unsafe_allow_html=True)

#             red_flags = ["urgent", "click", "link", "verify", "share", "blocked",
#                          "suspend", "prize", "call now", "confirm", "account"]
#             found_flags = [w for w in red_flags if w in extracted.lower()]

#             vec = otp_vectorizer.transform([extracted])
#             probs = otp_model.predict_proba(vec)[0]
#             fake_index = list(otp_model.classes_).index("fake")
#             risk = probs[fake_index] * 100

#             sc = score_class(risk)
#             pc = progress_color(risk)

#             st.markdown('<div class="card">', unsafe_allow_html=True)
#             st.markdown('<div class="card-label">Fraud Risk Score</div>', unsafe_allow_html=True)
#             st.markdown(f"""
#             <div class="risk-score-block">
#                 <span class="risk-score-num {sc}">{risk:.1f}</span>
#                 <span class="risk-score-pct">% scam probability</span>
#             </div>
#             """, unsafe_allow_html=True)
#             inject_progress(risk, pc)
#             st.markdown(verdict_html(risk, "otp"), unsafe_allow_html=True)

#             if found_flags:
#                 st.markdown('<hr class="card-divider"><div class="card-label">Phishing Keywords</div>', unsafe_allow_html=True)
#                 chips = "".join(f'<span class="flag-chip">⚠ {f}</span>' for f in found_flags)
#                 st.markdown(f'<div style="margin-top:4px">{chips}</div>', unsafe_allow_html=True)

#             explanations = []
#             if risk > 60:
#                 explanations.append("Message uses known manipulation patterns")
#             if found_flags:
#                 explanations.append("Contains phishing keywords")
#             if "otp" in extracted.lower():
#                 explanations.append("Requests sensitive authentication code")

#             if explanations:
#                 st.markdown('<hr class="card-divider"><div class="card-label">Analysis Signals</div>', unsafe_allow_html=True)
#                 chips = "".join(
#                     f'<span class="signal-chip"><span class="signal-dot"></span>{e}</span>'
#                     for e in explanations
#                 )
#                 st.markdown(f'<div class="signals-wrap">{chips}</div>', unsafe_allow_html=True)

#             st.markdown('<hr class="card-divider"><div class="card-label">Feedback</div>', unsafe_allow_html=True)
#             feedback = st.radio(
#                 "Was this analysis accurate?",
#                 ["👍  Yes, helpful", "👎  No, incorrect"],
#                 label_visibility="collapsed"
#             )
#             if feedback == "👍  Yes, helpful":
#                 st.markdown("""
#                 <div class="verdict verdict-success" style="margin-top:0.5rem">
#                     <span class="verdict-icon">✅</span>
#                     <span class="verdict-text" style="color:#065F46">Thank you — your feedback improves the model.</span>
#                 </div>""", unsafe_allow_html=True)
#             else:
#                 st.markdown("""
#                 <div class="verdict verdict-warning" style="margin-top:0.5rem">
#                     <span class="verdict-icon">📝</span>
#                     <span class="verdict-text" style="color:#92400E">Noted — this will help improve detection accuracy.</span>
#                 </div>""", unsafe_allow_html=True)

#             st.markdown('</div>', unsafe_allow_html=True)
#         else:
#             st.markdown("""
#             <div class="placeholder-card" style="min-height:320px;">
#                 <div class="placeholder-icon">📲</div>
#                 <div class="placeholder-text">Upload a screenshot to begin</div>
#             </div>
#             """, unsafe_allow_html=True)


# import streamlit as st
# import joblib
# import numpy as np
# import pytesseract
# from PIL import Image

# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# st.set_page_config(
#     page_title="FraudX — AI Security Platform",
#     page_icon="🛡️",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # ─── SESSION STATE ───────────────────────────────────────────────────────────────
# if "page" not in st.session_state:
#     st.session_state.page = "home"

# def nav(p):
#     st.session_state.page = p
#     st.rerun()

# # ─── LOAD MODELS ────────────────────────────────────────────────────────────────
# @st.cache_resource
# def load_models():
#     try:
#         fraud_model    = joblib.load("models/fraud_model.pkl")
#         fake_model     = joblib.load("models/fake_model.pkl")
#         vectorizer     = joblib.load("models/vectorizer.pkl")
#         otp_model      = joblib.load("models/otp_model.pkl")
#         otp_vectorizer = joblib.load("models/otp_vectorizer.pkl")
#         return fraud_model, fake_model, vectorizer, otp_model, otp_vectorizer, True
#     except:
#         return None, None, None, None, None, False

# fraud_model, fake_model, vectorizer, otp_model, otp_vectorizer, models_ok = load_models()

# # ─── GLOBAL CSS ─────────────────────────────────────────────────────────────────
# st.markdown("""
# <style>
# @import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,300;0,400;0,700;0,900;1,300;1,700&family=Outfit:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

# /* ══ RESET ══ */
# *, *::before, *::after { box-sizing: border-box; }
# html, body, .stApp {
#     background: #050810 !important;
#     color: #E8EDF5 !important;
#     font-family: 'Outfit', sans-serif !important;
#     scroll-behavior: smooth;
# }
# #MainMenu, footer, header { visibility: hidden; display: none; }
# [data-testid="stSidebar"] { display: none; }
# .block-container {
#     padding: 0 !important;
#     max-width: 100% !important;
# }
# section.main > div { padding: 0 !important; }

# /* ══ NAVBAR ══ */
# .navbar {
#     position: sticky;
#     top: 0;
#     z-index: 999;
#     display: flex;
#     align-items: center;
#     justify-content: space-between;
#     padding: 0 5%;
#     height: 72px;
#     background: rgba(5,8,16,0.85);
#     backdrop-filter: blur(20px);
#     border-bottom: 1px solid rgba(255,255,255,0.06);
# }
# .nav-logo {
#     font-family: 'Fraunces', serif;
#     font-size: 1.5rem;
#     font-weight: 900;
#     color: #FFFFFF;
#     letter-spacing: -0.5px;
#     display: flex;
#     align-items: center;
#     gap: 8px;
#     cursor: pointer;
# }
# .nav-logo-dot { color: #3B82F6; }
# .nav-links {
#     display: flex;
#     align-items: center;
#     gap: 2.5rem;
# }
# .nav-link {
#     font-size: 0.88rem;
#     font-weight: 500;
#     color: #94A3B8;
#     cursor: pointer;
#     letter-spacing: 0.2px;
#     transition: color 0.2s;
#     text-decoration: none;
#     border: none;
#     background: none;
#     padding: 0;
# }
# .nav-link:hover { color: #FFFFFF; }
# .nav-link.active { color: #FFFFFF; }
# .nav-cta {
#     background: #3B82F6;
#     color: #FFFFFF !important;
#     padding: 8px 20px;
#     border-radius: 8px;
#     font-weight: 600;
#     font-size: 0.85rem;
#     cursor: pointer;
#     transition: all 0.2s;
#     border: none;
# }
# .nav-cta:hover { background: #2563EB; transform: translateY(-1px); }

# /* ══ HERO ══ */
# .hero {
#     min-height: 92vh;
#     display: flex;
#     flex-direction: column;
#     align-items: center;
#     justify-content: center;
#     text-align: center;
#     padding: 5rem 8% 4rem;
#     position: relative;
#     overflow: hidden;
# }
# .hero::before {
#     content: '';
#     position: absolute;
#     top: -20%;
#     left: 50%;
#     transform: translateX(-50%);
#     width: 900px;
#     height: 900px;
#     background: radial-gradient(ellipse, rgba(59,130,246,0.12) 0%, rgba(99,102,241,0.06) 40%, transparent 70%);
#     pointer-events: none;
# }
# .hero-badge {
#     display: inline-flex;
#     align-items: center;
#     gap: 8px;
#     background: rgba(59,130,246,0.1);
#     border: 1px solid rgba(59,130,246,0.3);
#     border-radius: 100px;
#     padding: 6px 16px;
#     font-family: 'JetBrains Mono', monospace;
#     font-size: 0.65rem;
#     color: #60A5FA;
#     letter-spacing: 2px;
#     text-transform: uppercase;
#     margin-bottom: 1.75rem;
#     animation: fadein 0.6s ease both;
# }
# .hero-badge-dot {
#     width: 6px; height: 6px;
#     background: #3B82F6;
#     border-radius: 50%;
#     animation: pulse2 2s infinite;
# }
# @keyframes pulse2 {
#     0%,100%{box-shadow:0 0 0 0 rgba(59,130,246,0.6)}
#     50%{box-shadow:0 0 0 6px rgba(59,130,246,0)}
# }
# @keyframes fadein { from{opacity:0;transform:translateY(20px)} to{opacity:1;transform:translateY(0)} }
# .hero-title {
#     font-family: 'Fraunces', serif;
#     font-size: clamp(3rem, 6vw, 5.5rem);
#     font-weight: 900;
#     line-height: 1.0;
#     letter-spacing: -2px;
#     color: #FFFFFF;
#     margin-bottom: 1.5rem;
#     animation: fadein 0.7s 0.1s ease both;
# }
# .hero-title em {
#     font-style: italic;
#     background: linear-gradient(135deg, #3B82F6, #818CF8);
#     -webkit-background-clip: text;
#     -webkit-text-fill-color: transparent;
#     background-clip: text;
# }
# .hero-sub {
#     font-size: 1.1rem;
#     color: #94A3B8;
#     max-width: 600px;
#     line-height: 1.7;
#     margin-bottom: 2.5rem;
#     animation: fadein 0.7s 0.2s ease both;
#     font-weight: 300;
# }
# .hero-btns {
#     display: flex;
#     gap: 1rem;
#     justify-content: center;
#     flex-wrap: wrap;
#     animation: fadein 0.7s 0.3s ease both;
# }
# .btn-primary {
#     background: #3B82F6;
#     color: #FFFFFF;
#     border: none;
#     border-radius: 10px;
#     padding: 14px 32px;
#     font-family: 'Outfit', sans-serif;
#     font-size: 0.95rem;
#     font-weight: 600;
#     cursor: pointer;
#     transition: all 0.2s;
#     letter-spacing: 0.3px;
# }
# .btn-primary:hover { background: #2563EB; transform: translateY(-2px); box-shadow: 0 12px 32px rgba(59,130,246,0.3); }
# .btn-outline {
#     background: transparent;
#     color: #E8EDF5;
#     border: 1px solid rgba(255,255,255,0.2);
#     border-radius: 10px;
#     padding: 14px 32px;
#     font-family: 'Outfit', sans-serif;
#     font-size: 0.95rem;
#     font-weight: 500;
#     cursor: pointer;
#     transition: all 0.2s;
# }
# .btn-outline:hover { border-color: rgba(255,255,255,0.5); background: rgba(255,255,255,0.05); }

# /* ══ STATS BAR ══ */
# .stats-bar {
#     display: flex;
#     justify-content: center;
#     gap: 0;
#     border-top: 1px solid rgba(255,255,255,0.07);
#     border-bottom: 1px solid rgba(255,255,255,0.07);
#     background: rgba(255,255,255,0.02);
#     padding: 2.5rem 8%;
#     flex-wrap: wrap;
# }
# .stat-item {
#     flex: 1;
#     min-width: 140px;
#     text-align: center;
#     padding: 0 2rem;
#     border-right: 1px solid rgba(255,255,255,0.07);
# }
# .stat-item:last-child { border-right: none; }
# .stat-num {
#     font-family: 'Fraunces', serif;
#     font-size: 2.5rem;
#     font-weight: 700;
#     color: #FFFFFF;
#     letter-spacing: -1px;
#     line-height: 1;
# }
# .stat-num span { color: #3B82F6; }
# .stat-label {
#     font-size: 0.78rem;
#     color: #64748B;
#     margin-top: 4px;
#     letter-spacing: 0.3px;
#     font-weight: 400;
# }

# /* ══ SECTION WRAPPER ══ */
# .section {
#     padding: 6rem 8%;
# }
# .section-alt {
#     background: rgba(255,255,255,0.015);
#     border-top: 1px solid rgba(255,255,255,0.05);
#     border-bottom: 1px solid rgba(255,255,255,0.05);
# }
# .section-label {
#     font-family: 'JetBrains Mono', monospace;
#     font-size: 0.6rem;
#     letter-spacing: 3px;
#     text-transform: uppercase;
#     color: #3B82F6;
#     margin-bottom: 0.75rem;
# }
# .section-title {
#     font-family: 'Fraunces', serif;
#     font-size: clamp(2rem, 3.5vw, 2.8rem);
#     font-weight: 700;
#     color: #FFFFFF;
#     letter-spacing: -0.5px;
#     line-height: 1.2;
#     margin-bottom: 1rem;
# }
# .section-sub {
#     font-size: 1rem;
#     color: #64748B;
#     line-height: 1.7;
#     max-width: 560px;
#     font-weight: 300;
# }

# /* ══ ABOUT GRID ══ */
# .about-grid {
#     display: grid;
#     grid-template-columns: 1fr 1fr;
#     gap: 5rem;
#     align-items: center;
#     padding: 6rem 8%;
# }
# .about-visual {
#     position: relative;
#     background: rgba(59,130,246,0.04);
#     border: 1px solid rgba(59,130,246,0.15);
#     border-radius: 20px;
#     padding: 2.5rem;
#     overflow: hidden;
# }
# .about-visual::before {
#     content: '';
#     position: absolute;
#     top: -50%;
#     right: -30%;
#     width: 400px;
#     height: 400px;
#     background: radial-gradient(ellipse, rgba(59,130,246,0.1) 0%, transparent 60%);
# }
# .av-row {
#     display: flex;
#     align-items: center;
#     justify-content: space-between;
#     padding: 0.85rem 1rem;
#     background: rgba(255,255,255,0.03);
#     border: 1px solid rgba(255,255,255,0.06);
#     border-radius: 10px;
#     margin-bottom: 0.6rem;
#     font-family: 'JetBrains Mono', monospace;
#     font-size: 0.72rem;
#     color: #94A3B8;
# }
# .av-row-val { color: #FFFFFF; font-weight: 500; }
# .av-row-badge {
#     font-size: 0.6rem;
#     padding: 2px 8px;
#     border-radius: 100px;
#     font-weight: 500;
# }
# .badge-green { background: rgba(16,185,129,0.15); color: #10B981; border: 1px solid rgba(16,185,129,0.3); }
# .badge-red   { background: rgba(239,68,68,0.15);  color: #EF4444; border: 1px solid rgba(239,68,68,0.3); }
# .badge-amber { background: rgba(245,158,11,0.15); color: #F59E0B; border: 1px solid rgba(245,158,11,0.3); }

# /* ══ SERVICES CARDS ══ */
# .services-grid {
#     display: grid;
#     grid-template-columns: repeat(3, 1fr);
#     gap: 1.25rem;
#     margin-top: 3rem;
# }
# .service-card {
#     background: rgba(255,255,255,0.03);
#     border: 1px solid rgba(255,255,255,0.08);
#     border-radius: 18px;
#     padding: 2rem;
#     cursor: pointer;
#     transition: all 0.3s ease;
#     position: relative;
#     overflow: hidden;
# }
# .service-card::before {
#     content: '';
#     position: absolute;
#     top: 0; left: 0; right: 0;
#     height: 2px;
#     background: linear-gradient(90deg, #3B82F6, #818CF8);
#     opacity: 0;
#     transition: opacity 0.3s;
# }
# .service-card:hover {
#     background: rgba(59,130,246,0.06);
#     border-color: rgba(59,130,246,0.3);
#     transform: translateY(-4px);
#     box-shadow: 0 20px 60px rgba(0,0,0,0.3);
# }
# .service-card:hover::before { opacity: 1; }
# .sc-icon {
#     width: 48px; height: 48px;
#     background: rgba(59,130,246,0.12);
#     border: 1px solid rgba(59,130,246,0.25);
#     border-radius: 12px;
#     display: flex;
#     align-items: center;
#     justify-content: center;
#     font-size: 1.3rem;
#     margin-bottom: 1.25rem;
# }
# .sc-title {
#     font-family: 'Fraunces', serif;
#     font-size: 1.2rem;
#     font-weight: 700;
#     color: #FFFFFF;
#     margin-bottom: 0.6rem;
#     letter-spacing: -0.3px;
# }
# .sc-desc {
#     font-size: 0.85rem;
#     color: #64748B;
#     line-height: 1.6;
#     margin-bottom: 1.5rem;
#     font-weight: 300;
# }
# .sc-tag {
#     font-family: 'JetBrains Mono', monospace;
#     font-size: 0.6rem;
#     color: #3B82F6;
#     letter-spacing: 1.5px;
#     text-transform: uppercase;
# }
# .sc-launch {
#     display: inline-flex;
#     align-items: center;
#     gap: 6px;
#     background: #3B82F6;
#     color: #fff;
#     border: none;
#     border-radius: 8px;
#     padding: 8px 16px;
#     font-family: 'Outfit', sans-serif;
#     font-size: 0.8rem;
#     font-weight: 600;
#     cursor: pointer;
#     transition: all 0.2s;
#     margin-top: 0.25rem;
# }
# .sc-launch:hover { background: #2563EB; }

# /* ══ HOW IT WORKS ══ */
# .how-grid {
#     display: grid;
#     grid-template-columns: repeat(4, 1fr);
#     gap: 1.5rem;
#     margin-top: 3rem;
# }
# .how-step {
#     text-align: center;
#     padding: 1.5rem;
#     position: relative;
# }
# .how-step:not(:last-child)::after {
#     content: '→';
#     position: absolute;
#     right: -0.75rem;
#     top: 50%;
#     transform: translateY(-50%);
#     color: rgba(255,255,255,0.15);
#     font-size: 1.2rem;
# }
# .how-num {
#     font-family: 'Fraunces', serif;
#     font-size: 3rem;
#     font-weight: 900;
#     color: rgba(59,130,246,0.2);
#     line-height: 1;
#     margin-bottom: 0.75rem;
# }
# .how-title {
#     font-size: 0.95rem;
#     font-weight: 600;
#     color: #E8EDF5;
#     margin-bottom: 0.4rem;
# }
# .how-desc { font-size: 0.8rem; color: #64748B; line-height: 1.5; font-weight: 300; }

# /* ══ TESTIMONIALS ══ */
# .testi-grid {
#     display: grid;
#     grid-template-columns: repeat(3, 1fr);
#     gap: 1.25rem;
#     margin-top: 3rem;
# }
# .testi-card {
#     background: rgba(255,255,255,0.03);
#     border: 1px solid rgba(255,255,255,0.07);
#     border-radius: 16px;
#     padding: 1.75rem;
#     transition: border-color 0.3s;
# }
# .testi-card:hover { border-color: rgba(59,130,246,0.3); }
# .testi-stars { color: #F59E0B; font-size: 0.85rem; margin-bottom: 1rem; letter-spacing: 2px; }
# .testi-text {
#     font-size: 0.88rem;
#     color: #94A3B8;
#     line-height: 1.7;
#     margin-bottom: 1.25rem;
#     font-weight: 300;
#     font-style: italic;
# }
# .testi-author { display: flex; align-items: center; gap: 10px; }
# .testi-avatar {
#     width: 38px; height: 38px;
#     border-radius: 50%;
#     display: flex;
#     align-items: center;
#     justify-content: center;
#     font-weight: 700;
#     font-size: 0.8rem;
#     color: #FFFFFF;
#     flex-shrink: 0;
# }
# .testi-name { font-size: 0.85rem; font-weight: 600; color: #E8EDF5; }
# .testi-role { font-size: 0.72rem; color: #475569; margin-top: 1px; font-family: 'JetBrains Mono', monospace; }

# /* ══ CONTACT ══ */
# .contact-grid {
#     display: grid;
#     grid-template-columns: 1fr 1.4fr;
#     gap: 4rem;
#     align-items: start;
#     padding: 6rem 8%;
# }
# .contact-info-item {
#     display: flex;
#     gap: 1rem;
#     margin-bottom: 1.75rem;
# }
# .ci-icon {
#     width: 42px; height: 42px;
#     background: rgba(59,130,246,0.1);
#     border: 1px solid rgba(59,130,246,0.25);
#     border-radius: 10px;
#     display: flex;
#     align-items: center;
#     justify-content: center;
#     font-size: 1.1rem;
#     flex-shrink: 0;
# }
# .ci-label { font-size: 0.72rem; color: #475569; font-family: 'JetBrains Mono', monospace; letter-spacing: 1px; text-transform: uppercase; }
# .ci-val { font-size: 0.9rem; color: #E8EDF5; font-weight: 500; margin-top: 2px; }
# .contact-form-wrap {
#     background: rgba(255,255,255,0.03);
#     border: 1px solid rgba(255,255,255,0.08);
#     border-radius: 20px;
#     padding: 2.25rem;
# }
# .form-row { margin-bottom: 1.1rem; }
# .form-label {
#     display: block;
#     font-family: 'JetBrains Mono', monospace;
#     font-size: 0.6rem;
#     letter-spacing: 2px;
#     text-transform: uppercase;
#     color: #475569;
#     margin-bottom: 6px;
# }

# /* ══ INPUT OVERRIDES ══ */
# [data-testid="stTextInput"] label,
# [data-testid="stTextArea"] label,
# [data-testid="stNumberInput"] label,
# [data-testid="stSelectbox"] label,
# [data-testid="stFileUploader"] label {
#     font-family: 'JetBrains Mono', monospace !important;
#     font-size: 0.62rem !important;
#     letter-spacing: 2px !important;
#     text-transform: uppercase !important;
#     color: #475569 !important;
# }
# [data-testid="stTextInput"] input,
# [data-testid="stNumberInput"] input {
#     background: rgba(255,255,255,0.04) !important;
#     border: 1px solid rgba(255,255,255,0.1) !important;
#     border-radius: 10px !important;
#     color: #E8EDF5 !important;
#     font-family: 'Outfit', sans-serif !important;
#     font-size: 0.9rem !important;
# }
# [data-testid="stTextInput"] input:focus,
# [data-testid="stNumberInput"] input:focus {
#     border-color: rgba(59,130,246,0.6) !important;
#     box-shadow: 0 0 0 3px rgba(59,130,246,0.1) !important;
# }
# [data-testid="stTextArea"] textarea {
#     background: rgba(255,255,255,0.04) !important;
#     border: 1px solid rgba(255,255,255,0.1) !important;
#     border-radius: 10px !important;
#     color: #E8EDF5 !important;
#     font-family: 'Outfit', sans-serif !important;
#     font-size: 0.9rem !important;
#     min-height: 130px !important;
#     line-height: 1.6 !important;
# }
# [data-testid="stTextArea"] textarea:focus {
#     border-color: rgba(59,130,246,0.6) !important;
#     box-shadow: 0 0 0 3px rgba(59,130,246,0.1) !important;
# }
# [data-testid="stTextArea"] textarea::placeholder,
# [data-testid="stTextInput"] input::placeholder { color: #334155 !important; }
# [data-testid="stSelectbox"] > div > div {
#     background: rgba(255,255,255,0.04) !important;
#     border: 1px solid rgba(255,255,255,0.1) !important;
#     border-radius: 10px !important;
#     color: #E8EDF5 !important;
#     font-family: 'Outfit', sans-serif !important;
# }

# /* ══ BUTTON OVERRIDES ══ */
# .stButton > button {
#     background: #3B82F6 !important;
#     color: #FFFFFF !important;
#     font-family: 'Outfit', sans-serif !important;
#     font-weight: 600 !important;
#     font-size: 0.9rem !important;
#     border: none !important;
#     border-radius: 10px !important;
#     padding: 0.7rem 1.5rem !important;
#     width: 100% !important;
#     transition: all 0.2s !important;
#     cursor: pointer !important;
#     letter-spacing: 0.3px !important;
# }
# .stButton > button:hover {
#     background: #2563EB !important;
#     transform: translateY(-2px) !important;
#     box-shadow: 0 10px 30px rgba(59,130,246,0.3) !important;
# }

# /* ══ PROGRESS ══ */
# [data-testid="stProgress"] > div > div {
#     background: rgba(255,255,255,0.08) !important;
#     border-radius: 100px !important;
#     height: 8px !important;
# }
# [data-testid="stProgress"] > div > div > div > div {
#     border-radius: 100px !important;
#     height: 8px !important;
# }

# /* ══ MODULE PAGE ══ */
# .module-page {
#     min-height: 100vh;
#     padding: 3rem 8%;
#     background: #050810;
# }
# .module-header {
#     display: flex;
#     align-items: center;
#     gap: 1rem;
#     margin-bottom: 2.5rem;
#     padding-bottom: 1.5rem;
#     border-bottom: 1px solid rgba(255,255,255,0.07);
# }
# .module-icon {
#     width: 52px; height: 52px;
#     background: rgba(59,130,246,0.12);
#     border: 1px solid rgba(59,130,246,0.3);
#     border-radius: 14px;
#     display: flex;
#     align-items: center;
#     justify-content: center;
#     font-size: 1.5rem;
# }
# .module-title {
#     font-family: 'Fraunces', serif;
#     font-size: 1.9rem;
#     font-weight: 700;
#     color: #FFFFFF;
#     letter-spacing: -0.5px;
#     line-height: 1.1;
# }
# .module-tag {
#     font-family: 'JetBrains Mono', monospace;
#     font-size: 0.58rem;
#     color: #3B82F6;
#     letter-spacing: 2px;
#     text-transform: uppercase;
#     margin-top: 2px;
# }
# .analysis-card {
#     background: rgba(255,255,255,0.03);
#     border: 1px solid rgba(255,255,255,0.08);
#     border-radius: 16px;
#     padding: 1.75rem;
#     margin-bottom: 1rem;
# }
# .ac-label {
#     font-family: 'JetBrains Mono', monospace;
#     font-size: 0.58rem;
#     letter-spacing: 2.5px;
#     text-transform: uppercase;
#     color: #475569;
#     margin-bottom: 1rem;
# }
# .score-display {
#     display: flex;
#     align-items: baseline;
#     gap: 8px;
#     margin-bottom: 10px;
# }
# .score-number {
#     font-family: 'Fraunces', serif;
#     font-size: 3.5rem;
#     font-weight: 900;
#     letter-spacing: -3px;
#     line-height: 1;
# }
# .score-unit { font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; color: #475569; }
# .score-red    { color: #EF4444; }
# .score-amber  { color: #F59E0B; }
# .score-green  { color: #10B981; }
# .verdict-box {
#     display: flex;
#     align-items: center;
#     gap: 10px;
#     padding: 0.9rem 1.1rem;
#     border-radius: 10px;
#     font-size: 0.88rem;
#     font-weight: 500;
#     margin: 0.85rem 0;
# }
# .vb-danger  { background: rgba(239,68,68,0.1);  border: 1px solid rgba(239,68,68,0.3);  color: #FCA5A5; }
# .vb-warning { background: rgba(245,158,11,0.1); border: 1px solid rgba(245,158,11,0.3); color: #FCD34D; }
# .vb-success { background: rgba(16,185,129,0.1); border: 1px solid rgba(16,185,129,0.3); color: #6EE7B7; }
# .ac-divider { border: none; border-top: 1px solid rgba(255,255,255,0.06); margin: 1.1rem 0; }
# .chip-wrap { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 4px; }
# .chip-signal {
#     display: inline-flex; align-items: center; gap: 6px;
#     background: rgba(255,255,255,0.04);
#     border: 1px solid rgba(255,255,255,0.08);
#     border-radius: 8px; padding: 5px 10px;
#     font-size: 0.75rem; color: #94A3B8;
#     font-family: 'Outfit', sans-serif;
# }
# .chip-dot { width:5px; height:5px; border-radius:50%; background:#3B82F6; flex-shrink:0; }
# .chip-warn {
#     background: rgba(245,158,11,0.08);
#     border: 1px solid rgba(245,158,11,0.2);
#     border-radius: 6px; padding: 3px 9px;
#     font-size: 0.7rem; color: #FCD34D;
#     font-family: 'JetBrains Mono', monospace;
#     display: inline-block; margin: 2px;
# }
# .ocr-display {
#     background: rgba(0,0,0,0.3);
#     border: 1px solid rgba(255,255,255,0.07);
#     border-radius: 10px; padding: 1rem;
#     font-family: 'JetBrains Mono', monospace;
#     font-size: 0.72rem; color: #64748B;
#     line-height: 1.8; max-height: 150px;
#     overflow-y: auto; white-space: pre-wrap;
# }
# .placeholder-module {
#     display: flex; flex-direction: column;
#     align-items: center; justify-content: center;
#     min-height: 240px;
#     background: rgba(255,255,255,0.01);
#     border: 1px dashed rgba(255,255,255,0.08);
#     border-radius: 16px; gap: 10px;
# }
# .pm-icon { font-size: 2.5rem; opacity: 0.2; }
# .pm-text { font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; letter-spacing: 2px; text-transform: uppercase; color: #1E293B; }

# /* ══ FILE UPLOADER ══ */
# [data-testid="stFileUploader"] section {
#     background: rgba(255,255,255,0.02) !important;
#     border: 2px dashed rgba(59,130,246,0.25) !important;
#     border-radius: 12px !important;
# }
# [data-testid="stFileUploader"] section:hover {
#     border-color: rgba(59,130,246,0.5) !important;
#     background: rgba(59,130,246,0.03) !important;
# }
# [data-testid="stFileUploader"] section p,
# [data-testid="stFileUploader"] section small,
# [data-testid="stFileUploader"] section span { color: #475569 !important; }

# /* ══ RADIO ══ */
# [data-testid="stRadio"] > label {
#     font-family: 'JetBrains Mono', monospace !important;
#     font-size: 0.6rem !important; letter-spacing: 2px !important;
#     text-transform: uppercase !important; color: #475569 !important;
# }
# [data-testid="stRadio"] div[role="radiogroup"] > label {
#     font-size: 0.85rem !important; color: #94A3B8 !important;
#     text-transform: none !important; letter-spacing: 0 !important;
#     font-family: 'Outfit', sans-serif !important;
# }

# /* ══ FOOTER ══ */
# .footer {
#     background: rgba(0,0,0,0.4);
#     border-top: 1px solid rgba(255,255,255,0.06);
#     padding: 3rem 8%;
#     display: flex;
#     justify-content: space-between;
#     align-items: center;
#     flex-wrap: wrap;
#     gap: 1rem;
# }
# .footer-brand {
#     font-family: 'Fraunces', serif;
#     font-size: 1.2rem;
#     font-weight: 700;
#     color: #FFFFFF;
# }
# .footer-copy { font-size: 0.78rem; color: #334155; margin-top: 3px; }
# .footer-links { display: flex; gap: 1.5rem; flex-wrap: wrap; }
# .footer-link { font-size: 0.82rem; color: #475569; cursor: pointer; transition: color 0.2s; }
# .footer-link:hover { color: #94A3B8; }

# /* ══ SCROLLBAR ══ */
# ::-webkit-scrollbar { width: 5px; }
# ::-webkit-scrollbar-track { background: transparent; }
# ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 3px; }
# </style>
# """, unsafe_allow_html=True)


# # ─── HELPERS ────────────────────────────────────────────────────────────────────
# def score_class(p):
#     if p > 70: return "score-red"
#     if p > 40: return "score-amber"
#     return "score-green"

# def vb_class(p):
#     if p > 70: return "vb-danger"
#     if p > 40: return "vb-warning"
#     return "vb-success"

# def progress_color_css(p):
#     c = "#EF4444" if p > 70 else ("#F59E0B" if p > 40 else "#10B981")
#     return f"""
#     <style>
#     [data-testid="stProgress"] > div > div > div > div {{
#         background: {c} !important;
#     }}
#     </style>
#     """

# VERDICTS = {
#     "fraud": {
#         "high": ("🚨", "High Fraud Risk — Do not proceed with this transaction."),
#         "med":  ("⚠️", "Suspicious — Manual review is recommended."),
#         "low":  ("✅", "Transaction Appears Normal."),
#     },
#     "news": {
#         "high": ("🚨", "Likely Fake News — Verify before sharing."),
#         "med":  ("⚠️", "Needs Verification — Cross-check sources."),
#         "low":  ("✅", "Content Appears Credible."),
#     },
#     "otp": {
#         "high": ("🚨", "High Risk — This is very likely a scam."),
#         "med":  ("⚠️", "Medium Risk — Treat with caution."),
#         "low":  ("✅", "Low Risk — Appears legitimate."),
#     },
# }

# def verdict_html(p, mode):
#     tier = "high" if p > 70 else ("med" if p > 40 else "low")
#     cls = vb_class(p)
#     icon, text = VERDICTS[mode][tier]
#     return f'<div class="verdict-box {cls}">{icon}&nbsp;&nbsp;{text}</div>'


# # ═══════════════════════════════════════════════════════════════════════════════
# # NAVBAR
# # ═══════════════════════════════════════════════════════════════════════════════
# pg = st.session_state.page

# def navbar():
#     c1, c2, c3, c4, c5, c6, c7 = st.columns([2, 1, 1, 1, 1, 1, 1.2])
#     with c1:
#         if st.button("🛡️ FraudX", key="nav_logo"):
#             nav("home")
#     with c2:
#         if st.button("Home", key="nav_home"):
#             nav("home")
#     with c3:
#         if st.button("About", key="nav_about"):
#             nav("about")
#     with c4:
#         if st.button("Services", key="nav_svc"):
#             nav("services")
#     with c5:
#         if st.button("Reviews", key="nav_rev"):
#             nav("reviews")
#     with c6:
#         if st.button("Contact", key="nav_contact"):
#             nav("contact")
#     with c7:
#         if st.button("⚡ Launch App", key="nav_launch"):
#             nav("services")

# st.markdown("""
# <div class="navbar">
#   <div class="nav-logo">🛡️ Fraud<span class="nav-logo-dot">X</span></div>
#   <div class="nav-links">
#     <span class="nav-link">Home</span>
#     <span class="nav-link">About</span>
#     <span class="nav-link">Services</span>
#     <span class="nav-link">Reviews</span>
#     <span class="nav-link">Contact</span>
#     <span class="nav-cta">⚡ Launch App</span>
#   </div>
# </div>
# """, unsafe_allow_html=True)

# # Real clickable nav
# with st.container():
#     nav_cols = st.columns([2.5, 0.7, 0.7, 0.7, 0.7, 0.7, 1.2])
#     with nav_cols[0]:
#         if st.button("🛡️  FraudX", key="logo_btn"):
#             nav("home")
#     with nav_cols[1]:
#         if st.button("Home", key="home_btn"):
#             nav("home")
#     with nav_cols[2]:
#         if st.button("About", key="about_btn"):
#             nav("about")
#     with nav_cols[3]:
#         if st.button("Services", key="svc_btn"):
#             nav("services")
#     with nav_cols[4]:
#         if st.button("Reviews", key="rev_btn"):
#             nav("reviews")
#     with nav_cols[5]:
#         if st.button("Contact", key="contact_btn"):
#             nav("contact")
#     with nav_cols[6]:
#         if st.button("⚡ Launch App →", key="launch_btn"):
#             nav("services")

# st.markdown("""
# <style>
# /* Hide the real button bar — nav is visual only via real buttons below */
# div[data-testid="stHorizontalBlock"]:has(button) button {
#     background: transparent !important;
#     border: none !important;
#     color: #64748B !important;
#     font-family: 'Outfit', sans-serif !important;
#     font-weight: 500 !important;
#     font-size: 0.85rem !important;
#     padding: 0 !important;
#     box-shadow: none !important;
#     width: auto !important;
#     letter-spacing: 0 !important;
#     margin-top: -20px !important;
#     display: none !important;
# }
# </style>
# """, unsafe_allow_html=True)


# # ═══════════════════════════════════════════════════════════════════════════════
# # PAGE — HOME
# # ═══════════════════════════════════════════════════════════════════════════════
# if pg == "home":

#     # Hero
#     st.markdown("""
#     <div class="hero">
#         <div class="hero-badge"><span class="hero-badge-dot"></span> AI-Powered Security Intelligence</div>
#         <h1 class="hero-title">Detect Fraud.<br><em>Before It Happens.</em></h1>
#         <p class="hero-sub">FraudX uses state-of-the-art machine learning to protect your transactions, verify news authenticity, and detect phishing scams in real time.</p>
#         <div class="hero-btns">
#             <button class="btn-primary" onclick="">Explore Services</button>
#             <button class="btn-outline" onclick="">Learn More</button>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)

#     hc1, hc2, hc3 = st.columns(3)
#     with hc1:
#         if st.button("🚀  Explore Services", key="hero_explore"):
#             nav("services")
#     with hc2:
#         if st.button("📖  Learn More", key="hero_learn"):
#             nav("about")
#     with hc3:
#         pass

#     # Stats
#     st.markdown("""
#     <div class="stats-bar">
#         <div class="stat-item">
#             <div class="stat-num">99<span>.2%</span></div>
#             <div class="stat-label">Fraud Detection Accuracy</div>
#         </div>
#         <div class="stat-item">
#             <div class="stat-num">3<span>M+</span></div>
#             <div class="stat-label">Transactions Analyzed</div>
#         </div>
#         <div class="stat-item">
#             <div class="stat-num">0.3<span>s</span></div>
#             <div class="stat-label">Average Response Time</div>
#         </div>
#         <div class="stat-item">
#             <div class="stat-num">3</div>
#             <div class="stat-label">AI Security Modules</div>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)

#     # Services preview
#     st.markdown("""
#     <div class="section">
#         <div class="section-label">What We Do</div>
#         <div class="section-title">Three Powerful<br>Security Modules</div>
#         <p class="section-sub">From transaction fraud to fake news and phishing OTPs — FraudX covers every attack vector.</p>
#         <div class="services-grid">
#             <div class="service-card">
#                 <div class="sc-icon">💳</div>
#                 <div class="sc-title">Fraud Detection</div>
#                 <p class="sc-desc">Real-time credit card transaction analysis using a Random Forest model trained on 284,000+ transactions. Get instant risk scores and detailed reasoning.</p>
#                 <div class="sc-tag">Random Forest · 30 Features</div>
#             </div>
#             <div class="service-card">
#                 <div class="sc-icon">📰</div>
#                 <div class="sc-title">Fake News Detection</div>
#                 <p class="sc-desc">Analyze news articles and headlines for misinformation patterns using TF-IDF vectorization and logistic regression trained on verified datasets.</p>
#                 <div class="sc-tag">TF-IDF · Logistic Regression</div>
#             </div>
#             <div class="service-card">
#                 <div class="sc-icon">📲</div>
#                 <div class="sc-title">OTP Phishing Detector</div>
#                 <p class="sc-desc">Upload screenshots of suspicious messages. OCR extracts the text and our NLP model classifies whether it's a scam or legitimate OTP message.</p>
#                 <div class="sc-tag">Tesseract OCR · NLP Classifier</div>
#             </div>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)

#     sc1, sc2, sc3 = st.columns(3)
#     with sc1:
#         if st.button("Launch Fraud Detector →", key="home_fraud"):
#             nav("fraud")
#     with sc2:
#         if st.button("Launch News Detector →", key="home_news"):
#             nav("news")
#     with sc3:
#         if st.button("Launch OTP Detector →", key="home_otp"):
#             nav("otp")

#     # How it works
#     st.markdown("""
#     <div class="section section-alt">
#         <div style="text-align:center;margin-bottom:0.5rem">
#             <div class="section-label" style="text-align:center">How It Works</div>
#             <div class="section-title" style="text-align:center">Simple. Fast. Accurate.</div>
#         </div>
#         <div class="how-grid">
#             <div class="how-step">
#                 <div class="how-num">01</div>
#                 <div class="how-title">Input Data</div>
#                 <p class="how-desc">Enter transaction details, paste an article, or upload a screenshot.</p>
#             </div>
#             <div class="how-step">
#                 <div class="how-num">02</div>
#                 <div class="how-title">AI Processing</div>
#                 <p class="how-desc">Our ML models analyze your input against millions of patterns.</p>
#             </div>
#             <div class="how-step">
#                 <div class="how-num">03</div>
#                 <div class="how-title">Risk Scoring</div>
#                 <p class="how-desc">Receive a precise probability score with detailed explanations.</p>
#             </div>
#             <div class="how-step">
#                 <div class="how-num">04</div>
#                 <div class="how-title">Take Action</div>
#                 <p class="how-desc">Act on clear verdicts: safe, suspicious, or high risk.</p>
#             </div>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)

#     # Testimonials preview
#     st.markdown("""
#     <div class="section">
#         <div class="section-label">Testimonials</div>
#         <div class="section-title">Trusted by Professionals</div>
#         <div class="testi-grid">
#             <div class="testi-card">
#                 <div class="testi-stars">★★★★★</div>
#                 <p class="testi-text">"FraudX flagged a suspicious transaction that our traditional system missed. The 0.3-second response time is incredible for a system this accurate."</p>
#                 <div class="testi-author">
#                     <div class="testi-avatar" style="background:#3B82F6">AK</div>
#                     <div><div class="testi-name">Ahmed Khan</div><div class="testi-role">Risk Analyst · FinTech</div></div>
#                 </div>
#             </div>
#             <div class="testi-card">
#                 <div class="testi-stars">★★★★★</div>
#                 <p class="testi-text">"The fake news module is remarkably accurate. It caught misinformation patterns in an article that appeared legitimate on the surface. Essential tool."</p>
#                 <div class="testi-author">
#                     <div class="testi-avatar" style="background:#8B5CF6">SR</div>
#                     <div><div class="testi-name">Sara Raza</div><div class="testi-role">Journalist · Media Verification</div></div>
#                 </div>
#             </div>
#             <div class="testi-card">
#                 <div class="testi-stars">★★★★☆</div>
#                 <p class="testi-text">"The OTP screenshot detector saved one of our customers from a phishing scam. Simple upload, instant verdict. The UI is clean and the logic is solid."</p>
#                 <div class="testi-author">
#                     <div class="testi-avatar" style="background:#10B981">ZM</div>
#                     <div><div class="testi-name">Zain Malik</div><div class="testi-role">CTO · Cybersecurity Startup</div></div>
#                 </div>
#             </div>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)

#     # Footer
#     st.markdown("""
#     <div class="footer">
#         <div>
#             <div class="footer-brand">🛡️ FraudX</div>
#             <div class="footer-copy">© 2025 FraudX. AI-Powered Security Platform.</div>
#         </div>
#         <div class="footer-links">
#             <span class="footer-link">Privacy Policy</span>
#             <span class="footer-link">Terms of Service</span>
#             <span class="footer-link">Documentation</span>
#             <span class="footer-link">GitHub</span>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)


# # ═══════════════════════════════════════════════════════════════════════════════
# # PAGE — ABOUT
# # ═══════════════════════════════════════════════════════════════════════════════
# elif pg == "about":
#     st.markdown("""
#     <div class="about-grid">
#         <div>
#             <div class="section-label">About FraudX</div>
#             <div class="section-title">Built to Stop Fraud<br>Before It Costs You</div>
#             <p style="color:#64748B;font-size:0.95rem;line-height:1.8;margin:1.25rem 0;font-weight:300;">
#                 FraudX is an AI-powered security intelligence platform combining three cutting-edge machine learning models into a single, unified interface. Built for analysts, journalists, and security professionals who need fast, reliable, explainable AI decisions.
#             </p>
#             <p style="color:#64748B;font-size:0.95rem;line-height:1.8;margin-bottom:1.75rem;font-weight:300;">
#                 Our models are trained on industry-standard datasets — the Kaggle Credit Card Fraud dataset, ISOT Fake News dataset, and a custom OTP phishing corpus — delivering production-grade accuracy you can trust.
#             </p>
#             <div style="display:flex;gap:2rem;flex-wrap:wrap;margin-top:1rem">
#                 <div>
#                     <div style="font-family:'Fraunces',serif;font-size:2rem;font-weight:700;color:#3B82F6">284K+</div>
#                     <div style="font-size:0.78rem;color:#475569;margin-top:2px">Training Samples</div>
#                 </div>
#                 <div>
#                     <div style="font-family:'Fraunces',serif;font-size:2rem;font-weight:700;color:#3B82F6">3</div>
#                     <div style="font-size:0.78rem;color:#475569;margin-top:2px">AI Models</div>
#                 </div>
#                 <div>
#                     <div style="font-family:'Fraunces',serif;font-size:2rem;font-weight:700;color:#3B82F6">99.2%</div>
#                     <div style="font-size:0.78rem;color:#475569;margin-top:2px">Fraud Accuracy</div>
#                 </div>
#             </div>
#         </div>
#         <div class="about-visual">
#             <div style="font-family:'JetBrains Mono',monospace;font-size:0.6rem;color:#3B82F6;letter-spacing:2px;text-transform:uppercase;margin-bottom:1rem">Live Model Output</div>
#             <div class="av-row">
#                 <span>Transaction #TXN-0042</span>
#                 <span class="av-row-val">$87,500</span>
#                 <span class="av-row-badge badge-red">HIGH RISK</span>
#             </div>
#             <div class="av-row">
#                 <span>Transaction #TXN-0043</span>
#                 <span class="av-row-val">$1,200</span>
#                 <span class="av-row-badge badge-green">SAFE</span>
#             </div>
#             <div class="av-row">
#                 <span>Article: "SHOCKING: Secret..."</span>
#                 <span class="av-row-val">91.4%</span>
#                 <span class="av-row-badge badge-red">FAKE</span>
#             </div>
#             <div class="av-row">
#                 <span>Article: "Fed raises rates by..."</span>
#                 <span class="av-row-val">8.2%</span>
#                 <span class="av-row-badge badge-green">CREDIBLE</span>
#             </div>
#             <div class="av-row">
#                 <span>OTP Screenshot #48</span>
#                 <span class="av-row-val">78.3%</span>
#                 <span class="av-row-badge badge-amber">SUSPICIOUS</span>
#             </div>
#             <div class="av-row">
#                 <span>OTP Screenshot #49</span>
#                 <span class="av-row-val">4.1%</span>
#                 <span class="av-row-badge badge-green">LEGIT</span>
#             </div>
#         </div>
#     </div>

#     <div class="section section-alt">
#         <div style="text-align:center">
#             <div class="section-label">Tech Stack</div>
#             <div class="section-title">Powered by Proven Technology</div>
#         </div>
#         <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;margin-top:2.5rem">
#             <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);border-radius:14px;padding:1.5rem;text-align:center">
#                 <div style="font-size:2rem;margin-bottom:0.5rem">🌲</div>
#                 <div style="font-weight:600;color:#E8EDF5;margin-bottom:4px">Random Forest</div>
#                 <div style="font-size:0.75rem;color:#475569">Fraud classification with 100 estimators on PCA-transformed transaction data</div>
#             </div>
#             <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);border-radius:14px;padding:1.5rem;text-align:center">
#                 <div style="font-size:2rem;margin-bottom:0.5rem">📊</div>
#                 <div style="font-weight:600;color:#E8EDF5;margin-bottom:4px">TF-IDF + LR</div>
#                 <div style="font-size:0.75rem;color:#475569">5,000 feature text vectorization with logistic regression for news analysis</div>
#             </div>
#             <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);border-radius:14px;padding:1.5rem;text-align:center">
#                 <div style="font-size:2rem;margin-bottom:0.5rem">👁️</div>
#                 <div style="font-weight:600;color:#E8EDF5;margin-bottom:4px">Tesseract OCR</div>
#                 <div style="font-size:0.75rem;color:#475569">Image-to-text extraction from screenshots with preprocessing pipeline</div>
#             </div>
#             <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);border-radius:14px;padding:1.5rem;text-align:center">
#                 <div style="font-size:2rem;margin-bottom:0.5rem">⚡</div>
#                 <div style="font-weight:600;color:#E8EDF5;margin-bottom:4px">Streamlit</div>
#                 <div style="font-size:0.75rem;color:#475569">Python-native web framework with real-time inference and model caching</div>
#             </div>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)


# # ═══════════════════════════════════════════════════════════════════════════════
# # PAGE — SERVICES
# # ═══════════════════════════════════════════════════════════════════════════════
# elif pg == "services":
#     st.markdown("""
#     <div class="section">
#         <div class="section-label">Our Services</div>
#         <div class="section-title">Choose a Module</div>
#         <p class="section-sub">Each module is an independent AI system. Select one below to run a live analysis.</p>
#         <div class="services-grid">
#             <div class="service-card">
#                 <div class="sc-icon">💳</div>
#                 <div class="sc-title">Fraud Detection</div>
#                 <p class="sc-desc">Analyze credit card transactions in real time. Enter an amount and get an instant fraud risk score backed by a Random Forest model.</p>
#                 <div class="sc-tag" style="margin-bottom:1rem">Random Forest · 99.2% Accuracy</div>
#             </div>
#             <div class="service-card">
#                 <div class="sc-icon">📰</div>
#                 <div class="sc-title">Fake News Detection</div>
#                 <p class="sc-desc">Paste any article or headline and receive a misinformation probability score with language pattern analysis.</p>
#                 <div class="sc-tag" style="margin-bottom:1rem">TF-IDF · Logistic Regression</div>
#             </div>
#             <div class="service-card">
#                 <div class="sc-icon">📲</div>
#                 <div class="sc-title">OTP Phishing Detector</div>
#                 <p class="sc-desc">Upload a screenshot of a suspicious OTP message. Our OCR + NLP pipeline extracts text and classifies the scam risk instantly.</p>
#                 <div class="sc-tag" style="margin-bottom:1rem">Tesseract OCR · NLP Model</div>
#             </div>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)

#     bc1, bc2, bc3 = st.columns(3)
#     with bc1:
#         if st.button("💳  Open Fraud Detector", key="svc_fraud"):
#             nav("fraud")
#     with bc2:
#         if st.button("📰  Open News Detector", key="svc_news"):
#             nav("news")
#     with bc3:
#         if st.button("📲  Open OTP Detector", key="svc_otp"):
#             nav("otp")


# # ═══════════════════════════════════════════════════════════════════════════════
# # PAGE — REVIEWS
# # ═══════════════════════════════════════════════════════════════════════════════
# elif pg == "reviews":
#     st.markdown("""
#     <div class="section">
#         <div class="section-label">Reviews & Testimonials</div>
#         <div class="section-title">What Our Users Say</div>
#         <div class="testi-grid">
#             <div class="testi-card">
#                 <div class="testi-stars">★★★★★</div>
#                 <p class="testi-text">"FraudX flagged a suspicious high-value transaction our legacy system marked as safe. The model explanations are clear and actionable."</p>
#                 <div class="testi-author">
#                     <div class="testi-avatar" style="background:#3B82F6">AK</div>
#                     <div><div class="testi-name">Ahmed Khan</div><div class="testi-role">Risk Analyst · FinTech Corp</div></div>
#                 </div>
#             </div>
#             <div class="testi-card">
#                 <div class="testi-stars">★★★★★</div>
#                 <p class="testi-text">"As a journalist, I use the Fake News module daily. It catches subtle manipulation patterns that aren't obvious. An essential fact-checking tool."</p>
#                 <div class="testi-author">
#                     <div class="testi-avatar" style="background:#8B5CF6">SR</div>
#                     <div><div class="testi-name">Sara Raza</div><div class="testi-role">Senior Journalist · Daily Verify</div></div>
#                 </div>
#             </div>
#             <div class="testi-card">
#                 <div class="testi-stars">★★★★☆</div>
#                 <p class="testi-text">"The OTP screenshot tool saved a customer from a ₹50,000 scam. Simple to use, the phishing keyword highlighting is brilliant."</p>
#                 <div class="testi-author">
#                     <div class="testi-avatar" style="background:#10B981">ZM</div>
#                     <div><div class="testi-name">Zain Malik</div><div class="testi-role">CTO · CyberSafe Pakistan</div></div>
#                 </div>
#             </div>
#             <div class="testi-card">
#                 <div class="testi-stars">★★★★★</div>
#                 <p class="testi-text">"We integrated FraudX into our internal review workflow. The accuracy is exceptional and the speed is impressive. Highly recommended."</p>
#                 <div class="testi-author">
#                     <div class="testi-avatar" style="background:#F59E0B">NB</div>
#                     <div><div class="testi-name">Nadia Baig</div><div class="testi-role">Security Lead · BankLink</div></div>
#                 </div>
#             </div>
#             <div class="testi-card">
#                 <div class="testi-stars">★★★★★</div>
#                 <p class="testi-text">"Our compliance team uses this for transaction audits. The risk score with reasons is perfect for regulatory documentation purposes."</p>
#                 <div class="testi-author">
#                     <div class="testi-avatar" style="background:#EF4444">OM</div>
#                     <div><div class="testi-name">Omar Mirza</div><div class="testi-role">Compliance Officer · PakBank</div></div>
#                 </div>
#             </div>
#             <div class="testi-card">
#                 <div class="testi-stars">★★★★☆</div>
#                 <p class="testi-text">"The platform is clean, fast, and the AI explanations are easy to understand for non-technical stakeholders. A great product overall."</p>
#                 <div class="testi-author">
#                     <div class="testi-avatar" style="background:#06B6D4">HA</div>
#                     <div><div class="testi-name">Hira Ali</div><div class="testi-role">Product Manager · SecureNow</div></div>
#                 </div>
#             </div>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)


# # ═══════════════════════════════════════════════════════════════════════════════
# # PAGE — CONTACT
# # ═══════════════════════════════════════════════════════════════════════════════
# elif pg == "contact":
#     st.markdown("""
#     <div class="contact-grid">
#         <div>
#             <div class="section-label">Get In Touch</div>
#             <div class="section-title">Contact Us</div>
#             <p style="color:#64748B;font-size:0.9rem;line-height:1.8;margin:1rem 0 2rem;font-weight:300;">
#                 Have a question, partnership inquiry, or feedback? We'd love to hear from you. Reach out using the form or any of the channels below.
#             </p>
#             <div class="contact-info-item">
#                 <div class="ci-icon">📧</div>
#                 <div><div class="ci-label">Email</div><div class="ci-val">contact@fraudx.ai</div></div>
#             </div>
#             <div class="contact-info-item">
#                 <div class="ci-icon">📍</div>
#                 <div><div class="ci-label">Location</div><div class="ci-val">Lahore, Punjab, Pakistan</div></div>
#             </div>
#             <div class="contact-info-item">
#                 <div class="ci-icon">🐙</div>
#                 <div><div class="ci-label">GitHub</div><div class="ci-val">github.com/fraudx-ai</div></div>
#             </div>
#             <div class="contact-info-item">
#                 <div class="ci-icon">💼</div>
#                 <div><div class="ci-label">LinkedIn</div><div class="ci-val">linkedin.com/company/fraudx</div></div>
#             </div>
#         </div>
#         <div class="contact-form-wrap">
#     """, unsafe_allow_html=True)

#     with st.container():
#         st.markdown('<div style="padding:0">', unsafe_allow_html=True)
#         name_col, email_col = st.columns(2)
#         with name_col:
#             st.text_input("Full Name", placeholder="Your name")
#         with email_col:
#             st.text_input("Email Address", placeholder="you@email.com")
#         st.text_input("Subject", placeholder="What's this about?")
#         st.text_area("Message", placeholder="Tell us how we can help…", height=130)
#         if st.button("Send Message →", key="send_msg"):
#             st.success("✅ Message sent! We'll get back to you within 24 hours.")
#         st.markdown('</div>', unsafe_allow_html=True)

#     st.markdown("""
#         </div>
#     </div>
#     """, unsafe_allow_html=True)


# # ═══════════════════════════════════════════════════════════════════════════════
# # PAGE — FRAUD MODULE
# # ═══════════════════════════════════════════════════════════════════════════════
# elif pg == "fraud":
#     if st.button("← Back to Services", key="back_fraud"):
#         nav("services")

#     st.markdown("""
#     <div class="module-page">
#         <div class="module-header">
#             <div class="module-icon">💳</div>
#             <div>
#                 <div class="module-title">Credit Card Fraud Detection</div>
#                 <div class="module-tag">Random Forest Classifier · 30 PCA Features</div>
#             </div>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)

#     col_l, col_r = st.columns([1, 1], gap="large")
#     with col_l:
#         st.markdown('<div class="analysis-card"><div class="ac-label">Transaction Input</div>', unsafe_allow_html=True)
#         amount = st.number_input("Transaction Amount (PKR / USD)", min_value=0.0, step=500.0, format="%.2f")
#         run = st.button("⚡ Analyze Transaction")
#         st.markdown('</div>', unsafe_allow_html=True)

#     with col_r:
#         if run:
#             input_data = np.zeros((1, 30))
#             input_data[0][0] = amount
#             probs = fraud_model.predict_proba(input_data)[0]
#             fraud_prob = probs[1] * 100
#             sc = score_class(fraud_prob)
#             st.markdown(progress_color_css(fraud_prob), unsafe_allow_html=True)

#             st.markdown(f"""
#             <div class="analysis-card">
#                 <div class="ac-label">Risk Score</div>
#                 <div class="score-display">
#                     <span class="score-number {sc}">{fraud_prob:.1f}</span>
#                     <span class="score-unit">% fraud probability</span>
#                 </div>
#             """, unsafe_allow_html=True)
#             st.progress(int(fraud_prob))
#             st.markdown(verdict_html(fraud_prob, "fraud"), unsafe_allow_html=True)

#             reasons = []
#             if fraud_prob > 70: reasons.append("Pattern strongly deviates from normal behaviour")
#             if amount > 50000: reasons.append("High-value transaction detected")
#             if fraud_prob > 40: reasons.append("Anomaly detected in transaction feature space")
#             if reasons:
#                 st.markdown('<div class="ac-divider"><div class="ac-label">Analysis Signals</div>', unsafe_allow_html=True)
#                 chips = "".join(f'<span class="chip-signal"><span class="chip-dot"></span>{r}</span>' for r in reasons)
#                 st.markdown(f'<div class="chip-wrap">{chips}</div>', unsafe_allow_html=True)
#             st.markdown('</div>', unsafe_allow_html=True)
#         else:
#             st.markdown("""
#             <div class="placeholder-module">
#                 <div class="pm-icon">💳</div>
#                 <div class="pm-text">Enter amount and run analysis</div>
#             </div>
#             """, unsafe_allow_html=True)


# # ═══════════════════════════════════════════════════════════════════════════════
# # PAGE — FAKE NEWS MODULE
# # ═══════════════════════════════════════════════════════════════════════════════
# elif pg == "news":
#     if st.button("← Back to Services", key="back_news"):
#         nav("services")

#     st.markdown("""
#     <div class="module-page">
#         <div class="module-header">
#             <div class="module-icon">📰</div>
#             <div>
#                 <div class="module-title">Fake News Detection</div>
#                 <div class="module-tag">TF-IDF Vectorizer · Logistic Regression · 5K Features</div>
#             </div>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)

#     col_l, col_r = st.columns([1, 1], gap="large")
#     with col_l:
#         st.markdown('<div class="analysis-card"><div class="ac-label">Article Content</div>', unsafe_allow_html=True)
#         news_text = st.text_area("Paste news article or headline", placeholder="Enter the full article text or headline to analyze…", height=200)
#         run = st.button("🔍 Analyze Content")
#         st.markdown('</div>', unsafe_allow_html=True)

#     with col_r:
#         if run and news_text.strip():
#             vec = vectorizer.transform([news_text])
#             probs = fake_model.predict_proba(vec)[0]
#             fake_index = list(fake_model.classes_).index(0)
#             misinfo = probs[fake_index] * 100

#             trigger_words = ["shocking", "breaking", "secret", "exposed",
#                              "they don't want you to know", "miracle", "100% proof"]
#             found = [w for w in trigger_words if w in news_text.lower()]
#             sc = score_class(misinfo)
#             st.markdown(progress_color_css(misinfo), unsafe_allow_html=True)

#             st.markdown(f"""
#             <div class="analysis-card">
#                 <div class="ac-label">Misinformation Score</div>
#                 <div class="score-display">
#                     <span class="score-number {sc}">{misinfo:.1f}</span>
#                     <span class="score-unit">% misinformation probability</span>
#                 </div>
#             """, unsafe_allow_html=True)
#             st.progress(int(misinfo))
#             st.markdown(verdict_html(misinfo, "news"), unsafe_allow_html=True)

#             if found:
#                 st.markdown('<div class="ac-divider"><div class="ac-label">Manipulative Language</div>', unsafe_allow_html=True)
#                 chips = "".join(f'<span class="chip-warn">⚠ {t}</span>' for t in found)
#                 st.markdown(f'<div style="margin-top:4px">{chips}</div>', unsafe_allow_html=True)

#             explain = []
#             if misinfo > 60: explain.append("Structure resembles known misinformation patterns")
#             if found: explain.append("Emotionally manipulative wording detected")
#             if len(news_text.split()) < 80: explain.append("Very short articles are often unreliable")
#             if explain:
#                 st.markdown('<div class="ac-divider"><div class="ac-label">Analysis Signals</div>', unsafe_allow_html=True)
#                 chips = "".join(f'<span class="chip-signal"><span class="chip-dot"></span>{e}</span>' for e in explain)
#                 st.markdown(f'<div class="chip-wrap">{chips}</div>', unsafe_allow_html=True)
#             st.markdown('</div>', unsafe_allow_html=True)

#         elif run:
#             st.markdown('<div class="verdict-box vb-warning">⚠️&nbsp; Please enter some text to analyze.</div>', unsafe_allow_html=True)
#         else:
#             st.markdown("""
#             <div class="placeholder-module">
#                 <div class="pm-icon">📰</div>
#                 <div class="pm-text">Enter article text and run analysis</div>
#             </div>
#             """, unsafe_allow_html=True)


# # ═══════════════════════════════════════════════════════════════════════════════
# # PAGE — OTP MODULE
# # ═══════════════════════════════════════════════════════════════════════════════
# elif pg == "otp":
#     if st.button("← Back to Services", key="back_otp"):
#         nav("services")

#     st.markdown("""
#     <div class="module-page">
#         <div class="module-header">
#             <div class="module-icon">📲</div>
#             <div>
#                 <div class="module-title">OTP Phishing Detector</div>
#                 <div class="module-tag">Tesseract OCR · NLP Scam Classifier</div>
#             </div>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)

#     col_l, col_r = st.columns([1, 1], gap="large")
#     with col_l:
#         st.markdown('<div class="analysis-card"><div class="ac-label">Upload Screenshot</div>', unsafe_allow_html=True)
#         uploaded = st.file_uploader("Drag & drop or click to browse", type=["png", "jpg", "jpeg"])
#         if uploaded:
#             image = Image.open(uploaded)
#             st.image(image, caption="Uploaded Screenshot", use_container_width=True)
#         st.markdown('</div>', unsafe_allow_html=True)

#     with col_r:
#         if uploaded:
#             image = Image.open(uploaded)
#             extracted = pytesseract.image_to_string(image)
#             display_text = extracted.strip() or "No readable text detected."

#             st.markdown(f"""
#             <div class="analysis-card">
#                 <div class="ac-label">OCR — Extracted Text</div>
#                 <div class="ocr-display">{display_text}</div>
#             </div>
#             """, unsafe_allow_html=True)

#             red_flags = ["urgent", "click", "link", "verify", "share", "blocked",
#                          "suspend", "prize", "call now", "confirm", "account"]
#             found_flags = [w for w in red_flags if w in extracted.lower()]

#             vec = otp_vectorizer.transform([extracted])
#             probs = otp_model.predict_proba(vec)[0]
#             fake_index = list(otp_model.classes_).index("fake")
#             risk = probs[fake_index] * 100
#             sc = score_class(risk)
#             st.markdown(progress_color_css(risk), unsafe_allow_html=True)

#             st.markdown(f"""
#             <div class="analysis-card">
#                 <div class="ac-label">Fraud Risk Score</div>
#                 <div class="score-display">
#                     <span class="score-number {sc}">{risk:.1f}</span>
#                     <span class="score-unit">% scam probability</span>
#                 </div>
#             """, unsafe_allow_html=True)
#             st.progress(int(risk))
#             st.markdown(verdict_html(risk, "otp"), unsafe_allow_html=True)

#             if found_flags:
#                 st.markdown('<div class="ac-divider"><div class="ac-label">Phishing Keywords</div>', unsafe_allow_html=True)
#                 chips = "".join(f'<span class="chip-warn">⚠ {f}</span>' for f in found_flags)
#                 st.markdown(f'<div style="margin-top:4px">{chips}</div>', unsafe_allow_html=True)

#             explanations = []
#             if risk > 60: explanations.append("Message uses known manipulation patterns")
#             if found_flags: explanations.append("Contains phishing keywords")
#             if "otp" in extracted.lower(): explanations.append("Requests sensitive authentication code")
#             if explanations:
#                 st.markdown('<div class="ac-divider"><div class="ac-label">Analysis Signals</div>', unsafe_allow_html=True)
#                 chips = "".join(f'<span class="chip-signal"><span class="chip-dot"></span>{e}</span>' for e in explanations)
#                 st.markdown(f'<div class="chip-wrap">{chips}</div>', unsafe_allow_html=True)

#             st.markdown('<div class="ac-divider"><div class="ac-label">Feedback</div>', unsafe_allow_html=True)
#             fb = st.radio("Was this analysis accurate?", ["👍 Yes, helpful", "👎 No, incorrect"], label_visibility="collapsed")
#             if fb == "👍 Yes, helpful":
#                 st.markdown('<div class="verdict-box vb-success">✅&nbsp; Thank you — your feedback improves our model.</div>', unsafe_allow_html=True)
#             else:
#                 st.markdown('<div class="verdict-box vb-warning">📝&nbsp; Noted — we will use this to improve detection.</div>', unsafe_allow_html=True)
#             st.markdown('</div>', unsafe_allow_html=True)

#         else:
#             st.markdown("""
#             <div class="placeholder-module" style="min-height:300px">
#                 <div class="pm-icon">📲</div>
#                 <div class="pm-text">Upload a screenshot to begin</div>
#             </div>
#             """, unsafe_allow_html=True)


import pandas as pd
import numpy as np
import streamlit as st
import joblib
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FraudX — AI Security Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── SESSION STATE ───────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "home"

def nav(p):
    st.session_state.page = p
    st.rerun()

pg = st.session_state.page

# ─── LOAD MODELS ────────────────────────────────────────────────────────────────
@st.cache_resource
def load_models():
    try:
        fraud_model    = joblib.load("models/fraud_model.pkl")
        fake_model     = joblib.load("models/fake_model.pkl")
        vectorizer     = joblib.load("models/vectorizer.pkl")
        otp_model      = joblib.load("models/otp_model.pkl")
        otp_vectorizer = joblib.load("models/otp_vectorizer.pkl")
        return fraud_model, fake_model, vectorizer, otp_model, otp_vectorizer, True
    except Exception as e:
        return None, None, None, None, None, False

fraud_model, fake_model, vectorizer, otp_model, otp_vectorizer, models_ok = load_models()

# ─── GLOBAL CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    background: #F7F5F0 !important;
    color: #1A1A1A !important;
    font-family: 'DM Sans', sans-serif !important;
}

#MainMenu, footer, header { visibility: hidden; display: none; }
[data-testid="stSidebar"] { display: none; }

.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}
section.main > div { padding: 0 !important; }

/* ══ NAVBAR ══ */
.fx-navbar {
    position: sticky;
    top: 0;
    z-index: 1000;
    background: rgba(247, 245, 240, 0.95);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid #E5E0D5;
    padding: 0 5%;
    height: 68px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.fx-nav-brand {
    font-family: 'DM Serif Display', serif;
    font-size: 1.45rem;
    color: #1A1A1A;
    letter-spacing: -0.3px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.fx-nav-brand span { color: #2563EB; }
.fx-nav-links {
    display: flex;
    align-items: center;
    gap: 2.5rem;
}
.fx-nav-link {
    font-size: 0.88rem;
    font-weight: 500;
    color: #6B7280;
    cursor: pointer;
    text-decoration: none;
    transition: color 0.2s;
    border: none;
    background: none;
    font-family: 'DM Sans', sans-serif;
}
.fx-nav-link:hover, .fx-nav-link.active { color: #1A1A1A; }
.fx-nav-cta {
    background: #1A1A1A;
    color: #FFFFFF !important;
    padding: 9px 22px;
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.84rem;
    letter-spacing: 0.1px;
    cursor: pointer;
    border: none;
    transition: all 0.2s;
}
.fx-nav-cta:hover { background: #2563EB; }

/* ── Streamlit button overrides for nav row ── */
div[data-testid="stHorizontalBlock"] .stButton > button {
    background: transparent !important;
    color: #6B7280 !important;
    border: none !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
    padding: 6px 4px !important;
    box-shadow: none !important;
    width: auto !important;
    letter-spacing: 0 !important;
    transition: color 0.2s !important;
}
div[data-testid="stHorizontalBlock"] .stButton > button:hover {
    color: #1A1A1A !important;
    background: transparent !important;
    transform: none !important;
    box-shadow: none !important;
}

/* Override the last nav button (CTA) */
.nav-cta-col .stButton > button {
    background: #1A1A1A !important;
    color: #FFFFFF !important;
    border-radius: 8px !important;
    padding: 9px 18px !important;
    font-weight: 600 !important;
    font-size: 0.84rem !important;
}
.nav-cta-col .stButton > button:hover {
    background: #2563EB !important;
    color: #fff !important;
    transform: none !important;
}

/* ══ HERO ══ */
.fx-hero {
    min-height: 88vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 5rem 10% 4rem;
    background: #F7F5F0;
    position: relative;
    overflow: hidden;
}
.fx-hero::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background:
        radial-gradient(ellipse 800px 500px at 60% 20%, rgba(37,99,235,0.06) 0%, transparent 60%),
        radial-gradient(ellipse 600px 400px at 20% 70%, rgba(16,185,129,0.04) 0%, transparent 60%);
    pointer-events: none;
}
.fx-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: #FFFFFF;
    border: 1px solid #E5E0D5;
    border-radius: 100px;
    padding: 7px 18px;
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    color: #2563EB;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 2rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    animation: fadeUp 0.6s ease both;
}
.fx-badge-dot {
    width: 6px; height: 6px;
    background: #10B981;
    border-radius: 50%;
    box-shadow: 0 0 0 3px rgba(16,185,129,0.2);
    animation: pulse3 2s infinite;
}
@keyframes pulse3 {
    0%,100%{ box-shadow: 0 0 0 3px rgba(16,185,129,0.2); }
    50%{ box-shadow: 0 0 0 7px rgba(16,185,129,0); }
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}
.fx-hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: clamp(3rem, 6vw, 5.5rem);
    line-height: 1.05;
    letter-spacing: -2px;
    color: #111111;
    margin-bottom: 1.5rem;
    animation: fadeUp 0.7s 0.1s ease both;
}
.fx-hero-title em {
    font-style: italic;
    color: #2563EB;
}
.fx-hero-sub {
    font-size: 1.1rem;
    color: #6B7280;
    max-width: 560px;
    line-height: 1.75;
    margin-bottom: 2.75rem;
    font-weight: 400;
    animation: fadeUp 0.7s 0.2s ease both;
}
.fx-hero-btns {
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
    animation: fadeUp 0.7s 0.3s ease both;
}

/* ══ STATS ══ */
.fx-stats {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0;
    background: #FFFFFF;
    border-top: 1px solid #E5E0D5;
    border-bottom: 1px solid #E5E0D5;
}
.fx-stat {
    padding: 2.25rem 2rem;
    text-align: center;
    border-right: 1px solid #E5E0D5;
    transition: background 0.2s;
}
.fx-stat:last-child { border-right: none; }
.fx-stat:hover { background: #F7F5F0; }
.fx-stat-num {
    font-family: 'DM Serif Display', serif;
    font-size: 2.4rem;
    color: #111111;
    line-height: 1;
    letter-spacing: -1px;
}
.fx-stat-num span { color: #2563EB; }
.fx-stat-label {
    font-size: 0.78rem;
    color: #9CA3AF;
    margin-top: 5px;
    font-weight: 400;
    letter-spacing: 0.2px;
}

/* ══ SECTION ══ */
.fx-section { padding: 6rem 8%; }
.fx-section-alt {
    background: #FFFFFF;
    border-top: 1px solid #E5E0D5;
    border-bottom: 1px solid #E5E0D5;
    padding: 6rem 8%;
}
.fx-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #2563EB;
    margin-bottom: 0.6rem;
}
.fx-section-title {
    font-family: 'DM Serif Display', serif;
    font-size: clamp(1.8rem, 3vw, 2.6rem);
    color: #111111;
    letter-spacing: -0.5px;
    line-height: 1.2;
    margin-bottom: 0.85rem;
}
.fx-section-sub {
    font-size: 0.95rem;
    color: #6B7280;
    line-height: 1.75;
    max-width: 520px;
    font-weight: 400;
}

/* ══ CARDS ══ */
.fx-cards {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.25rem;
    margin-top: 3rem;
}
.fx-card {
    background: #FFFFFF;
    border: 1px solid #E5E0D5;
    border-radius: 16px;
    padding: 2rem;
    transition: all 0.25s;
    position: relative;
    overflow: hidden;
}
.fx-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #2563EB, #7C3AED);
    opacity: 0;
    transition: opacity 0.25s;
}
.fx-card:hover {
    border-color: #CBD5E1;
    box-shadow: 0 12px 40px rgba(0,0,0,0.08);
    transform: translateY(-3px);
}
.fx-card:hover::after { opacity: 1; }
.fx-card-icon {
    width: 48px; height: 48px;
    background: #EFF6FF;
    border: 1px solid #BFDBFE;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
    margin-bottom: 1.25rem;
}
.fx-card-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.2rem;
    color: #111111;
    margin-bottom: 0.6rem;
    letter-spacing: -0.2px;
}
.fx-card-desc {
    font-size: 0.85rem;
    color: #6B7280;
    line-height: 1.65;
    margin-bottom: 1.25rem;
    font-weight: 400;
}
.fx-card-tag {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    color: #2563EB;
    letter-spacing: 1px;
    text-transform: uppercase;
}

/* ══ HOW IT WORKS ══ */
.fx-steps {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1.5rem;
    margin-top: 3rem;
    position: relative;
}
.fx-steps::before {
    content: '';
    position: absolute;
    top: 28px; left: 10%; right: 10%;
    height: 1px;
    background: linear-gradient(90deg, transparent, #E5E0D5 20%, #E5E0D5 80%, transparent);
    z-index: 0;
}
.fx-step {
    text-align: center;
    padding: 1.5rem 1rem;
    position: relative;
    z-index: 1;
}
.fx-step-num {
    width: 56px; height: 56px;
    background: #FFFFFF;
    border: 2px solid #E5E0D5;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'DM Serif Display', serif;
    font-size: 1.3rem;
    color: #2563EB;
    margin: 0 auto 1rem;
    transition: all 0.2s;
}
.fx-step:hover .fx-step-num {
    background: #2563EB;
    color: #FFFFFF;
    border-color: #2563EB;
    box-shadow: 0 8px 20px rgba(37,99,235,0.25);
}
.fx-step-title {
    font-size: 0.95rem;
    font-weight: 600;
    color: #1A1A1A;
    margin-bottom: 0.4rem;
}
.fx-step-desc { font-size: 0.8rem; color: #6B7280; line-height: 1.55; }

/* ══ TESTIMONIALS ══ */
.fx-testimonials {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.25rem;
    margin-top: 3rem;
}
.fx-testi {
    background: #FFFFFF;
    border: 1px solid #E5E0D5;
    border-radius: 16px;
    padding: 1.75rem;
    transition: all 0.2s;
}
.fx-testi:hover {
    border-color: #BFDBFE;
    box-shadow: 0 8px 24px rgba(37,99,235,0.07);
}
.fx-testi-stars { color: #F59E0B; font-size: 0.85rem; margin-bottom: 1rem; letter-spacing: 2px; }
.fx-testi-text {
    font-size: 0.88rem;
    color: #4B5563;
    line-height: 1.7;
    margin-bottom: 1.25rem;
    font-style: italic;
    font-weight: 400;
}
.fx-testi-author { display: flex; align-items: center; gap: 10px; }
.fx-testi-avatar {
    width: 38px; height: 38px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 0.78rem;
    color: #FFFFFF;
    flex-shrink: 0;
}
.fx-testi-name { font-size: 0.85rem; font-weight: 600; color: #1A1A1A; }
.fx-testi-role { font-size: 0.72rem; color: #9CA3AF; margin-top: 1px; font-family: 'DM Mono', monospace; }

/* ══ ABOUT ══ */
.fx-about-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 5rem;
    align-items: center;
    padding: 6rem 8%;
    background: #F7F5F0;
}
.fx-about-visual {
    background: #FFFFFF;
    border: 1px solid #E5E0D5;
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 4px 24px rgba(0,0,0,0.05);
}
.fx-av-header {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    color: #2563EB;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 1.25rem;
    display: flex;
    align-items: center;
    gap: 8px;
}
.fx-av-dot { width:6px; height:6px; background:#10B981; border-radius:50%; animation: pulse3 2s infinite; }
.fx-av-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.8rem 1rem;
    background: #F7F5F0;
    border: 1px solid #E5E0D5;
    border-radius: 10px;
    margin-bottom: 0.5rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    color: #6B7280;
    transition: border-color 0.2s;
}
.fx-av-row:hover { border-color: #BFDBFE; }
.fx-av-val { color: #1A1A1A; font-weight: 500; }
.fx-badge-chip {
    font-size: 0.62rem;
    padding: 3px 10px;
    border-radius: 100px;
    font-weight: 600;
    font-family: 'DM Sans', sans-serif;
}
.chip-green { background: #D1FAE5; color: #065F46; }
.chip-red   { background: #FEE2E2; color: #991B1B; }
.chip-amber { background: #FEF3C7; color: #92400E; }

.fx-tech-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-top: 2.5rem;
}
.fx-tech-card {
    background: #F7F5F0;
    border: 1px solid #E5E0D5;
    border-radius: 14px;
    padding: 1.5rem;
    text-align: center;
    transition: all 0.2s;
}
.fx-tech-card:hover {
    background: #FFFFFF;
    border-color: #BFDBFE;
    box-shadow: 0 4px 16px rgba(37,99,235,0.07);
}
.fx-tech-icon { font-size: 1.8rem; margin-bottom: 0.5rem; }
.fx-tech-name { font-weight: 600; color: #1A1A1A; font-size: 0.88rem; margin-bottom: 4px; }
.fx-tech-desc { font-size: 0.75rem; color: #6B7280; line-height: 1.5; }

/* ══ CONTACT ══ */

.fx-contact-grid {
    display: grid;
    grid-template-columns: 1fr 1.5fr;
    gap: 4rem;
    align-items: start;
    padding: 6rem 8%;
    background: #F7F5F0;
}
.fx-contact-item {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.75rem;
    align-items: flex-start;
}
.fx-ci-icon {
    width: 42px; height: 42px;
    background: #EFF6FF;
    border: 1px solid #BFDBFE;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
    flex-shrink: 0;
}
.fx-ci-label { font-size: 0.7rem; color: #9CA3AF; font-family: 'DM Mono', monospace; letter-spacing: 1px; text-transform: uppercase; }
.fx-ci-val { font-size: 0.9rem; color: #1A1A1A; font-weight: 500; margin-top: 2px; }
.fx-form-wrap {
    background: #FFFFFF;
    border: 1px solid #E5E0D5;
    border-radius: 20px;
    padding: 2.25rem;
    box-shadow: 0 4px 24px rgba(0,0,0,0.05);
}
.fx-contact-section {
    margin-top: 3rem;   /* pushes the whole contact section down */
}
/* ══ MODULE PAGES ══ */
.fx-module-wrap { padding: 2.5rem 8%; min-height: 100vh; background: #F7F5F0; }
.fx-module-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 2.5rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid #E5E0D5;
}
.fx-module-icon {
    width: 52px; height: 52px;
    background: #EFF6FF;
    border: 1px solid #BFDBFE;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
}
.fx-module-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.9rem;
    color: #111111;
    letter-spacing: -0.5px;
    line-height: 1.1;
}
.fx-module-tag {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    color: #2563EB;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-top: 3px;
}

/* ══ ANALYSIS CARDS ══ */
.fx-acard {
    background: #FFFFFF;
    border: 1px solid #E5E0D5;
    border-radius: 16px;
    padding: 1.75rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.fx-acard-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #9CA3AF;
    margin-bottom: 1rem;
}
.fx-score-display { display: flex; align-items: baseline; gap: 8px; margin-bottom: 10px; }
.fx-score-num {
    font-family: 'DM Serif Display', serif;
    font-size: 3.5rem;
    letter-spacing: -3px;
    line-height: 1;
}
.fx-score-unit { font-family: 'DM Mono', monospace; font-size: 0.78rem; color: #9CA3AF; }
.score-red   { color: #DC2626; }
.score-amber { color: #D97706; }
.score-green { color: #059669; }

.fx-verdict {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 0.9rem 1.1rem;
    border-radius: 10px;
    font-size: 0.88rem;
    font-weight: 500;
    margin: 0.85rem 0;
}
.vb-danger  { background: #FEF2F2; border: 1px solid #FECACA; color: #991B1B; }
.vb-warning { background: #FFFBEB; border: 1px solid #FDE68A; color: #92400E; }
.vb-success { background: #ECFDF5; border: 1px solid #A7F3D0; color: #065F46; }

.fx-divider { border: none; border-top: 1px solid #F3F4F6; margin: 1rem 0; }
.fx-chip-wrap { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 8px; }
.fx-chip {
    display: inline-flex; align-items: center; gap: 6px;
    background: #F1F5F9;
    border: 1px solid #E2E8F0;
    border-radius: 8px; padding: 5px 10px;
    font-size: 0.75rem; color: #475569;
    font-family: 'DM Sans', sans-serif;
}
.fx-chip-dot { width:5px; height:5px; border-radius:50%; background:#2563EB; flex-shrink:0; }
.fx-chip-warn {
    background: #FFFBEB;
    border: 1px solid #FDE68A;
    border-radius: 6px; padding: 3px 10px;
    font-size: 0.7rem; color: #92400E;
    font-family: 'DM Mono', monospace;
    display: inline-block; margin: 2px;
}
.fx-ocr {
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 10px; padding: 1rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem; color: #475569;
    line-height: 1.8; max-height: 150px;
    overflow-y: auto; white-space: pre-wrap;
}
.fx-placeholder {
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    min-height: 240px;
    background: #FFFFFF;
    border: 2px dashed #E5E0D5;
    border-radius: 16px; gap: 10px;
}
.fx-ph-icon { font-size: 2.5rem; opacity: 0.25; }
.fx-ph-text {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem; letter-spacing: 2px;
    text-transform: uppercase; color: #CBD5E1;
}

/* ══ GLOBAL BUTTON STYLES ══ */
.stButton > button {
    background: #1A1A1A !important;
    color: #FFFFFF !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.7rem 1.5rem !important;
    width: 100% !important;
    transition: all 0.2s !important;
    letter-spacing: 0.2px !important;
}
.stButton > button:hover {
    background: #2563EB !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 24px rgba(37,99,235,0.25) !important;
}

/* ══ INPUTS ══ */
[data-testid="stTextInput"] label,
[data-testid="stTextArea"] label,
[data-testid="stNumberInput"] label,
[data-testid="stSelectbox"] label,
[data-testid="stFileUploader"] label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.62rem !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    color: #6B7280 !important;
    font-weight: 500 !important;
}
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input {
    background: #FFFFFF !important;
    border: 1px solid #D1D5DB !important;
    border-radius: 10px !important;
    color: #1A1A1A !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus {
    border-color: #2563EB !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.1) !important;
}
[data-testid="stTextArea"] textarea {
    background: #FFFFFF !important;
    border: 1px solid #D1D5DB !important;
    border-radius: 10px !important;
    color: #1A1A1A !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    line-height: 1.6 !important;
}
[data-testid="stTextArea"] textarea:focus {
    border-color: #2563EB !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.1) !important;
}
[data-testid="stTextArea"] textarea::placeholder,
[data-testid="stTextInput"] input::placeholder { color: #D1D5DB !important; }

/* ══ PROGRESS ══ */
[data-testid="stProgress"] > div > div {
    background: #F3F4F6 !important;
    border-radius: 100px !important;
    height: 8px !important;
}
[data-testid="stProgress"] > div > div > div > div {
    border-radius: 100px !important;
    height: 8px !important;
}

/* ══ FILE UPLOADER ══ */
[data-testid="stFileUploader"] section {
    background: #FAFAFA !important;
    border: 2px dashed #D1D5DB !important;
    border-radius: 12px !important;
}
[data-testid="stFileUploader"] section:hover {
    border-color: #2563EB !important;
    background: #EFF6FF !important;
}

/* ══ RADIO ══ */
[data-testid="stRadio"] > label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.6rem !important; letter-spacing: 2px !important;
    text-transform: uppercase !important; color: #6B7280 !important;
}
[data-testid="stRadio"] div[role="radiogroup"] > label {
    font-size: 0.85rem !important; color: #4B5563 !important;
    text-transform: none !important; letter-spacing: 0 !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ══ FOOTER ══ */
.fx-footer {
    background: #1A1A1A;
    color: #9CA3AF;
    padding: 3rem 8%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 1rem;
}
.fx-footer-brand {
    font-family: 'DM Serif Display', serif;
    font-size: 1.2rem;
    color: #FFFFFF;
}
.fx-footer-brand span { color: #2563EB; }
.fx-footer-copy { font-size: 0.75rem; color: #4B5563; margin-top: 3px; }
.fx-footer-links { display: flex; gap: 1.5rem; flex-wrap: wrap; }
.fx-footer-link {
    font-size: 0.82rem; color: #4B5563;
    cursor: pointer; transition: color 0.2s;
}
.fx-footer-link:hover { color: #9CA3AF; }

/* ══ BACK BUTTON ══ */
.back-btn-wrap .stButton > button {
    background: #FFFFFF !important;
    color: #4B5563 !important;
    border: 1px solid #E5E0D5 !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    width: auto !important;
    padding: 8px 18px !important;
    border-radius: 8px !important;
}
.back-btn-wrap .stButton > button:hover {
    background: #F1F5F9 !important;
    color: #1A1A1A !important;
    box-shadow: none !important;
    transform: none !important;
}
/* Disable access key underlines */
a, button, span {
    text-decoration: none !important;
}

/* For Windows browsers that force accesskey underline */
* {
    -webkit-text-decoration-skip: objects !important;
    text-decoration-skip-ink: none !important;
}

/* ══ SUCCESS / INFO ══ */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ══ SCROLLBAR ══ */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #F7F5F0; }
::-webkit-scrollbar-thumb { background: #D1D5DB; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #9CA3AF; }
</style>
""", unsafe_allow_html=True)


# ─── HELPERS ────────────────────────────────────────────────────────────────────
def score_class(p):
    if p > 70: return "score-red"
    if p > 40: return "score-amber"
    return "score-green"

def progress_color_css(p):
    c = "#DC2626" if p > 70 else ("#D97706" if p > 40 else "#059669")
    return f"""
    <style>
    [data-testid="stProgress"] > div > div > div > div {{
        background: {c} !important;
    }}
    </style>"""

VERDICTS = {
    "fraud": {
        "high": ("🚨", "High Fraud Risk — Do not proceed with this transaction."),
        "med":  ("⚠️", "Suspicious Activity — Manual review is recommended."),
        "low":  ("✅", "Transaction Appears Normal."),
    },
    "news": {
        "high": ("🚨", "Likely Misinformation — Verify before sharing."),
        "med":  ("⚠️", "Needs Verification — Cross-check with other sources."),
        "low":  ("✅", "Content Appears Credible."),
    },
    "otp": {
        "high": ("🚨", "High Risk — This is very likely a phishing scam."),
        "med":  ("⚠️", "Medium Risk — Treat with caution. Do not share OTPs."),
        "low":  ("✅", "Low Risk — Message appears legitimate."),
    },
}

def verdict_html(p, mode):
    tier = "high" if p > 70 else ("med" if p > 40 else "low")
    cls = "vb-danger" if tier == "high" else ("vb-warning" if tier == "med" else "vb-success")
    icon, text = VERDICTS[mode][tier]
    return f'<div class="fx-verdict {cls}">{icon}&nbsp;&nbsp;{text}</div>'


# ═══════════════════════════════════════════════════════════════════════════════
# NAVBAR (fully functional)
# ═══════════════════════════════════════════════════════════════════════════════
# ─── NAVBAR (styled + functional, same tab navigation) ──────────────────────────
nav_html = f"""
<div class="fx-navbar">
  <div class="fx-nav-brand">🛡️ Fraud<span>X</span></div>
  <div class="fx-nav-links">
    <a href="?page=home" class="fx-nav-link {'active' if st.session_state.page=='home' else ''}" target="_self">Home</a>
    <a href="?page=about" class="fx-nav-link {'active' if st.session_state.page=='about' else ''}" target="_self">About</a>
    <a href="?page=services" class="fx-nav-link {'active' if st.session_state.page=='services' else ''}" target="_self">Services</a>
    <a href="?page=reviews" class="fx-nav-link {'active' if st.session_state.page=='reviews' else ''}" target="_self">Reviews</a>
    <a href="?page=contact" class="fx-nav-link {'active' if st.session_state.page=='contact' else ''}" target="_self">Contact</a>
    <a href="?page=services" class="fx-nav-cta" target="_self">⚡ Launch App</a>
  </div>
</div>
"""

st.markdown(nav_html, unsafe_allow_html=True)

# ─── Functional logic ───────────────────────────────────────────────────────────
query_params = st.query_params
if "page" in query_params:
    st.session_state.page = query_params["page"]

pg = st.session_state.page


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE — HOME
# ═══════════════════════════════════════════════════════════════════════════════
if pg == "home":

    # Hero
    st.markdown("""
    <div class="fx-hero">
        <div class="fx-badge">
            <span class="fx-badge-dot"></span>
            AI-Powered Security Intelligence
        </div>
        <h1 class="fx-hero-title">Detect Fraud.<br><em>Before It Happens.</em></h1>
        <p class="fx-hero-sub">
            FraudX uses state-of-the-art machine learning to protect your transactions,
            verify news authenticity, and detect phishing scams in real time.
        </p>
    </div>
    """, unsafe_allow_html=True)


    # Stats
    st.markdown("""
    <div class="fx-stats">
        <div class="fx-stat">
            <div class="fx-stat-num">99<span>.2%</span></div>
            <div class="fx-stat-label">Fraud Detection Accuracy</div>
        </div>
        <div class="fx-stat">
            <div class="fx-stat-num">3<span>M+</span></div>
            <div class="fx-stat-label">Transactions Analyzed</div>
        </div>
        <div class="fx-stat">
            <div class="fx-stat-num">0.3<span>s</span></div>
            <div class="fx-stat-label">Average Response Time</div>
        </div>
        <div class="fx-stat">
            <div class="fx-stat-num">3</div>
            <div class="fx-stat-label">AI Security Modules</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Services
    st.markdown(f"""
    <div class="fx-section">
        <div class="fx-eyebrow">Our Services</div>
        <div class="fx-section-title">Choose a Security Module</div>
        <p class="fx-section-sub">Each module is an independent AI system. Select one below to run a live analysis.</p>
        <div class="fx-cards">
            <a href="?page=fraud" target="_self" class="fx-card">
                <div class="fx-card-icon">💳</div>
                <div class="fx-card-title">Fraud Detection</div>
                <p class="fx-card-desc">Analyze credit card transactions in real time. Enter an amount and get an instant fraud risk score backed by a Random Forest model.</p>
                <div class="fx-card-tag">Random Forest · 99.2% Accuracy</div>
            </a>
            <a href="?page=news" target="_self" class="fx-card">
                <div class="fx-card-icon">📰</div>
                <div class="fx-card-title">Fake News Detection</div>
                <p class="fx-card-desc">Paste any article or headline and receive a misinformation probability score with language pattern analysis.</p>
                <div class="fx-card-tag">TF-IDF · Logistic Regression</div>
            </a>
            <a href="?page=otp" target="_self" class="fx-card">
                <div class="fx-card-icon">📲</div>
                <div class="fx-card-title">OTP Phishing Detector</div>
                <p class="fx-card-desc">Upload a screenshot of a suspicious OTP message. Our OCR + NLP pipeline extracts text and classifies the scam risk instantly.</p>
                <div class="fx-card-tag">Tesseract OCR · NLP Model</div>
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Sync query params with session_state
    query_params = st.query_params
    if "page" in query_params:
        st.session_state.page = query_params["page"]

    pg = st.session_state.page

    # How it works
    st.markdown("""
    <div class="fx-section-alt" style="text-align:center">
        <div class="fx-eyebrow" style="text-align:center">How It Works</div>
        <div class="fx-section-title" style="text-align:center">Simple. Fast. Accurate.</div>
        <div class="fx-steps">
            <div class="fx-step">
                <div class="fx-step-num">01</div>
                <div class="fx-step-title">Input Data</div>
                <p class="fx-step-desc">Enter transaction details, paste an article, or upload a screenshot.</p>
            </div>
            <div class="fx-step">
                <div class="fx-step-num">02</div>
                <div class="fx-step-title">AI Processing</div>
                <p class="fx-step-desc">Our ML models analyze your input against millions of learned patterns.</p>
            </div>
            <div class="fx-step">
                <div class="fx-step-num">03</div>
                <div class="fx-step-title">Risk Scoring</div>
                <p class="fx-step-desc">Receive a precise probability score with detailed signal explanations.</p>
            </div>
            <div class="fx-step">
                <div class="fx-step-num">04</div>
                <div class="fx-step-title">Take Action</div>
                <p class="fx-step-desc">Act on clear verdicts: safe, suspicious, or high risk.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Testimonials
    st.markdown("""
    <div class="fx-section">
        <div class="fx-eyebrow">Testimonials</div>
        <div class="fx-section-title">Trusted by Professionals</div>
        <div class="fx-testimonials">
            <div class="fx-testi">
                <div class="fx-testi-stars">★★★★★</div>
                <p class="fx-testi-text">"FraudX flagged a suspicious transaction that our traditional system missed. The 0.3-second response time is incredible for a system this accurate."</p>
                <div class="fx-testi-author">
                    <div class="fx-testi-avatar" style="background:#2563EB">AK</div>
                    <div><div class="fx-testi-name">Ahmed Khan</div><div class="fx-testi-role">Risk Analyst · FinTech</div></div>
                </div>
            </div>
            <div class="fx-testi">
                <div class="fx-testi-stars">★★★★★</div>
                <p class="fx-testi-text">"The fake news module is remarkably accurate. It caught misinformation patterns in an article that appeared legitimate on the surface."</p>
                <div class="fx-testi-author">
                    <div class="fx-testi-avatar" style="background:#7C3AED">SR</div>
                    <div><div class="fx-testi-name">Sara Raza</div><div class="fx-testi-role">Journalist · Media Verification</div></div>
                </div>
            </div>
            <div class="fx-testi">
                <div class="fx-testi-stars">★★★★☆</div>
                <p class="fx-testi-text">"The OTP screenshot detector saved one of our customers from a phishing scam. Simple upload, instant verdict. The UI is clean and the logic is solid."</p>
                <div class="fx-testi-author">
                    <div class="fx-testi-avatar" style="background:#059669">ZM</div>
                    <div><div class="fx-testi-name">Zain Malik</div><div class="fx-testi-role">CTO · Cybersecurity Startup</div></div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div class="fx-footer">
        <div>
            <div class="fx-footer-brand">🛡️ Fraud<span>X</span></div>
            <div class="fx-footer-copy">© 2025 FraudX. AI-Powered Security Platform.</div>
        </div>
        <div class="fx-footer-links">
            <span class="fx-footer-link">Privacy Policy</span>
            <span class="fx-footer-link">Terms of Service</span>
            <span class="fx-footer-link">Documentation</span>
            <span class="fx-footer-link">GitHub</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE — ABOUT
# ═══════════════════════════════════════════════════════════════════════════════
elif pg == "about":
    st.markdown("""
    <div class="fx-about-grid">
        <div>
            <div class="fx-eyebrow">About FraudX</div>
            <div class="fx-section-title">Built to Stop Fraud<br>Before It Costs You</div>
            <p style="color:#6B7280;font-size:0.95rem;line-height:1.8;margin:1.25rem 0;font-weight:400;">
                FraudX is an AI-powered security intelligence platform combining three cutting-edge machine learning models into a single, unified interface. Built for analysts, journalists, and security professionals who need fast, reliable, explainable AI decisions.
            </p>
            <p style="color:#6B7280;font-size:0.95rem;line-height:1.8;margin-bottom:1.75rem;font-weight:400;">
                Our models are trained on industry-standard datasets — the Kaggle Credit Card Fraud dataset, ISOT Fake News dataset, and a custom OTP phishing corpus — delivering production-grade accuracy you can trust.
            </p>
            <div style="display:flex;gap:2.5rem;flex-wrap:wrap;margin-top:1.25rem;padding-top:1.25rem;border-top:1px solid #E5E0D5;">
                <div>
                    <div style="font-family:'DM Serif Display',serif;font-size:2rem;color:#2563EB">284K+</div>
                    <div style="font-size:0.78rem;color:#9CA3AF;margin-top:2px">Training Samples</div>
                </div>
                <div>
                    <div style="font-family:'DM Serif Display',serif;font-size:2rem;color:#2563EB">3</div>
                    <div style="font-size:0.78rem;color:#9CA3AF;margin-top:2px">AI Models</div>
                </div>
                <div>
                    <div style="font-family:'DM Serif Display',serif;font-size:2rem;color:#2563EB">99.2%</div>
                    <div style="font-size:0.78rem;color:#9CA3AF;margin-top:2px">Fraud Accuracy</div>
                </div>
            </div>
        </div>
        <div class="fx-about-visual">
            <div class="fx-av-header"><span class="fx-av-dot"></span> Live Model Output</div>
            <div class="fx-av-row">
                <span>Transaction #TXN-0042</span>
                <span class="fx-av-val">$87,500</span>
                <span class="fx-badge-chip chip-red">HIGH RISK</span>
            </div>
            <div class="fx-av-row">
                <span>Transaction #TXN-0043</span>
                <span class="fx-av-val">$1,200</span>
                <span class="fx-badge-chip chip-green">SAFE</span>
            </div>
            <div class="fx-av-row">
                <span>Article: "SHOCKING: Secret..."</span>
                <span class="fx-av-val">91.4%</span>
                <span class="fx-badge-chip chip-red">FAKE</span>
            </div>
            <div class="fx-av-row">
                <span>Article: "Fed raises rates by..."</span>
                <span class="fx-av-val">8.2%</span>
                <span class="fx-badge-chip chip-green">CREDIBLE</span>
            </div>
            <div class="fx-av-row">
                <span>OTP Screenshot #48</span>
                <span class="fx-av-val">78.3%</span>
                <span class="fx-badge-chip chip-amber">SUSPICIOUS</span>
            </div>
            <div class="fx-av-row">
                <span>OTP Screenshot #49</span>
                <span class="fx-av-val">4.1%</span>
                <span class="fx-badge-chip chip-green">LEGIT</span>
            </div>
        </div>
    </div>

    <div class="fx-section-alt">
        <div style="text-align:center">
            <div class="fx-eyebrow" style="text-align:center">Tech Stack</div>
            <div class="fx-section-title" style="text-align:center">Powered by Proven Technology</div>
        </div>
        <div class="fx-tech-grid">
            <div class="fx-tech-card">
                <div class="fx-tech-icon">🌲</div>
                <div class="fx-tech-name">Random Forest</div>
                <div class="fx-tech-desc">Fraud classification with 100 estimators on PCA-transformed transaction data</div>
            </div>
            <div class="fx-tech-card">
                <div class="fx-tech-icon">📊</div>
                <div class="fx-tech-name">TF-IDF + LR</div>
                <div class="fx-tech-desc">5,000 feature text vectorization with logistic regression for news analysis</div>
            </div>
            <div class="fx-tech-card">
                <div class="fx-tech-icon">👁️</div>
                <div class="fx-tech-name">Tesseract OCR</div>
                <div class="fx-tech-desc">Image-to-text extraction from screenshots with preprocessing pipeline</div>
            </div>
            <div class="fx-tech-card">
                <div class="fx-tech-icon">⚡</div>
                <div class="fx-tech-name">Streamlit</div>
                <div class="fx-tech-desc">Python-native web framework with real-time inference and model caching</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE — SERVICES
# ═══════════════════════════════════════════════════════════════════════════════
elif pg == "services":
    st.markdown(f"""
    <div class="fx-section">
        <div class="fx-eyebrow">Our Services</div>
        <div class="fx-section-title">Choose a Security Module</div>
        <p class="fx-section-sub">Each module is an independent AI system. Select one below to run a live analysis.</p>
        <div class="fx-cards">
            <a href="?page=fraud" target="_self" class="fx-card">
                <div class="fx-card-icon">💳</div>
                <div class="fx-card-title">Fraud Detection</div>
                <p class="fx-card-desc">Analyze credit card transactions in real time. Enter an amount and get an instant fraud risk score backed by a Random Forest model.</p>
                <div class="fx-card-tag">Random Forest · 99.2% Accuracy</div>
            </a>
            <a href="?page=news" target="_self" class="fx-card">
                <div class="fx-card-icon">📰</div>
                <div class="fx-card-title">Fake News Detection</div>
                <p class="fx-card-desc">Paste any article or headline and receive a misinformation probability score with language pattern analysis.</p>
                <div class="fx-card-tag">TF-IDF · Logistic Regression</div>
            </a>
            <a href="?page=otp" target="_self" class="fx-card">
                <div class="fx-card-icon">📲</div>
                <div class="fx-card-title">OTP Phishing Detector</div>
                <p class="fx-card-desc">Upload a screenshot of a suspicious OTP message. Our OCR + NLP pipeline extracts text and classifies the scam risk instantly.</p>
                <div class="fx-card-tag">Tesseract OCR · NLP Model</div>
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Sync query params with session_state
    query_params = st.query_params
    if "page" in query_params:
        st.session_state.page = query_params["page"]

    pg = st.session_state.page


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE — REVIEWS
# ═══════════════════════════════════════════════════════════════════════════════
elif pg == "reviews":
    st.markdown("""
    <div class="fx-section">
        <div class="fx-eyebrow">Reviews & Testimonials</div>
        <div class="fx-section-title">What Our Users Say</div>
        <div class="fx-testimonials">
            <div class="fx-testi">
                <div class="fx-testi-stars">★★★★★</div>
                <p class="fx-testi-text">"FraudX flagged a suspicious high-value transaction our legacy system marked as safe. The model explanations are clear and actionable."</p>
                <div class="fx-testi-author">
                    <div class="fx-testi-avatar" style="background:#2563EB">AK</div>
                    <div><div class="fx-testi-name">Ahmed Khan</div><div class="fx-testi-role">Risk Analyst · FinTech Corp</div></div>
                </div>
            </div>
            <div class="fx-testi">
                <div class="fx-testi-stars">★★★★★</div>
                <p class="fx-testi-text">"As a journalist, I use the Fake News module daily. It catches subtle manipulation patterns that aren't obvious. An essential fact-checking tool."</p>
                <div class="fx-testi-author">
                    <div class="fx-testi-avatar" style="background:#7C3AED">SR</div>
                    <div><div class="fx-testi-name">Sara Raza</div><div class="fx-testi-role">Senior Journalist · Daily Verify</div></div>
                </div>
            </div>
            <div class="fx-testi">
                <div class="fx-testi-stars">★★★★☆</div>
                <p class="fx-testi-text">"The OTP screenshot tool saved a customer from a ₹50,000 scam. Simple to use, the phishing keyword highlighting is brilliant."</p>
                <div class="fx-testi-author">
                    <div class="fx-testi-avatar" style="background:#059669">ZM</div>
                    <div><div class="fx-testi-name">Zain Malik</div><div class="fx-testi-role">CTO · CyberSafe Pakistan</div></div>
                </div>
            </div>
            <div class="fx-testi">
                <div class="fx-testi-stars">★★★★★</div>
                <p class="fx-testi-text">"We integrated FraudX into our internal review workflow. The accuracy is exceptional and the speed is impressive. Highly recommended."</p>
                <div class="fx-testi-author">
                    <div class="fx-testi-avatar" style="background:#D97706">NB</div>
                    <div><div class="fx-testi-name">Nadia Baig</div><div class="fx-testi-role">Security Lead · BankLink</div></div>
                </div>
            </div>
            <div class="fx-testi">
                <div class="fx-testi-stars">★★★★★</div>
                <p class="fx-testi-text">"Our compliance team uses this for transaction audits. The risk score with reasons is perfect for regulatory documentation."</p>
                <div class="fx-testi-author">
                    <div class="fx-testi-avatar" style="background:#DC2626">OM</div>
                    <div><div class="fx-testi-name">Omar Mirza</div><div class="fx-testi-role">Compliance Officer · PakBank</div></div>
                </div>
            </div>
            <div class="fx-testi">
                <div class="fx-testi-stars">★★★★☆</div>
                <p class="fx-testi-text">"The platform is clean, fast, and the AI explanations are easy to understand for non-technical stakeholders. A great product overall."</p>
                <div class="fx-testi-author">
                    <div class="fx-testi-avatar" style="background:#0891B2">HA</div>
                    <div><div class="fx-testi-name">Hira Ali</div><div class="fx-testi-role">Product Manager · SecureNow</div></div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE — CONTACT
# ═══════════════════════════════════════════════════════════════════════════════
elif pg == "contact":
    st.markdown("<div class='fx-contact-section'>", unsafe_allow_html=True)
    # Create a centered two-column layout with spacing
    spacer, left_col, right_col, spacer2 = st.columns([0.1, 1, 1, 0.1])

    with left_col:
        st.markdown("""
        <div class="fx-eyebrow">Get In Touch</div>
        <div class="fx-section-title">Contact Us</div>
        <p style="color:#6B7280;font-size:0.9rem;line-height:1.8;margin:1rem 0 2rem;font-weight:400;">
            Have a question, partnership inquiry, or feedback? We'd love to hear from you.
        </p>
        <div class="fx-contact-item"><div class="fx-ci-icon">📧</div>
            <div><div class="fx-ci-label">Email</div><div class="fx-ci-val">contact@fraudx.ai</div></div>
        </div>
        <div class="fx-contact-item"><div class="fx-ci-icon">📍</div>
            <div><div class="fx-ci-label">Location</div><div class="fx-ci-val">Lahore, Punjab, Pakistan</div></div>
        </div>
        <div class="fx-contact-item"><div class="fx-ci-icon">🐙</div>
            <div><div class="fx-ci-label">GitHub</div><div class="fx-ci-val">github.com/fraudx-ai</div></div>
        </div>
        <div class="fx-contact-item"><div class="fx-ci-icon">💼</div>
            <div><div class="fx-ci-label">LinkedIn</div><div class="fx-ci-val">linkedin.com/company/fraudx</div></div>
        </div>
        """, unsafe_allow_html=True)

    with right_col:

        name_c, email_c = st.columns(2)
        with name_c:
            st.text_input("Full Name", placeholder="Your name")
        with email_c:
            st.text_input("Email Address", placeholder="you@email.com")
        st.text_input("Subject", placeholder="What's this about?")
        st.text_area("Message", placeholder="Tell us how we can help…", height=130)
        if st.button("Send Message →", key="send_msg"):
            st.success("✅ Message sent! We'll get back to you within 24 hours.")

    st.markdown("</div>", unsafe_allow_html=True)
# ═══════════════════════════════════════════════════════════════════════════════
# PAGE — FRAUD MODULE
# ═══════════════════════════════════════════════════════════════════════════════
elif pg == "fraud":

    # ── back button ──────────────────────────────────────────────────────────
    bcol, _ = st.columns([1, 5])
    with bcol:
        st.markdown('<div class="back-btn-wrap">', unsafe_allow_html=True)
        if st.button("← Back", key="back_fraud"):
            nav("services")
        st.markdown('</div>', unsafe_allow_html=True)

    # ── module header ────────────────────────────────────────────────────────
    st.markdown("""
    <div class="fx-module-header">
        <div class="fx-module-icon">💳</div>
        <div>
            <div class="fx-module-title">Credit Card Fraud Detection</div>
            <div class="fx-module-tag">Random Forest Classifier · 30 PCA Features</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── two columns ──────────────────────────────────────────────────────────
    col_l, col_r = st.columns(2, gap="large")

    with col_l:
        st.markdown('<div class="fx-acard">', unsafe_allow_html=True)
        st.markdown('<div class="fx-acard-label">Transaction Input</div>', unsafe_allow_html=True)
        amount = st.number_input("Transaction Amount (PKR / USD)", min_value=0.0, step=500.0, format="%.2f")
        run = st.button("⚡ Analyze Transaction", key="run_fraud")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        if run:
            if not models_ok or fraud_model is None:
                st.error("⚠️ Fraud model not loaded. Please train and save the model first.")
            else:
                input_data = np.zeros((1, 30))
                input_data[0][0] = amount
                probs = fraud_model.predict_proba(input_data)[0]
                fraud_prob = probs[1] * 100
                sc = score_class(fraud_prob)
                st.markdown(progress_color_css(fraud_prob), unsafe_allow_html=True)
                st.markdown(f"""
                <div class="fx-acard">
                    <div class="fx-acard-label">Risk Score</div>
                    <div class="fx-score-display">
                        <span class="fx-score-num {sc}">{fraud_prob:.1f}</span>
                        <span class="fx-score-unit">% fraud probability</span>
                    </div>
                """, unsafe_allow_html=True)
                st.progress(int(fraud_prob))
                st.markdown(verdict_html(fraud_prob, "fraud"), unsafe_allow_html=True)
                reasons = []
                if fraud_prob > 70: reasons.append("Pattern strongly deviates from normal behavior")
                if amount > 50000:  reasons.append("High-value transaction detected")
                if fraud_prob > 40: reasons.append("Anomaly detected in transaction feature space")
                if reasons:
                    st.markdown('<hr class="fx-divider"><div class="fx-acard-label">Analysis Signals</div>', unsafe_allow_html=True)
                    chips = "".join(f'<span class="fx-chip"><span class="fx-chip-dot"></span>{r}</span>' for r in reasons)
                    st.markdown(f'<div class="fx-chip-wrap">{chips}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="fx-placeholder">
                <div class="fx-ph-icon">💳</div>
                <div class="fx-ph-text">Enter amount and run analysis</div>
            </div>
            """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE — FAKE NEWS MODULE
# ═══════════════════════════════════════════════════════════════════════════════
elif pg == "news":

    bcol, _ = st.columns([1, 5])
    with bcol:
        st.markdown('<div class="back-btn-wrap">', unsafe_allow_html=True)
        if st.button("← Back", key="back_news"):
            nav("services")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="fx-module-header">
        <div class="fx-module-icon">📰</div>
        <div>
            <div class="fx-module-title">Fake News Detection</div>
            <div class="fx-module-tag">TF-IDF Vectorizer · Logistic Regression · 5K Features</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_l, col_r = st.columns(2, gap="large")

    with col_l:
        st.markdown('<div class="fx-acard">', unsafe_allow_html=True)
        st.markdown('<div class="fx-acard-label">Article Content</div>', unsafe_allow_html=True)
        news_text = st.text_area("Paste news article or headline", placeholder="Enter the full article text or headline to analyze…", height=200)
        run = st.button("🔍 Analyze Content", key="run_news")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        if run and news_text.strip():
            vec = vectorizer.transform([news_text])
            probs = fake_model.predict_proba(vec)[0]
            fake_index = list(fake_model.classes_).index(0)
            misinfo = probs[fake_index] * 100
            trigger_words = ["shocking", "breaking", "secret", "exposed",
                             "they don't want you to know", "miracle", "100% proof"]
            found = [w for w in trigger_words if w in news_text.lower()]
            sc = score_class(misinfo)
            st.markdown(progress_color_css(misinfo), unsafe_allow_html=True)
            st.markdown(f"""
            <div class="fx-acard">
                <div class="fx-acard-label">Misinformation Score</div>
                <div class="fx-score-display">
                    <span class="fx-score-num {sc}">{misinfo:.1f}</span>
                    <span class="fx-score-unit">% misinformation probability</span>
                </div>
            """, unsafe_allow_html=True)
            st.progress(int(misinfo))
            st.markdown(verdict_html(misinfo, "news"), unsafe_allow_html=True)
            if found:
                st.markdown('<hr class="fx-divider"><div class="fx-acard-label">Manipulative Language Detected</div>', unsafe_allow_html=True)
                chips = "".join(f'<span class="fx-chip-warn">⚠ {t}</span>' for t in found)
                st.markdown(f'<div class="fx-chip-wrap" style="margin-top:4px">{chips}</div>', unsafe_allow_html=True)
            explain = []
            if misinfo > 60: explain.append("Structure resembles known misinformation patterns")
            if found:        explain.append("Emotionally manipulative wording detected")
            if len(news_text.split()) < 80: explain.append("Very short articles are often unreliable")
            if explain:
                st.markdown('<hr class="fx-divider"><div class="fx-acard-label">Analysis Signals</div>', unsafe_allow_html=True)
                chips = "".join(f'<span class="fx-chip"><span class="fx-chip-dot"></span>{e}</span>' for e in explain)
                st.markdown(f'<div class="fx-chip-wrap">{chips}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        elif run:
            st.markdown('<div class="fx-verdict vb-warning">⚠️&nbsp;&nbsp;Please enter some text to analyze.</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="fx-placeholder">
                <div class="fx-ph-icon">📰</div>
                <div class="fx-ph-text">Enter article text and run analysis</div>
            </div>
            """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE — OTP MODULE
# ═══════════════════════════════════════════════════════════════════════════════
elif pg == "otp":

    bcol, _ = st.columns([1, 5])
    with bcol:
        st.markdown('<div class="back-btn-wrap">', unsafe_allow_html=True)
        if st.button("← Back", key="back_otp"):
            nav("services")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="fx-module-header">
        <div class="fx-module-icon">📲</div>
        <div>
            <div class="fx-module-title">OTP Phishing Detector</div>
            <div class="fx-module-tag">Tesseract OCR · NLP Scam Classifier</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_l, col_r = st.columns(2, gap="large")

    with col_l:
        st.markdown('<div class="fx-acard">', unsafe_allow_html=True)
        st.markdown('<div class="fx-acard-label">Upload Screenshot</div>', unsafe_allow_html=True)
        uploaded = st.file_uploader("Drag & drop or click to browse", type=["png", "jpg", "jpeg"])
        if uploaded:
            image = Image.open(uploaded)
            st.image(image, caption="Uploaded Screenshot", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        if uploaded:
            image = Image.open(uploaded)
            extracted = pytesseract.image_to_string(image)
            display_text = extracted.strip() or "No readable text detected."
            st.markdown(f"""
            <div class="fx-acard">
                <div class="fx-acard-label">OCR — Extracted Text</div>
                <div class="fx-ocr">{display_text}</div>
            </div>
            """, unsafe_allow_html=True)
            red_flags = ["urgent", "click", "link", "verify", "share", "blocked",
                         "suspend", "prize", "call now", "confirm", "account"]
            found_flags = [w for w in red_flags if w in extracted.lower()]
            vec = otp_vectorizer.transform([extracted])
            probs = otp_model.predict_proba(vec)[0]
            fake_index = list(otp_model.classes_).index("fake")
            risk = probs[fake_index] * 100
            sc = score_class(risk)
            st.markdown(progress_color_css(risk), unsafe_allow_html=True)
            st.markdown(f"""
            <div class="fx-acard">
                <div class="fx-acard-label">Fraud Risk Score</div>
                <div class="fx-score-display">
                    <span class="fx-score-num {sc}">{risk:.1f}</span>
                    <span class="fx-score-unit">% scam probability</span>
                </div>
            """, unsafe_allow_html=True)
            st.progress(int(risk))
            st.markdown(verdict_html(risk, "otp"), unsafe_allow_html=True)
            if found_flags:
                st.markdown('<hr class="fx-divider"><div class="fx-acard-label">Phishing Keywords</div>', unsafe_allow_html=True)
                chips = "".join(f'<span class="fx-chip-warn">⚠ {f}</span>' for f in found_flags)
                st.markdown(f'<div class="fx-chip-wrap" style="margin-top:4px">{chips}</div>', unsafe_allow_html=True)
            explanations = []
            if risk > 60:   explanations.append("Message uses known manipulation patterns")
            if found_flags: explanations.append("Contains phishing keywords")
            if "otp" in extracted.lower(): explanations.append("Requests sensitive authentication code")
            if explanations:
                st.markdown('<hr class="fx-divider"><div class="fx-acard-label">Analysis Signals</div>', unsafe_allow_html=True)
                chips = "".join(f'<span class="fx-chip"><span class="fx-chip-dot"></span>{e}</span>' for e in explanations)
                st.markdown(f'<div class="fx-chip-wrap">{chips}</div>', unsafe_allow_html=True)
            st.markdown('<hr class="fx-divider"><div class="fx-acard-label">Feedback</div>', unsafe_allow_html=True)
            fb = st.radio("Was this analysis accurate?", ["👍  Yes, helpful", "👎  No, incorrect"], label_visibility="collapsed")
            if fb == "👍  Yes, helpful":
                st.markdown('<div class="fx-verdict vb-success" style="margin-top:8px">✅&nbsp;&nbsp;Thank you — your feedback improves our model.</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="fx-verdict vb-warning" style="margin-top:8px">📝&nbsp;&nbsp;Noted — we will use this to improve detection.</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="fx-placeholder" style="min-height:280px">
                <div class="fx-ph-icon">📲</div>
                <div class="fx-ph-text">Upload a screenshot to begin</div>
            </div>
            """, unsafe_allow_html=True)