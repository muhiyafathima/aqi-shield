import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.helpers import show_sidebar_info

st.set_page_config(page_title="About — AQI Shield", page_icon="ℹ️", layout="wide")

st.sidebar.title("🌫️ AQI Shield")
st.sidebar.caption("AI-Powered Air Quality Forecast")
show_sidebar_info()

# ══════════════════════════════════════════════════════════════
st.title("ℹ️ About AQI Shield")
st.caption("AI-Powered Air Quality Forecasting & Advisory System — Major Project Phase II")
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("🌫️ What is AQI?")
    st.write("""
    **Air Quality Index (AQI)** is a number used to communicate how polluted
    the air is. India uses the CPCB AQI scale from **0 to 500**.

    Higher AQI = worse air quality = more dangerous for health.

    AQI is calculated from 8 pollutants:
    PM2.5, PM10, NO₂, SO₂, CO, O₃, NH₃, NOx
    """)

    st.subheader("📊 Dataset")
    st.write("""
    **Air Quality Data in India (2015–2020)**
    - Author: Rohan Rao (rohanrao)
    - Source: Kaggle
    - License: CC0 1.0 Public Domain
    - File: city_day.csv — 29,531 rows
    - 8 cities: Delhi, Mumbai, Bangalore, Chennai,
      Hyderabad, Kolkata, Ahmedabad, Pune
    """)

with col2:
    st.subheader("🛠️ How It Works")
    st.write("""
    1. **Data Cleaning** — remove duplicates, fill missing values
    2. **Features/Targets** — lag features, rolling averages, calendar features
    3. **Model Training** — Linear Regression, Random Forest, XGBoost
    4. **Evaluation** — compare R² scores (Linear Regression wins at 0.96)
    5. **Prediction** — enter today's values → get AQI forecast
    6. **AI Advisor** — Groq LLaMA-3 answers health questions using zero-shot prompting
    """)

    st.subheader("👥 Project Team")
    st.write("""
    - Muhya Fatima
    - Saniya Begum
    - Amrita Kumari Chauhan
    - Harry Nikita Beulat
    """)

    st.subheader("⚙️ Built With")
    st.write("Python · Streamlit · Scikit-learn · XGBoost · Plotly · Groq LLaMA-3 · Google Colab")
