import streamlit as st

import matplotlib.pyplot as plt
plt.style.use("seaborn-v0_8-darkgrid")
def divider():
    st.markdown("<hr style='border: 1px solid #333;'>", unsafe_allow_html=True)


st.set_page_config(
    page_title="Solar & Wind Forecasting",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Global CSS
st.markdown("""
<style>

html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
}

/* MAIN PAGE WRAPPER */
.main-container {
    background-color: #0F0F0F;
    padding: 25px 30px;
    border-radius: 12px;
    border: 1px solid #2a2a2a;
    margin-top: 15px;
}

/* PAGE TITLES */
.page-title {
    font-size: 34px;
    font-weight: 700;
    margin-bottom: 10px;
    color: #fafafa;
}

/* SECTION TITLES */
.section-title {
    font-size: 22px;
    margin-top: 25px;
    margin-bottom: 8px;
    font-weight: 600;
    color: #dddddd;
}

/* METRIC CARDS */
.metric-card {
    padding: 22px;
    border-radius: 12px;
    background-color: #1A1A1A;
    border: 1px solid #333333;
    text-align: center;
    transition: all 0.25s ease;
}

.metric-card:hover {
    transform: translateY(-3px) scale(1.02);
    border-color: #4dd2ff;
    box-shadow: 0px 0px 25px rgba(77, 210, 255, 0.15);
}

/* METRIC CARD TEXT */
.metric-card h3 {
    color: #A8A8A8;
    margin-bottom: 5px;
    font-weight: 500;
}

.metric-card h2 {
    color: #ffffff;
    margin: 0;
    font-size: 30px;
    font-weight: 600;
}

/* CLEAN DIVIDER */
.hr-line {
    border-top: 1px solid #2a2a2a;
    margin: 25px 0;
}

/* TABLE HOVER */
tbody tr:hover {
    background-color: #222 !important;
}

</style>
""", unsafe_allow_html=True)

def start_container():
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)

def end_container():
    st.markdown("</div>", unsafe_allow_html=True)

def divider():
    st.markdown("<div class='hr-line'></div>", unsafe_allow_html=True)


import streamlit as st
import os

st.set_page_config(page_title="Renewable Forecasting Prototype",
                   layout="wide",
                   initial_sidebar_state="expanded")

st.sidebar.success("Select a page from the left.")

st.title("⚡ Renewable Generation Forecasting – Prototype")

st.markdown("""
Welcome to the multi-page forecasting dashboard.

### Features:
- Upload SCADA + Weather data
- Train a forecasting model
- Configure weather APIs
- Generate 24-hour forecasts
- Export SLDC 96-block schedules

Use the sidebar to begin.
""")
