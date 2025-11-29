

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
st.markdown("<div class='page-title'>Upload SCADA Data</div>", unsafe_allow_html=True)

from utils.weather_api import fetch_open_meteo_forecast
from utils.model_utils import forecast_next_24h

st.title("🔮 24-Hour Forecast")

def start_container():
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)

def end_container():
    st.markdown("</div>", unsafe_allow_html=True)

def divider():
    st.markdown("<div class='hr-line'></div>", unsafe_allow_html=True)



if "model" not in st.session_state:
    st.error("Train the model first.")
    st.stop()

model = st.session_state["model"]
df_prepared = st.session_state["df_prepared"]
feature_cols = st.session_state["feature_cols"]

lat = st.session_state.get("lat", 22.5)
lon = st.session_state.get("lon", 72.5)

weather_df = fetch_open_meteo_forecast(lat, lon)

st.write("Next 24h Weather Forecast:")
st.dataframe(weather_df.head())

future_df = forecast_next_24h(df_prepared, model, feature_cols, override_weather=weather_df)

st.subheader("Predicted Power (Next 24 Hours)")
st.dataframe(future_df[['pred_power_kw']].head())

fig, ax = plt.subplots(figsize=(15,5))
ax.plot(future_df['pred_power_kw'])
ax.set_title("Next 24h Forecast"); ax.grid(True)
st.pyplot(fig)

st.session_state["future_df"] = future_df

end_container()
