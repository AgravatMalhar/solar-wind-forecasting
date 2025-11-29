

import streamlit as st
import pandas as pd
import os

st.markdown("<div class='page-title'>Upload SCADA Data</div>", unsafe_allow_html=True)

from utils.model_utils import prepare_dataframe, train_model
import matplotlib.pyplot as plt

DATA_FILE = "data/uploaded_data.csv"

st.title("⚙️ Train Forecast Model")

def start_container():
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)

def end_container():
    st.markdown("</div>", unsafe_allow_html=True)

def divider():
    st.markdown("<div class='hr-line'></div>", unsafe_allow_html=True)



if not os.path.exists(DATA_FILE):
    st.error("No data found. Upload a file first.")
    st.stop()

df = pd.read_csv(DATA_FILE)
st.write("Loaded Data:")
st.dataframe(df.head())

df_prepared = prepare_dataframe(df)
st.write("Prepared Data:")
st.dataframe(df_prepared.head())

feature_cols = [
    'lag_1','lag_2','lag_3','lag_4',
    'hour_sin','hour_cos',
    'ghi','temperature','cloudcover'
]

if st.button("Train Model"):
    with st.spinner("Training..."):
        model, train, test, preds_test, mae, rmse = train_model(df_prepared, feature_cols)

    st.success(f"Model trained. MAE={mae:.3f} kW | RMSE={rmse:.3f} kW")

    col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f'<div class="metric-card"><h3>MAE</h3><h2>{mae:.3f}</h2></div>', unsafe_allow_html=True)

with col2:
    st.markdown(f'<div class="metric-card"><h3>RMSE</h3><h2>{rmse:.3f}</h2></div>', unsafe_allow_html=True)

with col3:
    st.markdown(f'<div class="metric-card"><h3>Train Samples</h3><h2>{len(train)}</h2></div>', unsafe_allow_html=True)


    fig, ax = plt.subplots(figsize=(15,5))
    ax.plot(test.index, test["power_kw"], label="Actual")
    ax.plot(test.index, preds_test, label="Predicted")
    ax.legend(); ax.grid(True)
    st.pyplot(fig)

    # Save model in session_state
    st.session_state["df_prepared"] = df_prepared
    st.session_state["model"] = model
    st.session_state["feature_cols"] = feature_cols

    st.info("Model is ready. Go to Forecast page.")

end_container()
