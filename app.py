import streamlit as st
import pandas as pd
import os
from groq import Groq

# -----------------------
# Load GROQ API KEY
# -----------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

# -----------------------
# Fungsi Analisis Rasio
# -----------------------
def calculate_ratios(df):
    df["Current Ratio"] = df["Current Assets"] / df["Current Liabilities"]
    df["Debt to Equity"] = df["Total Liabilities"] / df["Equity"]
    df["Net Profit Margin"] = df["Net Income"] / df["Revenue"]
    return df

# -----------------------
# AI AGENT ANALISIS
# -----------------------
def ai_analysis(text):
    response = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {"role": "system", "content": "You are an expert financial analyst."},
            {"role": "user", "content": f"Berikan analisis lengkap dari rasio keuangan berikut:\n{text}"}
        ]
    )
    return response.choices[0].message["content"]


# -----------------------
# STREAMLIT UI
# -----------------------
st.title("📊 Financial Ratio AI Agent")
st.write("Upload laporan keuangan untuk menghitung rasio + analisis otomatis")

uploaded = st.file_uploader("Upload Excel", type=["xlsx"])

if uploaded:
    df = pd.read_excel(uploaded)

    st.subheader("Raw Data")
    st.dataframe(df)

    df_ratio = calculate_ratios(df)

    st.subheader("Hasil Perhitungan Rasio")
    st.dataframe(df_ratio)

    # Convert rasio ke text
    ratio_text = df_ratio.to_string()

    if st.button("🔍 Analisis Dengan AI"):
        with st.spinner("AI sedang menganalisis..."):
            analysis = ai_analysis(ratio_text)
        st.subheader("📘 Hasil Analisis AI")
        st.write(analysis)
