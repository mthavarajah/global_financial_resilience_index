import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from ml_models.regression_model import FRIRegressionModel

def app():
    @st.cache_data(show_spinner=True)
    def load_model():
        reg_model = FRIRegressionModel()
        return reg_model

    reg_model = load_model()

    df = pd.read_csv("datasets/merged_data.csv")
    df = df.dropna(subset=["Lat", "Lon"])

    st.title("📊 Financial Resilience Index (FRI)")

    countries = st.multiselect(
        "Select Countries", 
        df['Entity'].unique(), 
        default=["Canada", "United States"]
    )
    year = st.slider(
        "Select Year", 
        int(df['Year'].min()), 
        int(df['Year'].max()), 
        int(df['Year'].max())
    )

    df_input = df[(df['Entity'].isin(countries)) & (df['Year'] == year)]

    st.subheader("Financial Resilience Index (FRI) Score")

    X_reg = df_input[reg_model.features]
    preds = reg_model.predict(X_reg)
    df_input["Predicted_FRI"] = np.round(preds, 3)

    display_cols = ["Entity", "Year"]
    if "FRI" in df_input.columns:
        display_cols.append("FRI")
    display_cols.append("Predicted_FRI")
    st.dataframe(df_input[display_cols])

    fig = px.bar(
        df_input, 
        x="Entity", 
        y="Predicted_FRI", 
        color="Predicted_FRI",
        color_continuous_scale="RdYlGn",
        text="Predicted_FRI"
    )
    st.plotly_chart(fig, use_container_width=True)