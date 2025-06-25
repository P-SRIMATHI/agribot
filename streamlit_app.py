import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns

# Set custom background
import base64

def set_bg_image(image_file):
    with open(image_file, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode()
        css = f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)

set_bg_image("agri_bg.jpg")

# Load dataset
df = pd.read_csv("Custom_Crops_yield_Historical_Dataset.csv")

# Display basic dataset info
st.title("🌾 Smart Crop Yield Predictor")
st.write("This app uses real historical crop data to predict crop yield based on minimal user input.")
st.subheader("Dataset Preview")
st.dataframe(df.head())

# Drop missing values for simplicity
df.dropna(inplace=True)

# Select simple but key features
features = ['Rainfall (mm)', 'Fertilizer Used (kg/ha)', 'Avg Temperature (°C)']
target = 'Yield (kg/ha)'

X = df[features]
y = df[target]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict & evaluate
y_pred = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

st.subheader("Model Performance")
st.write(f"✅ RMSE: {rmse:.2f}")
st.write(f"✅ R² Score: {r2:.2f}")

# Feature importance plot
st.subheader("Feature Importance")
importance_df = pd.DataFrame({
    'Feature': features,
    'Importance': model.feature_importances_
}).sort_values(by='Importance', ascending=False)

fig, ax = plt.subplots()
sns.barplot(x='Importance', y='Feature', data=importance_df, ax=ax)
st.pyplot(fig)

# Real-time prediction
st.subheader("📥 Enter Crop Conditions")
rainfall = st.number_input("Rainfall (mm)", min_value=0.0, value=100.0)
fertilizer = st.number_input("Fertilizer Used (kg/ha)", min_value=0.0, value=50.0)
temp = st.number_input("Avg Temperature (°C)", min_value=0.0, value=25.0)

# Predict yield
if st.button("🔍 Predict Crop Yield"):
    user_input = pd.DataFrame({
        'Rainfall (mm)': [rainfall],
        'Fertilizer Used (kg/ha)': [fertilizer],
        'Avg Temperature (°C)': [temp]
    })
    prediction = model.predict(user_input)[0]
    st.success(f"🌱 Predicted Yield: {prediction:.2f} kg/ha")
