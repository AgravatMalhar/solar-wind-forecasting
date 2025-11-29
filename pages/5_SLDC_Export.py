

import streamlit as st
st.markdown("<div class='page-title'>Upload SCADA Data</div>", unsafe_allow_html=True)


from utils.sldc_utils import to_sldc_96
import pandas as pd
import io

st.title("📊 SLDC Export")

def start_container():
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)

def end_container():
    st.markdown("</div>", unsafe_allow_html=True)

def divider():
    st.markdown("<div class='hr-line'></div>", unsafe_allow_html=True)



if "future_df" not in st.session_state:
    st.error("Run forecast first.")
    st.stop()

future_df = st.session_state["future_df"]
sldc_df = to_sldc_96(future_df)

st.write("Preview:")
st.dataframe(sldc_df.head())

excel_buffer = io.BytesIO()
with pd.ExcelWriter(excel_buffer, engine="xlsxwriter") as writer:
    sldc_df.to_excel(writer, index=False, sheet_name="SLDC_96")

st.download_button(
    "Download SLDC Excel",
    data=excel_buffer.getvalue(),
    file_name="sldc_96_forecast.xlsx"
)

end_container()
