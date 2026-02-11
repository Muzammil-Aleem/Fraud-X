import streamlit as st
import joblib
import numpy as np
import pytesseract
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

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

        result = fraud_model.predict(input_data)

        if result[0] == 1:
            st.error("Fraudulent Transaction")
        else:
            st.success("Legitimate Transaction")

# ---------------- FAKE NEWS ----------------
if menu == "Fake News Detection":
    st.header("Fake News Detection")

    news = st.text_area("Enter News Text")

    if st.button("Analyze"):
        vec = vectorizer.transform([news])
        result = fake_model.predict(vec)

        if result[0] == 1:
            st.success("Real News")
        else:
            st.error("Fake News")

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

        # Predict
        vec = otp_vectorizer.transform([extracted_text])
        result = otp_model.predict(vec)[0]

        if result == "fake":
            st.error("⚠ This looks like a SCAM message!")
        else:
            st.success("✔ This appears to be a legitimate OTP message.")
