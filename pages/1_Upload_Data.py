

import streamlit as st
import pandas as pd
import os
st.markdown("<div class='page-title'>Upload SCADA Data</div>", unsafe_allow_html=True)

DATA_DIR = "data"

st.title("📄 Upload SCADA + Weather Data")

def start_container():
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)

def end_container():
    st.markdown("</div>", unsafe_allow_html=True)

def divider():
    st.markdown("<div class='hr-line'></div>", unsafe_allow_html=True)



st.markdown("""
Upload your CSV file containing:

- `timestamp`
- `power_kw`
Optional:
- `ghi`, `temperature`, `cloudcover`
""")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    st.write("Preview:")
    st.dataframe(df.head())

    # save to data directory
    os.makedirs(DATA_DIR, exist_ok=True)
    save_path = os.path.join(DATA_DIR, "uploaded_data.csv")
    df.to_csv(save_path, index=False)

    st.success(f"File saved to {save_path}")

    st.info("You can now go to the **Train Model** page.")

end_container()
