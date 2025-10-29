import streamlit as st
from pages_t import map_view, line_chart, bar_chart, data_table, ml_dashboard

st.set_page_config(page_title="Global Financial Resilience Index", layout="wide")

st.sidebar.title("🌍 Global Financial Resilience Index (GFRI)")
page = st.sidebar.radio(
    "Navigate", 
    ["Map View", "Line Chart", "Bar Chart", "Data Table", "Financial Resilience Index"]
)

if page == "Map View":
    map_view.app()
elif page == "Line Chart":
    line_chart.app()
elif page == "Bar Chart":
    bar_chart.app()
elif page == "Data Table":
    data_table.app()
elif page == "Financial Resilience Index":
    ml_dashboard.app()