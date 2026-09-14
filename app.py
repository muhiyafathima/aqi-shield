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

# ── Sidebar ───────────────────────────────────────────────────
st.sidebar.title("🌫️ AQI Shield")
st.sidebar.caption("AI-Powered Air Quality Forecast")
show_sidebar_info()

# ── Load models ───────────────────────────────────────────────
@st.cache_resource
def load_models():
    lr = joblib.load('models/linear_regression.pkl')
    sc = joblib.load('models/scaler.pkl')
    return lr, sc

lr_model, scaler = load_models()

# ══════════════════════════════════════════════════════════════
# FORECAST DASHBOARD
# ══════════════════════════════════════════════════════════════
st.title("🌫️ AQI Shield — Air Quality Forecast")
st.caption("Enter today's pollution readings to predict the Air Quality Index for your city.")
st.divider()

inp_col, result_col = st.columns([1, 1], gap="large")

# ─── LEFT: Inputs ─────────────────────────────────────────────
with inp_col:
    st.subheader("🏙️ City & Pollutant Inputs")

    city = st.selectbox("Select City", CITIES)

    st.write("**Pollutant Levels (µg/m³)**")
    c1, c2, c3 = st.columns(3)
    with c1:
        pm25 = st.number_input("PM2.5", min_value=0.0, value=60.0, step=1.0)
        no   = st.number_input("NO",    min_value=0.0, value=10.0, step=1.0)
        nh3  = st.number_input("NH3",   min_value=0.0, value=10.0, step=1.0)
    with c2:
        pm10 = st.number_input("PM10",  min_value=0.0, value=90.0, step=1.0)
        no2  = st.number_input("NO2",   min_value=0.0, value=25.0, step=1.0)
        co   = st.number_input("CO",    min_value=0.0, value=1.0,  step=0.1)
    with c3:
        nox  = st.number_input("NOx",   min_value=0.0, value=35.0, step=1.0)
        so2  = st.number_input("SO2",   min_value=0.0, value=12.0, step=1.0)
        o3   = st.number_input("O3",    min_value=0.0, value=40.0, step=1.0)

    st.write("**Recent AQI History**")
    h1, h2 = st.columns(2)
    with h1:
        lag1 = st.number_input("Yesterday",  min_value=0.0, value=120.0, step=1.0)
        lag3 = st.number_input("3 days ago", min_value=0.0, value=110.0, step=1.0)
    with h2:
        lag2 = st.number_input("2 days ago", min_value=0.0, value=115.0, step=1.0)
        lag7 = st.number_input("Last week",  min_value=0.0, value=105.0, step=1.0)

    st.write("")
    predict_btn = st.button("🔍 Predict AQI Now", use_container_width=True, type="primary")

# ─── RIGHT: Results ────────────────────────────────────────────
with result_col:
    st.subheader("📈 Prediction Result")

    if predict_btn:
        features = build_features(pm25, pm10, no, no2, nox, nh3, co, so2, o3,
                                  lag1, lag2, lag3, lag7, city)
        features_scaled = scaler.transform(features)
        pred = float(np.clip(lr_model.predict(features_scaled)[0], 0, 500))
        pred = round(pred, 1)

        label, color, advice = get_band(pred)
        avg7  = round((lag1 + lag2 + lag3 + lag7) / 4, 1)
        delta = round(pred - lag1, 1)

        # Metric cards
        k1, k2, k3 = st.columns(3)
        k1.metric("Predicted AQI", pred, delta=f"{delta:+.1f} vs yesterday")
        k2.metric("Category", label)
        k3.metric("7-Day Avg AQI", avg7)

        st.divider()

        # Health advisory
        status = get_st_status(pred)
        if status == "success":
            st.success(f"**{label}** — {advice}")
        elif status == "warning":
            st.warning(f"**{label}** — {advice}")
        else:
            st.error(f"**{label}** — {advice}")

        # AQI progress bar
        st.caption("AQI Level Indicator (0–500)")
        st.progress(min(int(pred / 5), 100))

        # Gauge chart
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=pred,
            number={'suffix': " AQI", 'font': {'size': 40}},
            gauge={
                'axis': {'range': [0, 500], 'tickwidth': 1},
                'bar':  {'color': color},
                'steps': [
                    {'range': [0,   50],  'color': '#00b050'},
                    {'range': [50,  100], 'color': '#92d050'},
                    {'range': [100, 200], 'color': '#ffcc00'},
                    {'range': [200, 300], 'color': '#ff7c00'},
                    {'range': [300, 400], 'color': '#ff0000'},
                    {'range': [400, 500], 'color': '#7030a0'},
                ],
                'threshold': {'line': {'color': 'white', 'width': 3}, 'value': pred}
            },
            title={'text': f"Predicted AQI — {city}"}
        ))
        fig_gauge.update_layout(height=280, margin=dict(t=50, b=0, l=20, r=20))
        st.plotly_chart(fig_gauge, use_container_width=True)

        # 7-Day Trend
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
            title="7-Day AQI Trend", height=220,
            margin=dict(t=36, b=16, l=40, r=10),
            showlegend=False,
            yaxis=dict(range=[0, max(aqi_vals) * 1.25])
        )
        st.plotly_chart(fig_trend, use_container_width=True)

        # Pollutant bar chart
        poll_names = ['PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'SO2', 'O3']
        poll_vals  = [pm25, pm10, no, no2, nox, nh3, so2, o3]
        fig_pol = go.Figure(go.Bar(
            x=poll_names, y=poll_vals,
            marker_color='#0077b6',
            text=[f'{v:.1f}' for v in poll_vals],
            textposition='outside'
        ))
        fig_pol.update_layout(
            title="Pollutant Breakdown (µg/m³)", height=220,
            margin=dict(t=36, b=10, l=40, r=10),
            showlegend=False
        )
        st.plotly_chart(fig_pol, use_container_width=True)

    else:
        st.info("👈 Fill in the values on the left and click **Predict AQI Now**")

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
