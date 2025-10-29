import pandas as pd
from countryinfo import CountryInfo

gdp = pd.read_csv("datasets/gdp_per_capita/gdp.csv")
hdi = pd.read_csv("datasets/hdi/hdi.csv")
internet = pd.read_csv("datasets/internet/internet.csv")
agri = pd.read_csv("datasets/labor_agri/agri.csv")

gdp = gdp[["Entity", "Code", "Year", "GDP per capita"]].rename(columns={"GDP per capita": "GDP"})
hdi = hdi[["Entity", "Code", "Year", "Human Development Index"]].rename(columns={"Human Development Index": "HDI"})
internet = internet[["Entity", "Code", "Year", "Individuals using the Internet (% of population)"]].rename(columns={"Individuals using the Internet (% of population)": "Internet"})
agri = agri[["Entity", "Code", "Year", "share_employed_agri"]].rename(columns={"share_employed_agri": "Agri"})

merged = gdp.merge(hdi, on=["Entity", "Code", "Year"], how="outer")
merged = merged.merge(internet, on=["Entity", "Code", "Year"], how="outer")
merged = merged.merge(agri, on=["Entity", "Code", "Year"], how="outer")

merged = merged[(merged["Year"] >= 1990) & (merged["Year"] <= 2023)]
merged = merged.sort_values(by=["Entity", "Year"]).reset_index(drop=True)

num_cols = ["GDP", "HDI", "Internet", "Agri"]
for col in num_cols:
    merged[col] = pd.to_numeric(merged[col], errors="coerce")

merged = merged.groupby("Entity", group_keys=False).apply(lambda g: g.fillna(method="ffill").fillna(method="bfill"))

for col in num_cols:
    if merged[col].isna().any():
        merged[col] = merged[col].fillna(merged[col].median())

if "Code" in merged.columns:
    merged = merged.drop(columns=["Code"])

coords = []
unique_countries = merged["Entity"].unique()

for country in unique_countries:
    try:
        info = CountryInfo(country)
        details = info.info()
        lat, lon = details.get("latlng", [None, None])
    except Exception:
        lat, lon = None, None
    coords.append({"Entity": country, "Lat": lat, "Lon": lon})

coords_df = pd.DataFrame(coords)
merged = merged.merge(coords_df, on="Entity", how="left")
merged.to_csv("datasets/merged_data.csv", index=False)