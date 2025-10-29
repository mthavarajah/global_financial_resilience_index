import streamlit as st
import pandas as pd
import plotly.express as px

def app():
    st.title("📈 GFRI Line Chart")

    df = pd.read_csv("datasets/merged_data.csv")

    countries = st.multiselect("Select Countries", df['Entity'].unique(), default=["Canada", "United States"])
    metric = st.selectbox("Select Metric", ["GDP", "HDI", "Internet", "Agri", "Poverty"])
    years = st.slider("Select Year Range",
                      int(df['Year'].min()), int(df['Year'].max()),
                      (int(df['Year'].min()), int(df['Year'].max())))

    df_filtered = df[(df['Entity'].isin(countries)) &
                     (df['Year'] >= years[0]) &
                     (df['Year'] <= years[1])]

    fig = px.line(df_filtered, x='Year', y=metric, color='Entity', markers=True,
                  title=f"{metric} Trends ({years[0]}–{years[1]})")
    st.plotly_chart(fig, use_container_width=True)