import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
import base64
import requests

# Set background image
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

# Weather API integration
@st.cache_data
def get_weather_data(city_name, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "Temperature": data["main"]["temp"],
            "Humidity": data["main"]["humidity"],
            "Wind_Speed": data["wind"]["speed"]
        }
    else:
        return None

# Load dataset
try:
    df = pd.read_csv("Custom_Crops_yield_Historical_Dataset.csv")
    df.dropna(inplace=True)

    available_columns = df.columns.tolist()

    rainfall_col = "Rainfall_mm"
    temperature_col = "Temperature_C"
    fertilizer_col = "Total_N_kg"  # assuming NPK values are considered fertilizer inputs
    target_col = "Yield_kg_per_ha"
    crop_col = "Crop"

    if None in [rainfall_col, fertilizer_col, temperature_col, target_col, crop_col]:
        st.error("🚫 Required columns not found. Available: " + ", ".join(available_columns))
    else:
        df[crop_col] = df[crop_col].astype('category')
        df['Crop_encoded'] = df[crop_col].cat.codes

        features = [rainfall_col, fertilizer_col, temperature_col, 'Crop_encoded']
        X = df[features]
        y = df[target_col]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)

        st.title("🌾 Smart Crop Yield Predictor")
        st.write("This app uses historical crop data + live weather to predict your yield accurately.")

        st.subheader("📊 Model Performance")
        st.write(f"✅ RMSE: {rmse:.2f}")
        st.write(f"✅ R² Score: {r2:.2f}")

        st.subheader("📌 Feature Importance")
        importance_df = pd.DataFrame({
            'Feature': features,
            'Importance': model.feature_importances_
        }).sort_values(by='Importance', ascending=False)

        fig1, ax1 = plt.subplots(figsize=(4, 3))
        sns.barplot(x='Importance', y='Feature', data=importance_df, ax=ax1)
        st.pyplot(fig1)

        st.subheader("🧮 Enter Values for Prediction")

        selected_crop = st.selectbox("🌾 Choose Crop", df[crop_col].unique())
        district = st.text_input("📍 District/City for Weather", value="Chennai")

        weather_api_key = st.secrets["weather_api_key"] if "weather_api_key" in st.secrets else "your_openweather_key_here"
        weather = get_weather_data(district, weather_api_key)

        if weather:
            st.success(f"🌡️ Temp: {weather['Temperature']} °C | 💧 Humidity: {weather['Humidity']}% | 🌬️ Wind: {weather['Wind_Speed']} m/s")

        try:
            rainfall = float(st.text_input("🌧️ Rainfall (mm)", "100"))
            fertilizer = float(st.text_input("🧪 Fertilizer Used (kg/ha)", "50"))
            temp = weather['Temperature'] if weather else float(st.text_input("🌡️ Temperature (°C)", "25"))
        except ValueError:
            st.error("❗Please enter numeric values.")
            st.stop()

        crop_encoded = df[df[crop_col] == selected_crop]['Crop_encoded'].iloc[0]

        if st.button("🔍 Predict Yield"):
            user_input = pd.DataFrame({
                rainfall_col: [rainfall],
                fertilizer_col: [fertilizer],
                temperature_col: [temp],
                'Crop_encoded': [crop_encoded]
            })
            prediction = model.predict(user_input)[0]
            st.success(f"🌱 Estimated Yield for {selected_crop}: {prediction:.2f} kg/ha")

        st.subheader("📈 Trend Visualizations")
        crop_data = df[df[crop_col] == selected_crop]

        col1, col2 = st.columns(2)
        with col1:
            fig2, ax2 = plt.subplots(figsize=(4, 3))
            sns.lineplot(data=crop_data, x='Year', y=target_col, ax=ax2)
            ax2.set_title("Yield Over Years")
            st.pyplot(fig2)

        with col2:
            fig3, ax3 = plt.subplots(figsize=(4, 3))
            sns.heatmap(crop_data[[rainfall_col, target_col]].corr(), annot=True, cmap="coolwarm", ax=ax3)
            ax3.set_title("Rainfall vs Yield")
            st.pyplot(fig3)

        fig4, ax4 = plt.subplots(figsize=(3.5, 2.5))  # Reduced chart size
        sns.scatterplot(data=crop_data, x=fertilizer_col, y=target_col, ax=ax4)
        ax4.set_title("Fertilizer Impact on Yield")
        st.pyplot(fig4)

except Exception as e:
    st.error(f"🚨 Error: {e}")
