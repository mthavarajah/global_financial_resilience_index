import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import plotly.express as px

def calculate_trend_slope(x, y):
    if len(x) < 2:
        return 0
    model = LinearRegression()
    model.fit(np.array(x).reshape(-1, 1), np.array(y))
    return model.coef_[0]

def app():
    st.title("📋 GFRI Data Table")

    df = pd.read_csv("datasets/merged_data.csv")

    metric_labels = {
        "GDP per Capita": "GDP",
        "Human Development Index": "HDI",
        "Internet": "Internet",
        "Agriculture": "Agri",
    }

    countries = st.multiselect("Select Countries", df['Entity'].unique(), 
                               default=["Canada", "United States"])
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

    summary_list = []
    for country in countries:
        df_country = df_filtered[df_filtered['Entity'] == country]
        values = df_country[metric].values
        years_arr = df_country['Year'].values

        if len(values) == 0:
            continue

        first = values[0]
        last = values[-1]
        change = last - first
        pct_change = (change / first) * 100 if first != 0 else np.nan
        mean = np.mean(values)
        median = np.median(values)
        std = np.std(values)
        min_val = np.min(values)
        max_val = np.max(values)
        slope = calculate_trend_slope(years_arr, values)

        summary_list.append({
            "Entity": country,
            "First": first,
            "Last": last,
            "Change": change,
            "%Change": pct_change,
            "Mean": mean,
            "Median": median,
            "Std Dev": std,
            "Min": min_val,
            "Max": max_val,
            "Trend Slope": slope
        })

    summary_df = pd.DataFrame(summary_list)

    numeric_cols = summary_df.select_dtypes(include=np.number).columns
    summary_df[numeric_cols] = summary_df[numeric_cols].round(3)

    st.dataframe(summary_df)

if __name__ == "__main__":
    app()