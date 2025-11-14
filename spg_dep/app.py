import streamlit as st
import pickle
from streamlit.components.v1 import html
import os

st.markdown("""
<style>
/* Force sidebar above all page layers */
section[data-testid="stSidebar"] {
    position: relative !important;
    z-index: 10000 !important;   /* high so sidebar sits above floating art */
    pointer-events: auto !important; /* ensure it receives clicks */
}

/* Ensure app container sits behind sidebar visually */
[data-testid="stAppViewContainer"] {
    z-index: 1 !important;
}
</style>
""", unsafe_allow_html=True)

# Page configuration
st.set_page_config(page_title="Power Pred", page_icon="⚡",layout="wide")

st.markdown("""
<style>
[data-testid="stSidebar"] {
    display: block !important;
    visibility: visible !important;
}
</style>
""", unsafe_allow_html=True)

# Load Model & Scaler (cached, no UI inside)
# =========================================================
# ⚡ OPTIMIZED MODEL LOAD (WITH SINGLE TOAST)
# =========================================================

import streamlit as st
import pickle
import numpy as np

# ✅ Load Model & Scaler (cached — heavy ops only once per session)
@st.cache_resource(show_spinner=False)
def load_model_and_scaler():
    with open("spg_dep/model.pkl", "rb") as model_file:
        model = pickle.load(model_file)
    with open("spg_dep/scaler.pkl", "rb") as scaler_file:
        scaler = pickle.load(scaler_file)
    return model, scaler

# ✅ Load resources once
model, scaler = load_model_and_scaler()

# ✅ Show success toast only once per page load
if "model_loaded" not in st.session_state:
    st.session_state["model_loaded"] = True
    st.toast("✅ Model & Scaler loaded successfully!", icon="⚡")


# 2️⃣ GLOBAL STYLE


st.markdown("""
<style>
/* 🧨 Remove that top empty white container permanently */
#root > div:nth-child(1) > div.withScreencast > div > div.stAppViewContainer.appview-container.st-emotion-cache-1yiq2ps.e4man110 > div.st-emotion-cache-6px8kg.e4man1110 > section > div.stMainBlockContainer.block-container.st-emotion-cache-zy6yx3.e4man114 > div > div:nth-child(1) {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* 🌤️ Solar Glass Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(135deg,
        rgba(255, 249, 196, 0.25) 5%,       /* soft yellow tint */
        rgba(255, 224, 130, 0.20) 35%,      /* warm golden hue */
        rgba(189, 224, 254, 0.25) 90%) !important;  /* cool blue tint */
    backdrop-filter: blur(14px) !important;
    -webkit-backdrop-filter: blur(14px) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.25) !important;
    box-shadow: 6px 0 22px rgba(27, 73, 101, 0.10) !important;
    transition: all 0.4s ease-in-out;
}

/* 🩵 Sidebar Text + Widgets */
section[data-testid="stSidebar"] * {
    color: #1b4965 !important;
    font-family: 'Poppins', sans-serif !important;
    font-weight: 500 !important;
}

/* 🌫️ Light shimmer reflection effect (top-right) */
section[data-testid="stSidebar"]::before {
    content: "";
    position: absolute;
    top: 0;
    right: 0;
    width: 80%;
    height: 100%;
    background: radial-gradient(
        circle at top right,
        rgba(255, 255, 255, 0.3) 0%,
        rgba(255, 255, 255, 0.05) 40%,
        rgba(255, 255, 255, 0) 80%
    );
    pointer-events: none;
}

/* 🌈 Hover interactions (soft response, not flashy) */
section[data-testid="stSidebar"]:hover {
    box-shadow: 8px 0 26px rgba(27, 73, 101, 0.18) !important;
    background: linear-gradient(135deg,
        rgba(255, 249, 196, 0.28) 5%,
        rgba(255, 224, 130, 0.24) 35%,
        rgba(189, 224, 254, 0.28) 90%) !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* 🎯 Kill all known Streamlit sidebar collapse/expand buttons */
button[kind="headerNoPadding"],
div[data-testid="stSidebarCollapseButton"],
section[data-testid="stSidebar"] button[title*="Expand"],
section[data-testid="stSidebar"] button[title*="Collapse"],
section[data-testid="stSidebar"] button:has(svg),
section[data-testid="stSidebar"] svg {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
}

/* Also neutralize the parent wrapper that sometimes reflows */
section[data-testid="stSidebar"] > div:first-child {
    overflow: hidden !important;
}
</style>
""", unsafe_allow_html=True)

# 2️⃣ GLOBAL STYLE
st.markdown("""
<style>
/* 🌈 Global Base */
html, body, [class*="stApp"] {
    background: linear-gradient(to bottom right, #bde0fe 0%, #eaf6ff 100%);
    font-family: 'Poppins', sans-serif;
    transition: background 1.5s ease;
    color: #1b4965;
    overflow-x: hidden;
}

/* ✨ Font size globally increased */
h1, h2, h3, p, label, div {
    font-size: 1.05rem !important;
}
</style>
""", unsafe_allow_html=True)

# 4️⃣ ANIMATED BACKGROUND
st.markdown("""
<style>
/* 🌞 Aesthetic Sun */
.sun {
    position: fixed;
    top: -200px;
    right: -200px;
    width: 550px;
    height: 550px;
    background: radial-gradient(circle, #fff9c4 10%, #ffe082 45%, #fff3b0 70%, #ffec99 100%);
    border-radius: 50%;
    box-shadow: 0 0 180px 60px rgba(255, 245, 157, 0.6);
    z-index: 30;
    opacity: 0.9;
}

/* ☁️ Floating Clouds */
.cloud {
    position: fixed;
    background: #ffffffd0;
    border-radius: 50%;
    filter: blur(8px);
    animation: drift 50s linear infinite;
    z-index: 6;
}
.cloud1 { top: 150px; left: -200px; width: 200px; height: 90px; animation-delay: 0s; }
.cloud2 { top: 250px; left: -300px; width: 260px; height: 100px; animation-delay: 20s; }
.cloud3 { top: 180px; left: -400px; width: 240px; height: 100px; animation-delay: 40s; }
.cloud4 { top: 190px; left: -400px; width: 260px; height: 110px; animation-delay: 50s; }

@keyframes drift {
    from { transform: translateX(-250px); }
    to { transform: translateX(130vw); }
}

/* 🌫️ Smooth Title Animation */
.title {
    font-family: 'Poppins', sans-serif;
    font-size: 96px;
    font-weight: 800;
    color: #1b4965;
    text-align: center;
    padding-top: 160px;
    text-shadow: 4px 4px 25px rgba(0,0,0,0.15);
    letter-spacing: 1px;
    animation: fadeIn 2s ease-out;
}
.subtitle {
    text-align: center;
    color: #355070;
    font-size: 28px;
    font-weight: 500;
    margin-top: -10px;
    animation: fadeIn 3s ease-out;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
</style>

<!-- Inject the animated layers -->
<div class="sun"></div>
<div class="cloud cloud1"></div>
<div class="cloud cloud2"></div>
<div class="cloud cloud3"></div>
""", unsafe_allow_html=True)
st.markdown("""
<style>
/* ☀️ Predict Button – Sun Theme */
div.stButton > button {
    width: 100% !important;
    height: 65px !important;
    font-size: 1.2rem !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 12px !important;
    background: linear-gradient(135deg, #ffd166, #f6ae2d) !important;
    color: #1b4965 !important;
    box-shadow: 0px 4px 15px rgba(255, 196, 0, 0.4);
    transition: all 0.25s ease-in-out;
}
div.stButton > button:hover {
    transform: scale(1.03);
    box-shadow: 0px 6px 20px rgba(255, 196, 0, 0.6);
    background: linear-gradient(135deg, #ffe27a, #fcbf49) !important;
}

/* 🌤️ Output Box */
.power-box {
    background: linear-gradient(145deg, #ffffff, #f8fcff);
    border-radius: 16px;
    padding: 30px 25px 35px 25px;
    text-align: center;
    box-shadow: 0 8px 25px rgba(255, 220, 130, 0.25);
    border: 1px solid rgba(255, 220, 130, 0.4);
}
.power-box h1 {
    font-family: 'Poppins', sans-serif;
    color: #1b4965;
    font-weight: 700;
    margin-bottom: 0;
    text-shadow: 0px 0px 10px rgba(189,224,254,0.6);
}
.power-box span.unit {
    font-size: 1.3rem;
    color: #355070;
    font-weight: 500;
    margin-left: 5px;
}
.power-label {
    font-size: 1.2rem;
    color: #355070;
    font-weight: 500;
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* Kill top Streamlit padding + extra blank header zone */
div[data-testid="stDecoration"] {
    display: none !important;
}
header[data-testid="stHeader"] {
    display: none !important;
}
section.main > div:first-child {
    padding-top: 0rem !important;
    margin-top: -2rem !important;
}
div.block-container {
    padding-top: 0rem !important;
    margin-top: -2rem !important;
}
</style>
""", unsafe_allow_html=True)

#header
html("""
<!DOCTYPE html>
<html>
<head>
  <link href="https://fonts.googleapis.com/css2?family=Major+Mono+Display&family=Poppins:wght@300;400;500&display=swap" rel="stylesheet">
  <style>
    .header-wrapper {
      width: 100%;
      text-align: center;
      margin-top: 40px;
    }
    .header-container {
      font-family: 'Major Mono Display', monospace;
      font-size: 3.2rem;
      font-weight: 400;
      color: #1b4965;
      text-shadow: 2px 2px 10px rgba(0,0,0,0.1);
      line-height: 1.2;
      margin-bottom: 15px;
      letter-spacing: 1px;
      animation: fadeIn 1.5s ease-out;
    }
    .subtext {
      font-family: 'Poppins', sans-serif;
      color: #355070;
      font-size: 1.15rem;
      font-weight: 400;
      margin-bottom: 20px;
      letter-spacing: 0.5px;
      animation: fadeIn 2s ease-in;
    }
    .summary {
      font-family: 'Poppins', sans-serif;
      color: #5c677d;
      font-size: 1.05rem;
      font-weight: 400;
      text-align: center;
      width: 75%;
      margin: 0 auto;
      line-height: 1.55;
      letter-spacing: 0.3px;
      animation: fadeIn 2.8s ease-in;
    }
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(15px); }
      to { opacity: 1; transform: translateY(0); }
    }
  </style>
</head>
<body>
  <div class="header-wrapper">
    <div class="header-container">
      SOLAR POWER GENERATION<br>PREDICTOR
    </div>
    <div class="subtext">
      Predicts solar energy generation using environmental factors — powered by an optimized XGBoost regression model.
    </div>
    <div class="summary">
      Designed to emulate the behavior of solar energy systems, this model learns how weather and atmospheric variables impact power generation.<br>
      By analyzing complex interactions between sunlight, temperature, humidity, and sky coverage, it achieves highly accurate energy forecasts.<br>
      The result is a reliable, data-driven tool that transforms environmental readings into intelligent power predictions in real time.
    </div>
  </div>
</body>
</html>
""", height=350)



#solar panel image
## ==============================
# ☀️ SOLAR PANEL FRONT-LAYER FIX
# ==============================

import base64

# Encode your local PNG
st.markdown(f"""
<style>
  /* === Solar Panel Image === */
  .solar-panel {{
      position: fixed;
      bottom: 0;
      left: 0;
      width: 480px;
      height: auto;
      z-index: 50;  /* lowered so sidebar stays clickable and visible */
      pointer-events: none; /* still allows sidebar clicks */
      opacity: 0.97;
      filter: drop-shadow(0px 6px 14px rgba(0,0,0,0.25));
      animation: floaty 10s ease-in-out infinite alternate;
      transition: transform 0.5s ease-in-out, opacity 0.3s ease;
  }}

  /* ✨ Gentle floating motion */
  @keyframes floaty {{
      from {{ transform: translateY(0px); }}
      to {{ transform: translateY(-10px); }}
  }}

  /* Sidebar layer locked to prevent flicker */
  section[data-testid="stSidebar"] {{
      z-index: 10000 !important;  /* keep above solar panel */
      position: relative !important;
  }}

  /* Keep Streamlit container from clipping visuals */
  div[data-testid="stAppViewContainer"] {{
      overflow: visible !important;
  }}
</style>

<!-- Image injection -->
<img class="solar-panel" src="data:image/png;base64,{img_base64}" alt="Solar panel illustration">
""", unsafe_allow_html=True)

# =============================
# ==================== Custom CSS ====================
st.markdown("""
<style>
h3 {
    font-family: 'Poppins', sans-serif;
    font-weight: 600;
    letter-spacing: 0.5px;
}

/* Left block */
div[data-testid="stVerticalBlock"] > div:first-child {
    background: linear-gradient(145deg, #f9fbff, #e8f3ff);
    border-radius: 18px;
    padding: 30px 40px 35px 40px;
    box-shadow: 0 4px 14px rgba(91, 140, 167, 0.15);
    border: 1px solid rgba(255,255,255,0.3);
}

/* Blue slider + input aesthetics */
.stSlider label, .stNumberInput label, .stSelectSlider label {
    color: #1b4965 !important;
    font-weight: 500 !important;
}
.stSlider > div > div > div[role="slider"] {
    background-color: #4aa3d1 !important;
}
.stSlider > div > div > div[data-testid="stTickBar"] div {
    background-color: #a8dadc !important;
}
.stNumberInput input {
    background: rgba(255,255,255,0.85) !important;
    border: 1px solid rgba(90, 150, 190, 0.3) !important;
    border-radius: 8px !important;
    color: #1b4965 !important;
    text-align: center !important;
}

/* Prediction result block */
.prediction-box {
    background: linear-gradient(145deg, #f8fcff, #eaf6ff);
    border-radius: 18px;
    padding: 40px 25px;
    height: 420px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    box-shadow: 0 8px 22px rgba(27,73,101,0.12);
    border: 1px solid rgba(255,255,255,0.3);
}
.prediction-value {
    font-size: 3rem;
    font-weight: 800;
    color: #1b4965;
    text-shadow: 0 0 15px rgba(189,224,254,0.7);
}
.prediction-label {
    font-size: 1.2rem;
    color: #355070;
    font-weight: 500;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

# ==================== Layout ====================
col1, col2 = st.columns([7, 3], gap="large")

# ---- LEFT INPUTS ----
with col1:
    st.markdown("### 🌤️ Enter Environmental Parameters")

    colL, colR = st.columns(2, gap="medium")

    with colL:
        distance_to_solar_noon = st.slider(
            "Distance to Solar Noon (radians)", 
            min_value=0.0, max_value=3.14, value=1.5, step=0.01
        )
        temperature = st.number_input(
            "Temperature (°C)", 
            min_value=-10.0, max_value=60.0, value=25.0, step=0.5
        )
        sky_cover = st.select_slider(
            "Sky Cover (0 = Clear, 4 = Covered)", 
            options=[0, 1, 2, 3, 4], value=2
        )

    with colR:
        visibility = st.slider(
            "Visibility (km)", 
            min_value=0.0, max_value=50.0, value=20.0, step=0.5
        )
        humidity = st.slider(
            "Humidity (%)", 
            min_value=0, max_value=100, value=50, step=1
        )
        wind_speed = st.number_input(
            "Wind Speed (m/s)", 
            min_value=0.0, max_value=25.0, value=5.0, step=0.1
        )

# ---- RIGHT PREDICTION PANEL ----
with col2:
    # Prepare features for prediction
    features = np.array([[distance_to_solar_noon, temperature, sky_cover, visibility, humidity, wind_speed]])
    scaled_input = scaler.transform(features)

    # ☀️ Predict button (sun theme)
    predict_button = st.button("☀️ Generate Power", use_container_width=True)

    # 🌤️ Output Box
    if predict_button:
        try:
            prediction = model.predict(scaled_input)[0]
            prediction_str = f"{prediction:.2f}"
            st.markdown(f"""
<div class="power-box">
  <div class="power-label">🌤️ Power Generated</div>
  <div style="
        display:flex;
        justify-content:center;
        align-items:flex-start;
        gap:8px;
        line-height:1;
        margin-top:20px;">
    <span style="
          font-family:'Major Mono Display', monospace;
          font-weight:300;
          color:#1b4965;
          font-size:6rem;
          text-shadow:2px 2px 15px rgba(0,0,0,0.15);">
          {prediction_str}
    </span>
    <span style="
          font-family:'Poppins', sans-serif;
          color:#355070;
          font-size:3rem;
          margin-top:25px;">
          kW
    </span>
  </div>
</div>
""", unsafe_allow_html=True)

          
        except Exception as e:
            st.error(f"Prediction failed: {e}")
    else:
        st.markdown("""
            <div class="power-box">
                <div class="power-label">🌤️ Power Generated</div>
                <h1>--<span class="unit">kW</span></h1>
            </div>
        """, unsafe_allow_html=True)

# =========================================================
# ✨ Adjusted Animated Footer (centered perfectly with sidebar)
# =========================================================
st.markdown("""
<style>
/* 🌤️ Footer base */
.footer-wrapper {
    position: fixed;
    bottom: 25px;
    left: -60px; /* 👈 nudged ~1 inch left to counter sidebar width */
    width: 100%;
    text-align: center;
    font-family: 'Poppins', sans-serif;
    font-size: 0.95rem;
    color: #355070;
    opacity: 0;
    letter-spacing: 0.6px;
    animation: fadeUp 2.8s ease-out 2.5s forwards; /* soft delayed intro */
}

/* ✨ Link styling */
.footer-wrapper a {
    color: #1b4965;
    text-decoration: none;
    font-weight: 600;
    transition: all 0.3s ease;
}
.footer-wrapper a:hover {
    color: #f6ae2d;
    text-shadow: 0px 0px 8px rgba(255, 214, 102, 0.4);
}

/* 🌈 Soft fade-up animation */
@keyframes fadeUp {
    0%   { opacity: 0; transform: translateY(25px); }
    60%  { opacity: 0.5; transform: translateY(10px); }
    100% { opacity: 1; transform: translateY(0); }
}
</style>

<div class="footer-wrapper">
  By: <b>Abrar Waseem</b> | 
  <a href="https://github.com/Guynotknown" target="_blank">github.com/Guynotknown</a>
</div>
""", unsafe_allow_html=True)







