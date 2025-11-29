import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from lightgbm import LGBMRegressor


# -----------------------------------------------------
# DATA PREPARATION
# -----------------------------------------------------
def prepare_dataframe(df):
    df = df.copy()

    # Ensure timestamp exists
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.set_index("timestamp").sort_index()

    # Create missing weather columns if not present
    if "ghi" not in df.columns:
        df["ghi"] = 0
    if "temperature" not in df.columns:
        df["temperature"] = 25
    if "cloudcover" not in df.columns:
        df["cloudcover"] = 0.3

    # Time features
    df["hour"] = df.index.hour
    df["minute"] = df.index.minute
    df["minutes_of_day"] = df["hour"] * 60 + df["minute"]
    df["hour_sin"] = np.sin(2 * np.pi * df["minutes_of_day"] / 1440)
    df["hour_cos"] = np.cos(2 * np.pi * df["minutes_of_day"] / 1440)

    # Lag features (autoregression)
    for i in range(1, 5):
        df[f"lag_{i}"] = df["power_kw"].shift(i)

    df = df.dropna()
    return df


# -----------------------------------------------------
# TRAIN MODEL
# -----------------------------------------------------
def train_model(df, feature_cols):
    train, test = train_test_split(df, test_size=0.3, shuffle=False)

    X_train = train[feature_cols]
    y_train = train["power_kw"]
    X_test = test[feature_cols]
    y_test = test["power_kw"]

    model = LGBMRegressor(
        n_estimators=500,
        learning_rate=0.05,
        num_leaves=31,
        max_depth=-1
    )

    model.fit(X_train, y_train)

    preds_test = np.clip(model.predict(X_test), 0, None)

    mae = np.mean(np.abs(preds_test - y_test))
    rmse = np.sqrt(np.mean((preds_test - y_test) ** 2))

    return model, train, test, preds_test, mae, rmse


# -----------------------------------------------------
# 24-HOUR FORECAST USING AUTOREGRESSION
# -----------------------------------------------------
def forecast_next_24h(df, model, feature_cols, override_weather=None):
    """
    Generates 96-step (24h) forecast using:
    - autoregressive lags (lag_1..lag_4)
    - weather features (ghi, temp, cloudcover)
    - option to override weather with real Open-Meteo data
    """

    last_index = df.index.max()
    future_steps = 96

    future_index = pd.date_range(
        start=last_index + pd.Timedelta(minutes=15),
        periods=future_steps,
        freq="15min"
    )

    # Use real weather (Open-Meteo)
    if override_weather is not None:
        future_df = override_weather.copy()
        future_df = future_df.reindex(future_index).interpolate()

    else:
        # Synthetic fallback
        def synth_ghi(ts):
            h = ts.hour + ts.minute/60
            return max(0, np.sin((h - 6) * np.pi / 12)) * 800

        def synth_temp(ts):
            h = ts.hour + ts.minute/60
            return 20 + 8 * np.sin((h - 6) * np.pi / 12)

        cloud_base = df["cloudcover"].rolling(96, min_periods=1).mean().iloc[-1]
        rng = np.random.default_rng(42)

        future_df = pd.DataFrame(index=future_index)
        future_df["ghi"] = future_df.index.map(synth_ghi)
        future_df["temperature"] = future_df.index.map(synth_temp)
        future_df["cloudcover"] = np.clip(
            cloud_base + rng.normal(0, 0.05, len(future_df)), 0, 1
        )

    # Add time features
    future_df["hour"] = future_df.index.hour
    future_df["minute"] = future_df.index.minute
    future_df["minutes_of_day"] = future_df["hour"] * 60 + future_df["minute"]
    future_df["hour_sin"] = np.sin(2 * np.pi * future_df["minutes_of_day"] / 1440)
    future_df["hour_cos"] = np.cos(2 * np.pi * future_df["minutes_of_day"] / 1440)

    # Autoregressive loop
    last_lags = [df["power_kw"].iloc[-i] for i in range(1, 5)]
    lags = last_lags.copy()
    predictions = []

    for t in future_df.index:
        feat = {f"lag_{i}": lags[i-1] for i in range(1, 5)}
        feat.update({
            "hour_sin": future_df.loc[t, "hour_sin"],
            "hour_cos": future_df.loc[t, "hour_cos"],
            "ghi": future_df.loc[t, "ghi"],
            "temperature": future_df.loc[t, "temperature"],
            "cloudcover": future_df.loc[t, "cloudcover"],
        })

        x = np.array([feat[c] for c in feature_cols]).reshape(1, -1)
        pred = max(float(model.predict(x)[0]), 0)
        predictions.append(pred)

        lags = [pred] + lags[:-1]

    future_df["pred_power_kw"] = predictions
    return future_df
