import pandas as pd


def to_sldc_96(df):
    """
    Convert forecast dataframe into SLDC 96-block format.
    """

    out = pd.DataFrame({
        "timestamp": df.index,
        "interval": range(1, 97),
        "schedule_date": df.index.date,
        "forecast_MW": df["pred_power_kw"] / 1000,
        "plant_code": "PLANT001"
    })

    return out
