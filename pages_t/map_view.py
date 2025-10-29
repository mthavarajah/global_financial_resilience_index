import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

def app():
    st.title("🌍 GFRI Map View")

    df = pd.read_csv("datasets/merged_data.csv")

    df = df.dropna(subset=["Lat", "Lon"])

    metric = st.selectbox("Select Metric", ["GDP", "HDI", "Internet", "Agri", "Poverty"])
    year = st.slider("Select Year", int(df['Year'].min()), int(df['Year'].max()), int(df['Year'].max()))

    df_year = df[df["Year"] == year]

    m = folium.Map(location=[20,0], zoom_start=2, tiles="CartoDB dark_matter")
    for _, row in df_year.iterrows():
        folium.CircleMarker(
            location=[row["Lat"], row["Lon"]],
            radius=4,
            popup=f"{row['Entity']}: {metric} = {row[metric]}",
            color="#C2C2C2",
            fill=True,
            fill_color="#C2C2C2",
            fill_opacity=0.4
        ).add_to(m)

    st_folium(m, width=1200)