import numpy as np
import datetime
import streamlit as st

# ── Cities ────────────────────────────────────────────────────
CITIES = ["Delhi", "Mumbai", "Bangalore", "Chennai",
          "Hyderabad", "Kolkata", "Ahmedabad", "Pune"]
CITY_CODES = {c: i for i, c in enumerate(sorted(CITIES))}

# ── AQI band lookup ───────────────────────────────────────────
def get_band(aqi):
    if aqi <= 50:
        return "Good", "#00b050", "😊 Air is clean. Safe for everyone."
    elif aqi <= 100:
        return "Satisfactory", "#92d050", "🙂 Acceptable. Sensitive people take care outdoors."
    elif aqi <= 200:
        return "Moderate", "#ffcc00", "😐 Sensitive groups may feel effects. Limit outdoor time."
    elif aqi <= 300:
        return "Poor", "#ff7c00", "😷 Everyone may feel effects. Wear a mask outside."
    elif aqi <= 400:
        return "Very Poor", "#ff0000", "🚫 Serious health risk. Avoid going outside."
    else:
        return "Severe", "#7030a0", "☠️ Emergency conditions. Stay indoors — windows shut!"

def get_st_status(aqi):
    if aqi <= 100:
        return "success"
    elif aqi <= 300:
        return "warning"
    else:
        return "error"

# ── Feature vector builder ────────────────────────────────────
def build_features(pm25, pm10, no, no2, nox, nh3, co, so2, o3,
                   lag1, lag2, lag3, lag7, city):
    now = datetime.datetime.now()
    month = now.month
    dow   = now.weekday()
    doy   = now.timetuple().tm_yday
    roll_mean_3 = (lag1 + lag2 + lag3) / 3
    roll_mean_7 = lag7
    roll_std_3  = np.std([lag1, lag2, lag3])
    roll_std_7  = 5.0
    month_sin = np.sin(2 * np.pi * month / 12)
    month_cos = np.cos(2 * np.pi * month / 12)
    dow_sin   = np.sin(2 * np.pi * dow / 7)
    dow_cos   = np.cos(2 * np.pi * dow / 7)
    is_weekend = 1 if dow >= 5 else 0
    city_code  = CITY_CODES.get(city, 3)
    return np.array([[pm25, pm10, no, no2, nox, nh3, co, so2, o3,
                      lag1, lag2, lag3, lag7,
                      roll_mean_3, roll_mean_7, roll_std_3, roll_std_7,
                      month_sin, month_cos, dow_sin, dow_cos,
                      is_weekend, doy, city_code]])

# ── Sidebar info (shown on every page) ───────────────────────
def show_sidebar_info():
    st.sidebar.divider()
    st.sidebar.caption("**Dataset:** Air Quality Data in India  \nRohan Rao · Kaggle · CC0 Public Domain")
    st.sidebar.caption(
        "**Team:**  \n"
        "Muhya Fatima  \n"
        "Saniya Begum  \n"
        "Amrita Kumari Chauhan  \n"
        "Harry Nikita Beulat"
    )
