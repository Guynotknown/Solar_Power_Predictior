import streamlit as st
import base64
import os
# Correct base path to images folder
IMAGE_DIR = os.path.join(os.path.dirname(__file__), "..", "images")
# ==========================
# PAGE CONFIG
# ==========================
st.set_page_config(page_title="🌌 EDA Dashboard", page_icon="🌙", layout="wide")

# ==========================
# STYLE
# ==========================
st.markdown("""
<style>
html, body, [class*="stApp"] {
    background: radial-gradient(circle at top, #0b132b 0%, #1c2541 40%, #3a506b 100%);
    color: #e0e7ff !important;
    font-family: 'Poppins', sans-serif;
    overflow-x: hidden;
}

/* ✨ Header */
h2 {
    color: #d6e4ff !important;
    text-shadow: 0 0 15px rgba(120,180,255,0.35);
}
p.subtext {
    color: #a7c7e7;
    font-size: 1rem;
}

/* 🌠 Stars Animation */
@keyframes twinkle {
    0%,100% { opacity: 0.3; }
    50% { opacity: 1; }
}
.star {
    position: fixed;
    background: white;
    border-radius: 50%;
    opacity: 0.8;
    animation: twinkle 2.5s infinite ease-in-out;
    z-index: 0;
}
.star:nth-child(1) { top: 8%; left: 15%; width: 2px; height: 2px; animation-delay: 0s; }
.star:nth-child(2) { top: 30%; left: 50%; width: 3px; height: 3px; animation-delay: 1s; }
.star:nth-child(3) { top: 70%; left: 65%; width: 2px; height: 2px; animation-delay: 1.5s; }
.star:nth-child(4) { top: 20%; left: 80%; width: 4px; height: 4px; animation-delay: 0.5s; }
.star:nth-child(5) { top: 85%; left: 25%; width: 3px; height: 3px; animation-delay: 2s; }

/* 🪩 Glassy Cards */
.card {
    background: rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 20px 25px;
    margin: 25px 0;
    box-shadow: 0 0 25px rgba(120,180,255,0.12);
    border: 1px solid rgba(255,255,255,0.15);
    backdrop-filter: blur(6px);
    opacity: 0;
    transform: translateY(40px);
    animation: fadeInUp 1.4s forwards;
}

/* 🎞️ Fade In Scroll Effect */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(40px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Staggered entry timing for cards */
.card:nth-of-type(1) { animation-delay: 0.2s; }
.card:nth-of-type(2) { animation-delay: 0.4s; }
.card:nth-of-type(3) { animation-delay: 0.6s; }
.card:nth-of-type(4) { animation-delay: 0.8s; }
.card:nth-of-type(5) { animation-delay: 1.0s; }
.card:nth-of-type(6) { animation-delay: 1.2s; }

.card img {
    border-radius: 10px;
    width: 90%;
    display: block;
    margin: 0 auto 10px auto;
    box-shadow: 0 0 12px rgba(120,180,255,0.15);
    animation: fadeInUp 1.5s forwards;
}

/* 🌙 Caption fade (slightly later than image) */
.card p {
    text-align: center;
    color: #a7c7e7;
    font-size: 0.95rem;
    opacity: 0;
    transform: translateY(15px);
    animation: fadeInUp 1.2s forwards;
}
.card:nth-of-type(1) p { animation-delay: 0.6s; }
.card:nth-of-type(2) p { animation-delay: 0.8s; }
.card:nth-of-type(3) p { animation-delay: 1.0s; }
.card:nth-of-type(4) p { animation-delay: 1.2s; }
.card:nth-of-type(5) p { animation-delay: 1.4s; }
.card:nth-of-type(6) p { animation-delay: 1.6s; }

/* 🧭 Download Container */
.download-box {
    display: flex;
    justify-content: center;
    align-items: center;
    background: rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 25px;
    width: 250px;
    height: 130px;
    box-shadow: 0 0 25px rgba(120,180,255,0.12);
    border: 1px solid rgba(255,255,255,0.15);
    backdrop-filter: blur(6px);
    text-align: center;
    transition: 0.3s ease-in-out;
    cursor: pointer;
    opacity: 0;
    transform: translateY(30px);
    animation: fadeInUp 1.5s forwards;
}
.download-box:hover {
    transform: scale(1.05);
    box-shadow: 0 0 30px rgba(120,180,255,0.25);
}
.download-icon {
    font-size: 3rem;
    margin-bottom: 10px;
}
.download-text {
    color: #e0e7ff;
    font-size: 1rem;
}
.download-box:nth-of-type(1) { animation-delay: 1.4s; }
.download-box:nth-of-type(2) { animation-delay: 1.6s; }
</style>

<!-- Stars Background -->
<div class="star"></div>
<div class="star"></div>
<div class="star"></div>
<div class="star"></div>
<div class="star"></div>
""", unsafe_allow_html=True)

# ==========================
# HEADER
# ==========================
st.markdown("<h2> Exploratory Data Analysis</h2>", unsafe_allow_html=True)
st.markdown("<p class='subtext'>A reflective view of data patterns and model insights — illuminated in the quiet of the night.</p>", unsafe_allow_html=True)

# ==========================
# IMAGE CONTAINERS
# ==========================
plots = [
    ("heatmap.png", " Correlation Heatmap — Visualizing feature interdependence."),
    ("variable_corr.png", " Feature–Target Correlation — How each parameter affects power output."),
    ("reg_line.png", " predicted vs actual — Understanding model prediction spread."),
    ("model_comparison.png", "🪐 Model Comparison Map — Evaluating each algorithm's accuracy."),
    ("faeature_imp.png", "importance of each feature — Multi-feature comparison."),
    ("residual.png", "histplot — Compact overview of results and accuracy.")
]

for img, caption in plots:
    st.markdown(f"<div class='card'>", unsafe_allow_html=True)

    img_path = os.path.join(IMAGE_DIR, img)

    if os.path.exists(img_path):
        st.image(img_path, use_container_width=False, width=700)
    else:
        st.warning(f"Image '{img_path}' not found.")

    st.markdown(f"<p>{caption}</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================
# DOWNLOAD SECTION
# ==========================
st.markdown("<h3 style='margin-top:50px;'>📥 Downloads</h3>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

def download_button(file_path, label, icon):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
        href = f'<a href="data:file/txt;base64,{b64}" download="{os.path.basename(file_path)}" style="text-decoration:none;"><div class="download-box"><div class="download-icon">{icon}</div><div class="download-text">{label}</div></div></a>'
        st.markdown(href, unsafe_allow_html=True)
    else:
        st.warning(f"⚠️ {file_path} not found.")

with col1:
    download_button("solarpowergeneration.csv", "Download Dataset", "📁")
with col2:
    download_button("SPG_Model.ipynb", "Download Notebook", "💻")

