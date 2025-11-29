import requests
import pandas as pd


def fetch_open_meteo_forecast(lat, lon):
    """
    Fetch 24h weather forecast (15-min interpolated) from Open-Meteo API.
    """

    url = (
        "https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        "&hourly=shortwave_radiation,temperature_2m,cloudcover"
        "&timezone=auto"
    )

    r = requests.get(url).json()

    df = pd.DataFrame({
        "timestamp": r["hourly"]["time"],
        "ghi": r["hourly"]["shortwave_radiation"],
        "temperature": r["hourly"]["temperature_2m"],
        "cloudcover": [c/100 for c in r["hourly"]["cloudcover"]],
    })

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.set_index("timestamp")

    # Convert hourly → 15-min interpolated
    df = df.resample("15min").interpolate()

    return df.head(96)


def test_open_meteo(lat, lon):
    """
    Small test request to verify API connection.
    """
    return fetch_open_meteo_forecast(lat, lon)
