import streamlit as st
import pandas as pd
import plotly.express as px

def app():
    st.title("📈 GFRI Line Chart")

    df = pd.read_csv("datasets/merged_data.csv")

    metric_labels = {
        "GDP per Capita": "GDP",
        "Human Development Index": "HDI",
        "Internet": "Internet",
        "Agriculture": "Agri",
    }

    countries = st.multiselect("Select Countries", df['Entity'].unique(), default=["Canada", "United States"])
    selected_label = st.selectbox("Select Metric", list(metric_labels.keys()))
    metric = metric_labels[selected_label]

    years = st.slider(
        "Select Year Range",
        int(df['Year'].min()),
        int(df['Year'].max()),
        (int(df['Year'].min()), int(df['Year'].max()))
    )

    df_filtered = df[
        (df['Entity'].isin(countries)) &
        (df['Year'] >= years[0]) &
        (df['Year'] <= years[1])
    ]

    fig = px.line(
        df_filtered,
        x='Year',
        y=metric,
        color='Entity',
        markers=True,
        title=f"{selected_label} Trends ({years[0]}–{years[1]})"
    )
    st.plotly_chart(fig, use_container_width=True)