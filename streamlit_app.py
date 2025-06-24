import streamlit as st
import requests

# ---------------- CONFIG ----------------
st.set_page_config(page_title="AgriBot: NanoBioTwin", layout="wide")

# 🌱 Title
st.title("🌿 AgriBot: NanoBioTwin")
st.markdown("##### A Real-Time Digital Twin for Crop + Nanomaterial Simulation")

st.divider()

# ---------------- INPUT FIELDS ----------------
col1, col2, col3 = st.columns(3)

with col1:
    crop = st.selectbox("🌾 Select Crop", ["Maize", "Rice", "Wheat", "Tomato", "Cotton"])
with col2:
    nanomaterial = st.selectbox("🧪 Select Nanomaterial", ["Nano Urea", "ZnO Nanoparticles", "Nano Silica", "TiO2 Nano Pesticide"])
with col3:
    soil_type = st.selectbox("🧱 Select Soil Type", ["Sandy", "Loamy", "Clay", "Silty", "Peaty", "Saline"])

pH = st.slider("🔬 Soil pH", 3.0, 10.0, 6.5)
moisture = st.slider("💧 Soil Moisture (%)", 0, 100, 40)
location = st.text_input("📍 Enter Your Location (City)", "Chennai")

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
