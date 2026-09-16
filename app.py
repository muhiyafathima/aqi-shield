import streamlit as st
import joblib
import numpy as np
import plotly.graph_objects as go
import sys
import os

sys.path.append(os.path.dirname(__file__))
from utils.helpers import CITIES, get_band, get_st_status, build_features, show_sidebar_info

# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title="AQI Shield",
    page_icon="🌫️",
    layout="wide"
)

# ── Sidebar (info only) ───────────────────────────────────────
st.sidebar.title("🌫️ AQI Shield")
st.sidebar.caption("AI-Powered Air Quality Forecast")
show_sidebar_info()

# ── Load model ────────────────────────────────────────────────
@st.cache_resource
def load_models():
    lr = joblib.load('models/linear_regression.pkl')
    sc = joblib.load('models/scaler.pkl')
    return lr, sc

lr_model, scaler = load_models()

# ══════════════════════════════════════════════════════════════
# MAIN PAGE
# ══════════════════════════════════════════════════════════════
st.title("🌫️ AQI Shield — Air Quality Forecast")
st.caption("Enter pollutant readings below and click **Predict AQI Now**.")
st.divider()

# ── Two-column layout: inputs (left) | gauge (right) ─────────
col_inputs, col_gauge = st.columns([1, 1.2], gap="large")

with col_inputs:
    st.subheader("🏙️ City & Inputs")
    city = st.selectbox("Select City", CITIES)

    st.write("**Pollutant Levels (µg/m³)**")
    r1c1, r1c2, r1c3 = st.columns(3)
    pm25 = r1c1.number_input("PM2.5", min_value=0.0, value=60.0, step=1.0)
    pm10 = r1c2.number_input("PM10",  min_value=0.0, value=90.0, step=1.0)
    no   = r1c3.number_input("NO",    min_value=0.0, value=10.0, step=1.0)

    r2c1, r2c2, r2c3 = st.columns(3)
    no2  = r2c1.number_input("NO2",   min_value=0.0, value=25.0, step=1.0)
    nox  = r2c2.number_input("NOx",   min_value=0.0, value=35.0, step=1.0)
    nh3  = r2c3.number_input("NH3",   min_value=0.0, value=10.0, step=1.0)

    r3c1, r3c2, r3c3 = st.columns(3)
    co   = r3c1.number_input("CO",    min_value=0.0, value=1.0,  step=0.1)
    so2  = r3c2.number_input("SO2",   min_value=0.0, value=12.0, step=1.0)
    o3   = r3c3.number_input("O3",    min_value=0.0, value=40.0, step=1.0)

    st.write("**Recent AQI History**")
    h1c1, h1c2 = st.columns(2)
    lag1 = h1c1.number_input("Yesterday",  min_value=0.0, value=120.0, step=1.0)
    lag2 = h1c2.number_input("2 days ago", min_value=0.0, value=115.0, step=1.0)
    h2c1, h2c2 = st.columns(2)
    lag3 = h2c1.number_input("3 days ago", min_value=0.0, value=110.0, step=1.0)
    lag7 = h2c2.number_input("Last week",  min_value=0.0, value=105.0, step=1.0)

    predict_btn = st.button("🔍 Predict AQI Now", use_container_width=True, type="primary")

# ── Compute prediction ────────────────────────────────────────
if predict_btn:
    features = build_features(pm25, pm10, no, no2, nox, nh3, co, so2, o3,
                              lag1, lag2, lag3, lag7, city)
    features_scaled = scaler.transform(features)
    pred = float(np.clip(lr_model.predict(features_scaled)[0], 0, 500))
    pred = round(pred, 1)
    st.session_state["pred"]  = pred
    st.session_state["city"]  = city
    st.session_state["lags"]  = (lag1, lag2, lag3, lag7)
    st.session_state["polls"] = (pm25, pm10, no, no2, nox, nh3, so2, o3)

pred      = st.session_state.get("pred", 0)
scity     = st.session_state.get("city", city)
lags      = st.session_state.get("lags", (lag1, lag2, lag3, lag7))
polls     = st.session_state.get("polls", (pm25, pm10, no, no2, nox, nh3, so2, o3))
predicted = st.session_state.get("pred") is not None

# ── Gauge (right column) ──────────────────────────────────────
with col_gauge:
    label, color, advice = get_band(pred) if predicted else ("—", "#cccccc", "")

    st.caption("AQI Level Indicator (0–500)")
    st.progress(min(int(pred / 5), 100) if predicted else 0)

    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=pred,
        number={'suffix': " AQI", 'font': {'size': 42, 'color': color if predicted else '#aaaaaa'}},
        gauge={
            'axis': {'range': [0, 500], 'tickwidth': 1},
            'bar':  {'color': color if predicted else '#e0e0e0'},
            'steps': [
                {'range': [0,   50],  'color': '#00b050'},
                {'range': [50,  100], 'color': '#92d050'},
                {'range': [100, 200], 'color': '#ffcc00'},
                {'range': [200, 300], 'color': '#ff7c00'},
                {'range': [300, 400], 'color': '#ff0000'},
                {'range': [400, 500], 'color': '#7030a0'},
            ],
            'threshold': {
                'line': {'color': 'white', 'width': 4},
                'value': pred
            }
        },
        title={'text': f"Predicted AQI — {scity}" if predicted else "Predicted AQI"}
    ))
    fig_gauge.update_layout(height=280, margin=dict(t=50, b=0, l=30, r=30))
    st.plotly_chart(fig_gauge, use_container_width=True)

    if predicted:
        status = get_st_status(pred)
        if status == "success":
            st.success(f"**{label}** — {advice}")
        elif status == "warning":
            st.warning(f"**{label}** — {advice}")
        else:
            st.error(f"**{label}** — {advice}")
    else:
        st.info("Fill in the values and click **Predict AQI Now**")

# ── After prediction: trend + pollutant charts ────────────────
if predicted:
    st.divider()
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        lag1, lag2, lag3, lag7 = lags
        days = ["6d ago", "5d ago", "4d ago", "3d ago", "2d ago", "Yesterday", "Today"]
        mid1 = round((lag7 + lag3) / 2, 1)
        mid2 = round((lag3 + lag2) / 2, 1)
        aqi_vals = [lag7, mid1, mid2, lag3, lag2, lag1, pred]

        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=days, y=aqi_vals,
            mode='lines+markers',
            line=dict(color='#0077b6', width=2.5),
            marker=dict(size=8, color=[get_band(v)[1] for v in aqi_vals]),
            fill='tozeroy',
            fillcolor='rgba(0,119,182,0.1)',
        ))
        fig_trend.update_layout(
            title="7-Day AQI Trend", height=240,
            margin=dict(t=36, b=16, l=40, r=10),
            showlegend=False,
            yaxis=dict(range=[0, max(aqi_vals) * 1.25])
        )
        st.plotly_chart(fig_trend, use_container_width=True)

    with chart_col2:
        pm25, pm10, no, no2, nox, nh3, so2, o3 = polls
        poll_names = ['PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'SO2', 'O3']
        poll_vals  = [pm25, pm10, no, no2, nox, nh3, so2, o3]
        fig_pol = go.Figure(go.Bar(
            x=poll_names, y=poll_vals,
            marker_color='#0077b6',
            text=[f'{v:.1f}' for v in poll_vals],
            textposition='outside'
        ))
        fig_pol.update_layout(
            title="Pollutant Breakdown (µg/m³)", height=240,
            margin=dict(t=36, b=10, l=40, r=10),
            showlegend=False
        )
        st.plotly_chart(fig_pol, use_container_width=True)

# ── CPCB Scale Reference ──────────────────────────────────────
st.divider()
st.caption("**📋 CPCB AQI Scale Reference**")
bands_ref = [
    ("Good",        "0–50"),
    ("Satisfactory","51–100"),
    ("Moderate",    "101–200"),
    ("Poor",        "201–300"),
    ("Very Poor",   "301–400"),
    ("Severe",      "401–500"),
]
ref_cols = st.columns(6)
for i, (lbl, rng) in enumerate(bands_ref):
    ref_cols[i].metric(label=lbl, value=rng)
