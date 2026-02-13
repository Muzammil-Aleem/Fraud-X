import streamlit as st
import joblib
import numpy as np
import pytesseract
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
st.markdown("### AI-Powered Transaction & Message Verification System")
st.markdown("---")

st.title("FraudX — AI Security System")

# Load models
fraud_model = joblib.load("models/fraud_model.pkl")
fake_model = joblib.load("models/fake_model.pkl")
vectorizer = joblib.load("models/vectorizer.pkl")
otp_model = joblib.load("models/otp_model.pkl")
otp_vectorizer = joblib.load("models/otp_vectorizer.pkl")

menu = st.sidebar.selectbox(
    "Choose Feature",
    ["Fraud Detection", "Fake News Detection", "OTP Screenshot Detection"]
)

# ---------------- FRAUD ----------------
if menu == "Fraud Detection":
    st.header("Credit Card Fraud Detection")

    amount = st.number_input("Transaction Amount")

    if st.button("Predict Fraud"):
        input_data = np.zeros((1, 30))
        input_data[0][0] = amount

        prediction = fraud_model.predict(input_data)[0]

        probs = fraud_model.predict_proba(input_data)[0]
        fraud_probability = probs[1] * 100
        st.subheader("Transaction Risk Score")

        st.progress(int(fraud_probability))
        st.write(f"Fraud Probability: {fraud_probability:.2f}%")
        st.subheader("AI Transaction Analysis")

        reasons = []

        if fraud_probability > 70:
            reasons.append("Transaction pattern strongly deviates from normal behavior.")

        if amount > 50000:
            reasons.append("High-value transaction detected.")

        if fraud_probability > 40:
            reasons.append("Model detected anomaly in transaction features.")

        for r in reasons:
            st.write("✔", r)

        if fraud_probability > 70:
            st.error("🚨 HIGH FRAUD RISK")
        elif fraud_probability > 40:
            st.warning("⚠ Suspicious Transaction")
        else:
            st.success("✅ Transaction Appears Normal")

# ---------------- FAKE NEWS ----------------
if menu == "Fake News Detection":
    st.header("Fake News Detection")

    news = st.text_area("Enter News Text")

    if st.button("Analyze"):
        vec = vectorizer.transform([news])
        prediction = fake_model.predict(vec)[0]

        probs = fake_model.predict_proba(vec)[0]
        fake_index = list(fake_model.classes_).index(0)
        misinfo_score = probs[fake_index] * 100
        st.subheader("Misinformation Risk")

        st.progress(int(misinfo_score))
        st.write(f"Misinformation Probability: {misinfo_score:.2f}%")
        st.subheader("Content Analysis")

        trigger_words = ["shocking", "breaking", "secret", "exposed",
                        "they don't want you to know", "miracle", "100% proof"]

        found_triggers = [w for w in trigger_words if w in news.lower()]

        if found_triggers:
            st.warning("Manipulative Language Detected:")
            for t in found_triggers:
                st.write("•", t)
        else:
            st.write("No sensational language detected.")
        st.subheader("AI Explanation")

        explain = []

        if misinfo_score > 60:
            explain.append("Article structure resembles known misinformation patterns.")

        if len(found_triggers) > 0:
            explain.append("Emotionally manipulative wording detected.")

        if len(news.split()) < 80:
            explain.append("Very short articles are often unreliable.")

        for e in explain:
            st.write("✔", e)

        if misinfo_score > 70:
            st.error("🚨 Likely Fake News")
        elif misinfo_score > 40:
            st.warning("⚠ Needs Verification")
        else:
            st.success("✅ Appears Credible")

if menu == "OTP Screenshot Detection":
    st.header("Upload OTP Screenshot")

    uploaded_file = st.file_uploader("Upload Image", type=["png","jpg","jpeg"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)

        st.image(image, caption="Uploaded Screenshot")

        # OCR Extract Text
        extracted_text = pytesseract.image_to_string(image)

        st.subheader("Extracted Text:")
        st.write(extracted_text)
        st.subheader("Behavioral Analysis")

        red_flags = ["urgent", "click", "link", "verify", "share", "blocked",
                    "suspend", "prize", "call now", "confirm", "account"]

        found_flags = [word for word in red_flags if word in extracted_text.lower()]
        if found_flags:
            st.warning("Suspicious Language Detected:")
            for flag in found_flags:
                st.write(f"• {flag}")
        else:
            st.write("No strong phishing indicators detected.")

        # Predict
        vec = otp_vectorizer.transform([extracted_text])
        # Prediction
        prediction = otp_model.predict(vec)[0]

        # Get probability score
        probs = otp_model.predict_proba(vec)[0]
        fake_index = list(otp_model.classes_).index("fake")
        risk_score = probs[fake_index] * 100

        st.subheader("Fraud Risk Score")

        st.progress(int(risk_score))
        st.write(f"Risk Level: {risk_score:.2f}%")

        if risk_score > 70:
            st.error("🚨 HIGH RISK: Likely Scam")
        elif risk_score > 40:
            st.warning("⚠ MEDIUM RISK: Suspicious Message")
        else:
            st.success("✅ LOW RISK: Appears Legitimate")
        st.subheader("AI Explanation")

        explanations = []

        if risk_score > 60:
            explanations.append("Message uses manipulation patterns.")

        if len(found_flags) > 0:
            explanations.append("Contains known phishing keywords.")

        if "otp" in extracted_text.lower():
            explanations.append("Requests sensitive authentication information.")

        for exp in explanations:
            st.write("✔", exp)
        st.subheader("User Feedback")

        feedback = st.radio("Was this analysis helpful?", ["Yes", "No"])

        if feedback == "Yes":
            st.success("Thank you. Your feedback improves usability.")
        else:
            st.info("We will use this to improve detection.")
