import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

class FRIRegressionModel:
    def __init__(self, csv_path="datasets/merged_data.csv"):
        self.features = ["GDP", "HDI", "Internet", "Agri", "Poverty"]
        self.target = "FRI"
        self.df = pd.read_csv(csv_path)
        self._prepare_data()
        self._train_model()

    def _prepare_data(self):
        # Create FRI
        df_norm = self.df[self.features].copy()
        for col in self.features:
            min_val = df_norm[col].min()
            max_val = df_norm[col].max()
            df_norm[col] = (df_norm[col] - min_val) / (max_val - min_val)
        df_norm["Poverty"] = 1 - df_norm["Poverty"]  # invert poverty
        self.df[self.target] = (df_norm.mean(axis=1) * 100).round(3)
        # Drop any remaining NaNs
        self.df = self.df.dropna(subset=self.features + [self.target])

    def _train_model(self):
        X = self.df[self.features]
        y = self.df[self.target]
        self.model = RandomForestRegressor(n_estimators=200, random_state=42)
        self.model.fit(X, y)

    def predict(self, X_new):
        return self.model.predict(X_new)