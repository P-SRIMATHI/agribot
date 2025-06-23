import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
import base64
import altair as alt
from datetime import datetime
import requests

# Load data
df = pd.read_csv("biocontrol_data.csv")

# ✅ Set page config
st.set_page_config(page_title="AgriBot - Voice Based", layout="wide")

# ✅ Set background image
def set_bg_from_local(image_file):
    with open(image_file, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url('data:image/jpg;base64,{encoded}');
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

set_bg_from_local("agri_bg.jpg")

# ✅ Remove top padding/margin
st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# 🪧 Static English title & description shown first
st.markdown("# 🌾 AgriBot - Voice Based Biocontrol Assistant")
st.markdown("🎙️ Speak or type the crop and pest to get eco-friendly suggestions 💚")

# ✅ Language toggle placed AFTER title
lang = st.radio("🌐 Language / மொழி", ["English", "தமிழ்"], horizontal=True)

# ✅ Language dictionary
texts = {
    "English": {
        "title": "🌾 AgriBot - Voice Based Biocontrol Assistant",
        "desc": "🎙️ Speak or type the crop and pest to get eco-friendly suggestions 💚",
        "crop": "🌿 Crop",
        "pest": "🐛 Pest",
        "mic_note": "#### 🎙 Click to speak",
        "speak_crop": "🎙 Speak Crop",
        "speak_pest": "🎙 Speak Pest",
        "get_suggestion": "🔍 Get Suggestion",
        "agent": "✅ Biocontrol Agent",
        "usage": "📌 Usage",
        "no_match": "❗ No match found",
        "footer": "📊 Built by Srima 💚 | 🎙 Voice via Web Speech API | 🧪 Powered by Python & Streamlit"
    },
    "தமிழ்": {
        "title": "🌾 AgriBot - குரல் வழியிலான உயிரணுக் கட்டுப்பாட்டு உதவியாளர்",
        "desc": "🎙️ பயிர் மற்றும் பூச்சியை பேசவும் அல்லது டைப் செய்யவும் — சூழலுக்கு உதவும் பரிந்துரைகளை பெறுங்கள் 💚",
        "crop": "🌿 பயிர்",
        "pest": "🐛 பூச்சி",
        "mic_note": "#### 🎙 பேச கிளிக் செய்யவும்",
        "speak_crop": "🎙 பயிர் பேசவும்",
        "speak_pest": "🎙 பூச்சி பேசவும்",
        "get_suggestion": "🔍 பரிந்துரை பெற",
        "agent": "✅ உயிரணுக் கட்டுப்பாட்டு முகவர்",
        "usage": "📌 பயன்பாடு",
        "no_match": "❗ பொருந்தவில்லை",
        "footer": "📊 உருவாக்கியவர் Srima 💚 | 🎙 குரல் வழி Web Speech API | 🧪 Python மற்றும் Streamlit மூலம் இயக்கப்படுகிறது"
    }
}


# Matching function
def suggest_agent(crop, pest):
    crop = crop.lower().strip()
    pest = pest.lower().strip()
    df_clean = df.copy()
    df_clean['Crop'] = df_clean['Crop'].astype(str).str.lower().str.strip()
    df_clean['Pest'] = df_clean['Pest'].astype(str).str.lower().str.strip()

    crop_matches = df_clean[df_clean['Crop'] == crop]
    if crop_matches.empty:
        return "No match found", f"Crop '{crop}' not found in data."
    pest_matches = crop_matches[crop_matches['Pest'].str.contains(pest, na=False, case=False)]

    if pest_matches.empty:
        possible = crop_matches['Pest'].unique().tolist()
        return "No match found", f"Try one of these pests: {', '.join(possible)}"
    else:
        row = pest_matches.iloc[0]
        return row['Biocontrol Agent'], row['Usage Method']

# 📍 Get current location using IP (for weather and regional data)
def get_weather():
    try:
        res = requests.get("https://ipapi.co/json/").json()
        city = res.get("city")
        region = res.get("region")
        country = res.get("country_name")
        lat, lon = res.get("latitude"), res.get("longitude")

        weather_key = "7df16b3736msh6ab2c9620d3e8b9p1df10ajsnc689a2c1a182"  # demo key
        url = f"https://api.weatherapi.com/v1/current.json?key=YOUR_WEATHERAPI_KEY&q={lat},{lon}"
        weather = requests.get(url).json()

        return city, region, country, weather['current']['temp_c'], weather['current']['condition']['text']
    except:
        return None, None, None, None, None

city, region, country, temp, condition = get_weather()

# Layout
def main_ui():
    left, right = st.columns([1.2, 1])

    with left:
        st.markdown("## 📊 Data Insights")

        if st.checkbox("📌 Pest Frequency - Bar Chart"):
            bar_data = df['Pest'].value_counts().reset_index()
            bar_data.columns = ['Pest', 'Count']
            bar_chart = alt.Chart(bar_data).mark_bar(size=20).encode(
                x=alt.X('Pest', sort='-y'),
                y='Count'
            ).properties(width=400, height=300)
            st.altair_chart(bar_chart, use_container_width=False)

        if st.checkbox("🧬 Agent Usage - Pie Chart"):
            agent_counts = df['Biocontrol Agent'].value_counts()
            fig, ax = plt.subplots(figsize=(4, 4))
            agent_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90, ax=ax)
            ax.set_ylabel("")
            st.pyplot(fig)

    with right:
        st.markdown("## 🎤 Speak or Type your crop and pest")
        crop_input = st.text_input("Crop")
        crop_suggestions = [c for c in df['Crop'].unique().tolist() if crop_input.lower() in c.lower()]
        if crop_suggestions:
            crop = st.selectbox("✅ Suggested Crops", crop_suggestions)
        else:
            crop = crop_input

        pest_input = st.text_input("Pest")
        pest_suggestions = [p for p in df['Pest'].unique().tolist() if pest_input.lower() in p.lower()]
        if pest_suggestions:
            pest = st.selectbox("✅ Suggested Pests", pest_suggestions)
        else:
            pest = pest_input

        if st.button("🔍 Get Suggestion"):
            agent, usage = suggest_agent(crop, pest)
            if agent != "No match found":
                st.success(f"✅ Biocontrol Agent: {agent}")
                st.info(f"📌 Usage: {usage}")
            else:
                st.warning(f"❗ {usage}")

    # 🌦️ Real-time weather section
    st.markdown("---")
    st.markdown("### 🌦️ Weather & Region Info")
    if city:
        st.info(f"📍 Location: {city}, {region}, {country}\n🌡️ Temp: {temp}°C | 🌤️ Condition: {condition}")
    else:
        st.warning("Couldn't fetch your regional weather info.")

    # 📎 Footer
    st.markdown("---")
    st.markdown("📊 Built by Srima 💚 | 🎙 Voice via Web Speech API | 🧪 Powered by Python & Streamlit")

main_ui()
