import streamlit as st
import requests
import pandas as pd

# ---------------- CONFIG ----------------
st.set_page_config(page_title="AgriBot: NanoBioTwin", layout="wide")

# 🌱 Title
st.title("🌿 AgriBot: NanoBioTwin")
st.markdown("##### A Real-Time Digital Twin for Crop + Nanomaterial Simulation")

st.divider()

#INPUT 

# Load real crop yield dataset
df = pd.read_csv("Custom_Crops_yield_Historical_Dataset.csv")

# Show dataset preview
st.subheader("📋 Historical Crop Yield Dataset")
st.dataframe(df.head())

# ---------------- WEATHER DATA ----------------
API_KEY = "750cf7197bfe592beab29c3d93303d1b"

def get_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "rainfall": data.get("rain", {}).get("1h", 0.0),
            "weather": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"]
        }
    return None

# ---------------- SIMULATION ----------------
if st.button("🌦️ Run Simulation with Live Weather"):
    weather = get_weather_data(location)

    if weather:
        st.success(f"🌍 Real-Time Weather for **{location.title()}**")
        st.write(weather)

        # 🔬 Basic effectiveness formula
        score = 100
        score -= abs(pH - 6.5) * 5
        score -= abs(weather['temperature'] - 28) * 2
        score += {
            "Nano Urea": 10,
            "ZnO Nanoparticles": 7,
            "Nano Silica": 5,
            "TiO2 Nano Pesticide": 3
        }.get(nanomaterial, 0)

        score = max(min(score, 100), 0)

        # 📊 Result
        st.markdown("### 🧪 Predicted Nano Effectiveness Score")
        st.metric("📈 Expected Yield Impact", f"{score:.2f} / 100")

    else:
        st.error("⚠️ Could not fetch weather. Check city name or API key.")
