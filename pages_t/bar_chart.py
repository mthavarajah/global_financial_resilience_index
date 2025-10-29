import streamlit as st
import pandas as pd
import plotly.express as px

def app():
    st.title("📊 GFRI Bar Chart")

    # Load dataset
    df = pd.read_csv("datasets/merged_data.csv")

    # UI Controls
    year = st.slider("Select Year", int(df['Year'].min()), int(df['Year'].max()), int(df['Year'].min()))
    countries = st.multiselect("Select Countries", df['Entity'].unique(), default=["Canada", "United States"])
    metric = st.selectbox("Select Metric", ["GDP", "HDI", "Internet", "Agri", "Poverty"])

    # Filter data
    df_filtered = df[(df['Entity'].isin(countries)) & (df['Year'] == year)]

    # Plot
    fig = px.bar(df_filtered, x='Entity', y=metric, color=metric,
                 title=f"{metric} by Country in {year}")
    st.plotly_chart(fig, use_container_width=True)