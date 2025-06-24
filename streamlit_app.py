import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

st.set_page_config(page_title="🌾 Crop Yield Prediction App")
st.title("🌾 Real-Time Crop Yield Predictor")

# Load Data
df = pd.read_csv("Custom_Crops_yield_Historical_Dataset.csv")
st.subheader("📂 Dataset Preview")
st.dataframe(df.head())

# Rename for easier access (if needed)
df = df.rename(columns={
    "Temperature_C": "Temperature",
    "Humidity_%": "Humidity",
    "Rainfall_mm": "Rainfall",
    "Wind_Speed_m_s": "WindSpeed",
    "Solar_Radiation_MJ_m2_day": "SolarRadiation",
    "Yield_kg_per_ha": "Yield"
})

# Input features
features = ["Temperature", "Humidity", "pH", "Rainfall", "WindSpeed", "SolarRadiation"]
X = df[features]
y = df["Yield"]

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
preds = model.predict(X_test)
mse = mean_squared_error(y_test, preds)
r2 = r2_score(y_test, preds)

st.write(f"📉 **Model RMSE**: {np.sqrt(mse):.2f}")
st.write(f"📈 **Model R² Score**: {r2:.2f}")

# User Input
st.subheader("📌 Enter Environmental Conditions")
temp = st.number_input("Temperature (°C)", 0.0, 50.0, step=0.1)
humidity = st.number_input("Humidity (%)", 0.0, 100.0, step=1.0)
ph = st.number_input("Soil pH", 0.0, 14.0, step=0.1)
rainfall = st.number_input("Rainfall (mm)", 0.0, 3000.0, step=1.0)
wind = st.number_input("Wind Speed (m/s)", 0.0, 20.0, step=0.1)
solar = st.number_input("Solar Radiation (MJ/m²/day)", 0.0, 30.0, step=0.1)

if st.button("🚀 Predict Yield"):
    input_data = np.array([[temp, humidity, ph, rainfall, wind, solar]])
    prediction = model.predict(input_data)[0]
    st.success(f"🌾 Predicted Yield: **{prediction:.2f} kg/ha**")

# Show feature importance
st.subheader("🔍 Feature Importance")
importance_df = pd.DataFrame({
    "Feature": features,
    "Importance": model.feature_importances_
}).sort_values(by="Importance", ascending=False)

fig, ax = plt.subplots()
sns.barplot(x="Importance", y="Feature", data=importance_df, ax=ax)
st.pyplot(fig)

st.markdown("---")
st.caption("Built with 💚 using real-world Kaggle dataset")
