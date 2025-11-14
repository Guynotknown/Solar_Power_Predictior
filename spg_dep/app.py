# Ultra-premium Solar Theme (HYBRID) app.py
# Copy entire file into spg_dep/app.py

import streamlit as st
import pickle
import pandas as pd
import numpy as np
import os
from pathlib import Path
import base64
from datetime import datetime

# -------------------------
# Page config
# -------------------------
st.set_page_config(page_title="Solar Power Predictor - Solar UI",
                   page_icon="☀️",
                   layout="wide",
                   initial_sidebar_state="auto")

# -------------------------
# Utility: load model & scaler
# -------------------------
@st.cache_resource(show_spinner=False)
def load_model_and_scaler():
    try:
        model_path = Path("spg_dep") / "model.pkl"
        scaler_path = Path("spg_dep") / "scaler.pkl"
        with model_path.open("rb") as f:
            model = pickle.load(f)
        with scaler_path.open("rb") as f:
            scaler = pickle.load(f)
        return model, scaler
    except Exception as e:
        # Return None, None but show friendly info in UI where relevant
        return None, None

model, scaler = load_model_and_scaler()

# -------------------------
# Try load dataset (for KPIs)
# -------------------------
data_df = None
try:
    csv_path = Path("spg_dep") / "solarpowergeneration.csv"
    if csv_path.exists():
        data_df = pd.read_csv(csv_path)
except Exception:
    data_df = None

# -------------------------
# Styling - Solar hybrid theme + Inter font
# -------------------------
st.markdown(""" 
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;500;700;900&display=swap" rel="stylesheet">
<style>
:root{
  --solar-yellow: #FFB703;
  --solar-orange: #FB8500;
  --deep-blue: #023E8A;
  --glass-bg: rgba(255,255,255,0.18);
  --glass-border: rgba(255,255,255,0.25);
  --glass-dark: rgba(20,20,25,0.28);
}

html, body, [class*="css"]  {
    font-family: "Inter", system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
}

/* Ensure sidebar is on top */
[data-testid="stSidebar"] {
    position: relative !important;
    z-index: 9999 !important;
}

/* App container pushed behind sidebar */
[data-testid="stAppViewContainer"] {
    z-index: 1 !important;
}

/* Background gradient full page (behind content) */
.bg-solar {
    position: fixed;
    inset: 0;
    background: linear-gradient(180deg, #fff8e6 0%, #fff3e0 40%, #eaf6ff 100%);
    z-index: 0;
    pointer-events: none;
}

/* Glass panels hybrid */
.glass {
    background: var(--glass-bg);
    border-radius: 14px;
    padding: 18px;
    border: 1px solid var(--glass-border);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    box-shadow: 0 6px 20px rgba(2, 46, 91, 0.06);
}

/* Dark-mode variations (applied with .dark classname) */
.dark .glass {
    background: linear-gradient(180deg, rgba(10,10,14,0.5), rgba(10,10,14,0.38));
    border: 1px solid rgba(255,255,255,0.06);
}

/* Header style */
.header-title {
    font-size: 40px;
    font-weight: 900;
    color: var(--deep-blue);
    letter-spacing: -1px;
    text-align: center;
    margin-bottom: 6px;
}

/* Solar subheading */
.header-sub {
    text-align: center;
    color: #2b4d77;
    margin-top: -6px;
    margin-bottom: 10px;
}

/* Floating solar panel */
.floating {
    animation: float 6s ease-in-out infinite;
    transform-origin: center;
}
@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-14px); }
    100% { transform: translateY(0px); }
}

/* KPI cards */
.kpi {
    padding: 18px;
    border-radius: 12px;
    background: linear-gradient(135deg, rgba(255,255,255,0.45), rgba(255,255,255,0.25));
    border: 1px solid rgba(255,255,255,0.3);
    text-align: center;
}
.kpi-title { font-size: 13px; color:#40577a; }
.kpi-value { font-size: 28px; font-weight:800; color:var(--solar-orange); }

/* Result box neon */
.result {
    padding: 20px;
    border-radius: 14px;
    font-weight: 800;
    font-size: 34px;
    text-align:center;
    color: #06283D;
    background: linear-gradient(90deg, rgba(255,240,230,0.9), rgba(255,250,240,0.85));
    border: 1px solid rgba(255,200,120,0.25);
    box-shadow: 0 10px 30px rgba(251,133,0,0.08);
}

/* Neon button */
.neon-btn {
    background: linear-gradient(90deg, var(--solar-orange), var(--solar-yellow));
    color: #072A3B !important;
    padding: 10px 18px;
    border-radius: 12px;
    font-weight: 700;
    border: none;
    box-shadow: 0 6px 20px rgba(251,133,0,0.18);
}
.neon-btn:hover { transform: translateY(-2px); transition: .15s; }

/* small helper */
.small-muted { color: #556B86; font-size:13px; }

/* dark mode root toggles (applied via .dark class on body wrapper) */
</style>
""", unsafe_allow_html=True)

# background div
st.markdown('<div class="bg-solar"></div>', unsafe_allow_html=True)

# -------------------------
# Top header with animated solar panel (svg inline)
# -------------------------
solar_svg = """
<svg width="120" height="120" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <g transform="translate(8,8)">
    <rect x="12" y="22" width="28" height="18" rx="2" ry="2" fill="#ffd166" stroke="#fb8500" stroke-width="0.8"/>
    <rect x="6" y="12" width="40" height="10" rx="2" ry="2" fill="#ffb703"/>
    <g transform="translate(18,18)">
      <rect x="3" y="2" width="20" height="6" fill="#023e8a" rx="1" ry="1"/>
    </g>
  </g>
</svg>
"""

st.markdown(f"""
<div style="display:flex; justify-content:center; align-items:center; gap:16px; margin-top:18px; margin-bottom:6px;">
  <div class="floating" style="width:110px; height:110px;">{solar_svg}</div>
  <div style="max-width:820px;">
    <div class="header-title">Solar Power Predictor</div>
    <div class="header-sub">Hybrid Solar Theme · Glass panels · Premium Dashboard</div>
  </div>
</div>
""", unsafe_allow_html=True)

# -------------------------
# Sidebar - enhanced
# -------------------------
with st.sidebar:
    st.markdown("---")
    st.markdown("<div style='font-weight:800; color:#06283D; font-size:16px;'>☀️ Solar Tools</div>", unsafe_allow_html=True)
    page = st.radio("", ["Prediction", "Dashboard (KPIs)", "EDA", "About"], index=0)
    st.markdown("---")
    st.markdown("Built: <small style='color:#6b778d;'>"+datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")+"</small>", unsafe_allow_html=True)
    # Dark mode toggle via session_state
    if 'dark' not in st.session_state:
        st.session_state['dark'] = False
    if st.button("Toggle Dark Mode"):
        st.session_state['dark'] = not st.session_state['dark']
    st.markdown("<div style='height:8px'></div>")
    st.markdown("<small class='small-muted'>Tip: Use the Toggle to switch page background.</small>", unsafe_allow_html=True)

# Apply dark mode wrapper if toggled (simple approach)
if st.session_state.get('dark', False):
    st.markdown("<div class='dark'>", unsafe_allow_html=True)
else:
    st.markdown("<div>", unsafe_allow_html=True)

# -------------------------
# Prediction page
# -------------------------
if page == "Prediction":
    st.write("")  # spacing
    # inputs in glass container
    st.markdown('<div class="glass" style="margin-bottom:14px;">', unsafe_allow_html=True)
    st.markdown("<div style='display:flex; gap:18px; flex-wrap:wrap;'>", unsafe_allow_html=True)

    temp = st.number_input("Temperature (°C)", min_value=-30.0, max_value=60.0, value=25.0, step=0.1)
    humidity = st.number_input("Humidity (%)", min_value=0.0, max_value=100.0, value=40.0, step=0.1)
    wind = st.number_input("Wind Speed (m/s)", min_value=0.0, max_value=40.0, value=5.0, step=0.1)

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Predict button & result
    col1, col2 = st.columns([1, 2])
    with col1:
        if st.button("🔮 Predict Power", key="predict_btn", help="Click to predict", ):
            if model is None or scaler is None:
                st.error("Model or scaler missing — please check logs or add model.pkl & scaler.pkl to spg_dep/")
            else:
                # Use DataFrame with matching column names to avoid warnings
                try:
                    input_df = pd.DataFrame([{
                        "Temperature": temp,
                        "Humidity": humidity,
                        "Wind Speed": wind
                    }])
                    scaled = scaler.transform(input_df)
                    pred = model.predict(scaled)[0]
                    st.session_state['last_pred'] = float(pred)
                except Exception as e:
                    st.error(f"Prediction failed: {e}")

    with col2:
        last = st.session_state.get('last_pred', None)
        if last is not None:
            st.markdown(f"<div class='result'>⚡ Estimated Power: {last:.2f} kW</div>", unsafe_allow_html=True)
        else:
            st.info("Enter inputs and press Predict. Prediction will appear here.", icon="ℹ️")

    # small explanation card
    st.markdown('<div class="glass" style="margin-top:16px;">', unsafe_allow_html=True)
    st.markdown("<strong>How it works</strong>")
    st.markdown("Model scales inputs with trained StandardScaler and predicts power using XGBoost model you trained.")
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# Dashboard (KPIs)
# -------------------------
elif page == "Dashboard (KPIs)":
    st.markdown('<div class="glass">', unsafe_allow_html=True)

    if data_df is not None:
        # compute KPIs intelligently if columns exist
        # fallback to sample aggregations
        try:
            # attempt to find sensible numeric columns
            numeric_cols = data_df.select_dtypes(include='number').columns.tolist()
            # create simple KPIs
            avg_power = data_df[numeric_cols[0]].mean() if numeric_cols else np.nan
            max_power = data_df[numeric_cols[0]].max() if numeric_cols else np.nan
            samples = len(data_df)
        except Exception:
            avg_power = np.nan
            max_power = np.nan
            samples = len(data_df)
    else:
        # mock values
        avg_power = 3.45
        max_power = 7.8
        samples = 1500

    k1, k2, k3 = st.columns(3)
    k1.markdown(f"<div class='kpi'><div class='kpi-title'>☀️ Avg Power (kW)</div><div class='kpi-value'>{avg_power:.2f}</div></div>", unsafe_allow_html=True)
    k2.markdown(f"<div class='kpi'><div class='kpi-title'>⚡ Max Power (kW)</div><div class='kpi-value'>{max_power:.2f}</div></div>", unsafe_allow_html=True)
    k3.markdown(f"<div class='kpi'><div class='kpi-title'>📊 Samples</div><div class='kpi-value'>{samples}</div></div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # add quick charts if data present
    if data_df is not None:
        st.markdown('<div class="glass" style="margin-top:12px;">', unsafe_allow_html=True)
        st.write("Quick preview of dataset:")
        st.dataframe(data_df.head(250))
        st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# EDA Page
# -------------------------
elif page == "EDA":
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown("### Upload dataset for EDA")
    uploaded = st.file_uploader("Upload CSV", type=["csv"])
    if uploaded is not None:
        try:
            df = pd.read_csv(uploaded)
            st.success(f"Loaded {len(df)} rows and {len(df.columns)} columns")
            st.dataframe(df.head(200))
            # basic distributions
            numeric = df.select_dtypes(include='number').columns.tolist()
            if numeric:
                col = st.selectbox("Plot numeric column", numeric)
                st.bar_chart(df[col].dropna().reset_index(drop=True).head(200))
        except Exception as e:
            st.error(f"Failed to parse CSV: {e}")
    else:
        st.info("No file uploaded. Use the dashboard or use the sample file in the repo.", icon="ℹ")

    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# About Page
# -------------------------
elif page == "About":
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown("## About this app")
    st.markdown("""
    - Theme: Solar Hybrid (glass panels + warm solar gradient)  
    - Features: Prediction (XGBoost model), Dashboard KPIs, EDA uploader  
    - Pro tip: Place `model.pkl` and `scaler.pkl` into `spg_dep/` in the repo root for the prediction to work.
    """)
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# Close dark wrapper
# -------------------------
st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# Footer small credits
# -------------------------
st.markdown("""
<div style="text-align:center; margin-top:18px;">
  <small style="color:#6b778d">Built by Abrar · UI: Solar Hybrid · Powered by Streamlit</small>
</div>
""", unsafe_allow_html=True)
