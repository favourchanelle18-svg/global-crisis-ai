import pandas as pd
from sklearn.linear_model import LinearRegression

def train_model():
    data = pd.read_csv("data.csv")

    X = data[["population", "food_supply", "water_supply", "energy_supply", "crisis_severity"]]
    y = data["affected_population"]

    model = LinearRegression()
    model.fit(X, y)

    return model
