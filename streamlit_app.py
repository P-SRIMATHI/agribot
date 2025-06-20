import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import speech_recognition as sr
import base64

# Load Dataset
df = pd.read_csv("biocontrol_data.csv")

# Background image (optional)
def set_bg_from_local(image_file):
    with open(image_file, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Uncomment if you want background
# set_bg_from_local("agri_bg.jpg")

# Smart matching function
def suggest_agent(crop, pest):
    crop = crop.lower().strip()
    pest = pest.lower().strip()
    match = df[df['Crop'].str.lower() == crop]
    match = match[match['Pest'].str.lower().str.contains(pest)]
    if not match.empty:
        return match.iloc[0]['Biocontrol Agent'], match.iloc[0]['Usage Method']
    else:
        return "No match found", "Try a different crop or pest."

# Voice recognizer
def record_and_recognize():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎧 Listening... Speak clearly")
        audio = r.listen(source, phrase_time_limit=4)
        try:
            text = r.recognize_google(audio)
            st.success(f"✅ You said: `{text}`")
            return text
        except sr.UnknownValueError:
            st.warning("❗ Couldn't understand, try again.")
        except sr.RequestError:
            st.error("❌ API error. Check internet.")
    return ""

# Page config
st.set_page_config(page_title="AgriBot - Smart Biocontrol", layout="wide")

# 🌟 Welcome Header
st.markdown("""
# 🌱 Welcome to **AgriBot**
### Your Smart Organic Biocontrol Recommendation Assistant 🐞🧪  
Speak or type your crop and pest — get an eco-friendly, data-backed solution 💚  
""")

# Main 2-column layout
left, right = st.columns([1.2, 1])

# 👉 LEFT SIDE: Charts & Data
with left:
    st.markdown("## 📊 Pest & Biocontrol Analytics")

    if st.checkbox("📌 Show Pest Frequency (Bar Chart)"):
        pest_counts = df['Pest'].value_counts()
        st.bar_chart(pest_counts)

    if st.checkbox("🧬 Show Agent Usage (Pie Chart)"):
        agent_counts = df['Biocontrol Agent'].value_counts()
        fig, ax = plt.subplots()
        agent_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90, ax=ax)
        ax.set_ylabel("")
        st.pyplot(fig)

    with st.expander("📂 View Dataset"):
        st.dataframe(df)

# 👉 RIGHT SIDE: Suggestion UI
with right:
    st.markdown("## 📝 Get Biocontrol Suggestion")

    # Text inputs with session state
    crop = st.text_input("🌿 Enter Crop (e.g., Maize)", key="crop_input")
    pest = st.text_input("🐛 Enter Pest (e.g., Stem Borer)", key="pest_input")

    st.markdown("### 🎙️ Or Use Voice Input")

    if st.button("🎤 Record for Crop"):
        text = record_and_recognize()
        if text:
            st.session_state.crop_input = text

    if st.button("🎤 Record for Pest"):
        text = record_and_recognize()
        if text:
            st.session_state.pest_input = text

    if st.button("🔍 Suggest Biocontrol Agent"):
        agent, usage = suggest_agent(crop, pest)
        if agent != "No match found":
            st.success(f"✅ Biocontrol Agent: {agent}")
            st.info(f"📌 Usage Instructions: {usage}")
        else:
            st.warning("❗ No match found. Try different inputs.")

# Footer
st.markdown("""
---
🧪 Data: ICAR IPM for Maize | 👩‍🔬 Project by Srima | 🎤 Voice-enabled AgriBot  
🧠 Powered by Python + Streamlit + SpeechRecognition  
""")
