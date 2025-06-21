import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import streamlit.components.v1 as components

# Load CSV
df = pd.read_csv("biocontrol_data.csv")

# Set background
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

set_bg_from_local("agri_bg.jpg")

# Fix crop/pest matching
def suggest_agent(crop, pest):
    crop = crop.lower().strip()
    pest = pest.lower().strip()
    df_clean = df.copy()
    df_clean['Crop'] = df_clean['Crop'].str.lower().str.strip()
    df_clean['Pest'] = df_clean['Pest'].str.lower().str.strip()
    match_crop = df_clean[df_clean['Crop'] == crop]
    match = match_crop[match_crop['Pest'].str.contains(pest, na=False)]
    if not match.empty:
        return match.iloc[0]['Biocontrol Agent'], match.iloc[0]['Usage Method']
    elif not match_crop.empty:
        return "No match found", f"Try one of these pests: {', '.join(match_crop['Pest'].unique())}"
    else:
        return "No match found", "Try different crop or pest."

# Page settings
st.set_page_config(page_title="AgriBot - Voice Based", layout="wide")

# Header
st.markdown("""
# 🌾 AgriBot - Voice Based Biocontrol Assistant  
🎙️ Speak or type the crop and pest to get eco-friendly suggestions 💚  
""")

# Layout
left, right = st.columns([1.2, 1])

# Left side: charts
with left:
    st.markdown("## 📊 Data Insights")
    if st.checkbox("📌 Pest Frequency - Bar Chart"):
        st.bar_chart(df['Pest'].value_counts())
    if st.checkbox("🧬 Agent Usage - Pie Chart"):
        agent_counts = df['Biocontrol Agent'].value_counts()
        fig, ax = plt.subplots()
        agent_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90, ax=ax)
        ax.set_ylabel("")
        st.pyplot(fig)

# Right side: inputs + mic + suggestion
with right:
    st.markdown("## 🎤 Type or Speak Inputs")

    # Real Streamlit inputs — tightly bind to session state
    crop = st.text_input("🌿 Crop", key="crop_input")
    pest = st.text_input("🐛 Pest", key="pest_input")

    # Mic buttons update the above fields
    components.html("""
    <script>
    function recordSpeech(fieldId){
        const recog = new(window.SpeechRecognition || window.webkitSpeechRecognition)();
        recog.lang = 'en-IN';
        recog.interimResults = false;
        recog.maxAlternatives = 1;
        recog.onresult = function(e){
            const result = e.results[0][0].transcript;
            const inputBox = window.parent.document.querySelectorAll('input[data-baseweb="input"]');
            for (let i = 0; i < inputBox.length; i++) {
                if (inputBox[i].id.includes(fieldId)) {
                    inputBox[i].value = result;
                    inputBox[i].dispatchEvent(new Event('input', { bubbles: true }));
                }
            }
        };
        recog.start();
    }
    </script>
    <button onclick="recordSpeech('crop_input')">🎙 Speak Crop</button>
    <button onclick="recordSpeech('pest_input')">🎙 Speak Pest</button>
    """, height=100)

    # Suggestion button right under inputs
    if st.button("🔍 Get Suggestion", use_container_width=True):
        agent, usage = suggest_agent(crop, pest)
        if agent != "No match found":
            st.success(f"✅ Biocontrol Agent: {agent}")
            st.info(f"📌 Usage: {usage}")
        else:
            st.warning(f"❗ {usage}")

# Footer
st.markdown("""
---
📊 Built by Srima 💚 | 🎙 Voice via Web Speech API | 🧪 Powered by Python & Streamlit
""")
