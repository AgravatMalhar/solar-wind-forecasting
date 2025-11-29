import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

from utils.model_utils import prepare_dataframe, train_model

st.markdown("<div class='page-title'>Train Forecast Model</div>", unsafe_allow_html=True)

DATA_FILE = "data/uploaded_data.csv"

# -------------------------
# UTILITY UI FUNCTIONS
# -------------------------
def start_container():
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)

def end_container():
    st.markdown("</div>", unsafe_allow_html=True)


# -------------------------
# CHECK IF DATA EXISTS
# -------------------------
if not os.path.exists(DATA_FILE):
    st.error("No data found. Please upload a file in the Upload page.")
    st.stop()

df = pd.read_csv(DATA_FILE)
st.write("Loaded Data:")
st.dataframe(df.head())

# -------------------------
# PREPARE DATA
# -------------------------
df_prepared = prepare_dataframe(df)
st.write("Prepared Data:")
st.dataframe(df_prepared.head())

feature_cols = [
    "lag_1", "lag_2", "lag_3", "lag_4",
    "hour_sin", "hour_cos",
    "ghi", "temperature", "cloudcover"
]

# -------------------------
# TRAIN MODEL
# -------------------------
start_container()

train_button = st.button("Train Model", key="train_model_button")

if train_button:

    with st.spinner("Training model..."):
        model, train, test, preds_test, mae, rmse = train_model(df_prepared, feature_cols)

    st.success(f"Model trained successfully!")

    # -------------------------
    # METRIC CARDS (3 columns)
    # -------------------------
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f'<div class="metric-card"><h3>MAE</h3><h2>{mae:.3f}</h2></div>',
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f'<div class="metric-card"><h3>RMSE</h3><h2>{rmse:.3f}</h2></div>',
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f'<div class="metric-card"><h3>Train Samples</h3><h2>{len(train)}</h2></div>',
            unsafe_allow_html=True
        )

    # -------------------------
    # PLOT ACTUAL VS PREDICTED
    # -------------------------
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(test.index, test["power_kw"], label="Actual", marker="o")
    ax.plot(test.index, preds_test, label="Predicted", marker="x")
    ax.set_title("Actual vs Predicted (Test Set)")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)

    # -------------------------
    # STORE MODEL IN SESSION
    # -------------------------
    st.session_state["df_prepared"] = df_prepared
    st.session_state["model"] = model
    st.session_state["feature_cols"] = feature_cols

    st.info("Model ready! Proceed to the 24h Forecast page.")

end_container()
