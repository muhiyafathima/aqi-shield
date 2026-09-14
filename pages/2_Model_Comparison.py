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

models_data = [
    {"name": "Linear Regression", "r2": 0.9600, "rmse": 18.4, "mae": 11.2, "best": True},
    {"name": "Random Forest",     "r2": 0.9541, "rmse": 19.8, "mae": 12.5, "best": False},
    {"name": "XGBoost",           "r2": 0.9437, "rmse": 21.6, "mae": 13.8, "best": False},
]

# Metric cards
m1, m2, m3 = st.columns(3)
for col, m in zip([m1, m2, m3], models_data):
    delta_label = "✅ Best Model" if m["best"] else None
    col.metric(
        label=m["name"],
        value=m["r2"],
        delta=delta_label,
        delta_color="normal" if m["best"] else "off"
    )
    col.caption(f"RMSE: **{m['rmse']}** &nbsp;&nbsp; MAE: **{m['mae']}**")

st.divider()

# Bar chart
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
- Simple, fast, and easy to explain in a viva
- Random Forest (0.9541) and XGBoost (0.9437) also performed very well
""")
