import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

def app():
    st.title("🌍 GFRI Map View")

    df = pd.read_csv("datasets/merged_data.csv")
    df = df.dropna(subset=["Lat", "Lon"])

    metric_labels = {
        "GDP per Capita": "GDP",
        "Human Development Index": "HDI",
        "Internet Usage by Population (%)": "Internet",
        "Employment in Agriculture (%)": "Agri",
    }

    selected_label = st.selectbox("Select Metric", list(metric_labels.keys()))

    metric = metric_labels[selected_label]

    year = st.slider(
        "Select Year",
        int(df["Year"].min()),
        int(df["Year"].max()),
        int(df["Year"].max())
    )

    df_year = df[df["Year"] == year]

    m = folium.Map(location=[20, 0], zoom_start=2, tiles="CartoDB dark_matter")
    for _, row in df_year.iterrows():
        folium.CircleMarker(
            location=[row["Lat"], row["Lon"]],
            radius=4,
            popup=f"{row['Entity']}: {selected_label} = {row[metric]}",
            color="#C2C2C2",
            fill=True,
            fill_color="#C2C2C2",
            fill_opacity=0.4
        ).add_to(m)

    st_folium(m, width=1200)