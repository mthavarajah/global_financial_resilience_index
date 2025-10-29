import pandas as pd

def load_merged_data():
    # Load the single merged dataset
    df = pd.read_csv("datasets/merged_data.csv")

    # Rename columns for consistency
    df.rename(columns={
        "Human Development Index": "HDI",
        "Individuals using the Internet (% of population)": "Internet Usage (%)",
        "share_employed_agri": "Labor in Agriculture (%)",
        "Population (historical)": "Population"
    }, inplace=True)

    # Convert numeric columns properly
    numeric_cols = ["GDP per capita", "HDI", "Internet Usage (%)", "Labor in Agriculture (%)", "Population"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Sort and fill missing values (forward/backward fill per country)
    df = df.sort_values(by=["Entity", "Year"])
    df.groupby("Entity", group_keys=False).apply(lambda g: g.fillna(method="ffill").fillna(method="bfill"))

    # ✅ Add latitude/longitude from a predefined dictionary
    latlon_dict = {
        'Afghanistan': (33.9391, 67.7100),
        'Albania': (41.1533, 20.1683),
        'Algeria': (28.0339, 1.6596),
        'Angola': (-11.2027, 17.8739),
        'Argentina': (-38.4161, -63.6167),
        'Armenia': (40.0691, 45.0382),
        'Australia': (-25.2744, 133.7751),
        'Austria': (47.5162, 14.5501),
        'Bangladesh': (23.6850, 90.3563),
        'Belgium': (50.5039, 4.4699),
        'Brazil': (-14.2350, -51.9253),
        'Canada': (56.1304, -106.3468),
        'China': (35.8617, 104.1954),
        'France': (46.2276, 2.2137),
        'Germany': (51.1657, 10.4515),
        'India': (20.5937, 78.9629),
        'United States': (37.0902, -95.7129),
        # add more as needed...
    }

    df["Latitude"] = df["Entity"].map(lambda x: latlon_dict.get(x, (0, 0))[0])
    df["Longitude"] = df["Entity"].map(lambda x: latlon_dict.get(x, (0, 0))[1])

    return df