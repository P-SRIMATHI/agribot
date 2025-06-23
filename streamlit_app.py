import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
import base64
import altair as alt
from PIL import Image
import numpy as np
import tensorflow as tf

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("biocontrol_data.csv")

df = load_data()

# ✅ Set page config
st.set_page_config(page_title="AgriBot - Voice Based", layout="wide")

# ✅ Set background image
@st.cache_data
def get_bg_css(image_file):
    with open(image_file, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    return f"""
    <style>
    .stApp {{
        background-image: url('data:image/jpg;base64,{encoded}');
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }}
    </style>
    """

st.markdown(get_bg_css("agri_bg.jpg"), unsafe_allow_html=True)

# ✅ Remove top padding/margin
st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Title & Language
st.markdown("# 🌾 AgriBot - Voice Based Biocontrol Assistant")
st.markdown("🎙️ Speak or type the crop and pest to get eco-friendly suggestions 💚")
lang = st.radio("🌐 Language / மொழி", ["English", "தமிழ்"], horizontal=True)

# Language texts
txt = {
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
} if lang == "English" else {
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

# Image Recognition Model
@st.cache_resource
def load_model():
    return tf.keras.models.load_model("pest_disease_model.h5")

model = load_model()
class_names = ['healthy', 'stem borer', 'leaf blight', 'aphids']

def predict_image(image):
    img = image.resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = img_array.reshape((1, 224, 224, 3))
    prediction = model.predict(img_array)
    predicted_class = class_names[np.argmax(prediction)]
    confidence = np.max(prediction)
    return predicted_class, confidence

# UI
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
    crop = st.selectbox("✅ Suggested Crops", crop_suggestions) if crop_suggestions else crop_input

    pest_input = st.text_input("Pest")
    pest_suggestions = [p for p in df['Pest'].unique().tolist() if pest_input.lower() in p.lower()]
    pest = st.selectbox("✅ Suggested Pests", pest_suggestions) if pest_suggestions else pest_input

    if st.button("🔍 Get Suggestion"):
        agent, usage = suggest_agent(crop, pest)
        if agent != "No match found":
            st.success(f"✅ Biocontrol Agent: {agent}")
            st.info(f"📌 Usage: {usage}")
        else:
            st.warning(f"❗ {usage}")

    st.markdown("---")
    st.markdown("### 📷 Upload Crop Leaf Image")
    uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        predicted_class, confidence = predict_image(image)
        st.success(f"Predicted: {predicted_class} ({confidence * 100:.2f}% confidence)")

st.markdown("---")
st.markdown(txt["footer"])
