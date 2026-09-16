import streamlit as st
import plotly.graph_objects as go
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.helpers import show_sidebar_info

st.set_page_config(page_title="Model Comparison — AQI Shield", page_icon="🤖", layout="wide")

st.sidebar.title("🌫️ AQI Shield")
st.sidebar.caption("AI-Powered Air Quality Forecast")
show_sidebar_info()

# ══════════════════════════════════════════════════════════════
st.title("🤖 Model Comparison")
st.caption("We trained 3 machine learning models and compared their performance on test data.")
st.divider()

# ── Currently used model banner ────────────────────────────────
st.success("✅ **Currently Deployed Model: Linear Regression** — Selected for its highest accuracy (R² = 0.96) on the test dataset.")

st.divider()

# ── Model comparison table ─────────────────────────────────────
st.subheader("📊 Performance Metrics")

col_header, col_lr, col_rf, col_xgb = st.columns([2, 1.5, 1.5, 1.5])
col_header.markdown("**Metric**")
col_lr.markdown("**Linear Regression** ✅")
col_rf.markdown("**Random Forest**")
col_xgb.markdown("**XGBoost**")

st.markdown("---")

rows = [
    ("R² Score (↑ better)",  "**0.9600**", "0.9541", "0.9437"),
    ("RMSE (↓ better)",      "**18.4**",   "19.8",   "21.6"),
    ("MAE (↓ better)",       "**11.2**",   "12.5",   "13.8"),
    ("In Use",               "✅ Yes",      "—",      "—"),
]

for metric, lr_val, rf_val, xgb_val in rows:
    c1, c2, c3, c4 = st.columns([2, 1.5, 1.5, 1.5])
    c1.markdown(metric)
    c2.markdown(lr_val)
    c3.markdown(rf_val)
    c4.markdown(xgb_val)

st.divider()

# ── Bar chart ──────────────────────────────────────────────────
models_data = [
    {"name": "Linear Regression", "r2": 0.9600, "rmse": 18.4, "mae": 11.2},
    {"name": "Random Forest",     "r2": 0.9541, "rmse": 19.8, "mae": 12.5},
    {"name": "XGBoost",           "r2": 0.9437, "rmse": 21.6, "mae": 13.8},
]

fig_bar = go.Figure(go.Bar(
    x=[m["name"] for m in models_data],
    y=[m["r2"] for m in models_data],
    marker_color=["#00b4d8", "#0077b6", "#023e8a"],
    text=[str(m["r2"]) for m in models_data],
    textposition='outside'
))
fig_bar.update_layout(
    title="R² Score Comparison (higher = better)",
    yaxis=dict(range=[0.92, 1.0]),
    height=360,
    margin=dict(t=50, b=20, l=60, r=20)
)
st.plotly_chart(fig_bar, use_container_width=True)

st.divider()
st.subheader("💡 Why did we choose Linear Regression?")
st.write("""
- It gave the **highest R² score of 0.96** on test data
- R² = 0.96 means the model correctly explains **96% of AQI variation**
- Random Forest (0.9541) and XGBoost (0.9437) also performed very well
""")
