

import streamlit as st
st.markdown("<div class='page-title'>Upload SCADA Data</div>", unsafe_allow_html=True)


from utils.weather_api import test_open_meteo

st.title("🌤️ Weather API Settings")

def start_container():
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)

def end_container():
    st.markdown("</div>", unsafe_allow_html=True)

def divider():
    st.markdown("<div class='hr-line'></div>", unsafe_allow_html=True)


st.markdown("Configure Open-Meteo forecast location.")

lat = st.number_input("Latitude", value=22.5)
lon = st.number_input("Longitude", value=72.5)

if st.button("Test Weather API"):
    df = test_open_meteo(lat, lon)
    st.dataframe(df.head())
    st.success("Weather API working!")

st.session_state["lat"] = lat
st.session_state["lon"] = lon

end_container()
