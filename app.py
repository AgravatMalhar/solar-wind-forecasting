# app.py - shim to run your real home page
import streamlit as st

# This sets the sidebar label — MUST come first.
st.set_page_config(page_title="GridSight")
st.title("Home")   # ← THIS NAME WILL SHOW IN SIDEBAR INSTEAD OF "app"

import runpy
runpy.run_path("0_GridSight.py", run_name="__main__")

