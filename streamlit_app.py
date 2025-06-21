import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
import base64

# Load CSV
df = pd.read_csv("biocontrol_data.csv")

# Background image setup
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

# Set background
set_bg_from_local("agri_bg.jpg")

# 💡 FINAL fixed function
def suggest_agent(crop, pest):
    crop = crop.lower().strip()
    pest = pest.lower().strip()

    # Clean the dataframe
    df_clean = df.copy()
    df_clean['Crop'] = df_clean['Crop'].astype(str).str.lower().str.strip()
    df_clean['Pest'] = df_clean['Pest'].astype(str).str.lower().str.strip()

    # Filter by crop
    crop_matches = df_clean[df_clean['Crop'] == crop]

    if crop_matches.empty:
        return "No match found", f"Crop '{crop}' not found in data."

    # Filter pest using partial match (str.contains)
    pest_matches = crop_matches[crop_matches['Pest'].str.contains(pest, na=False, case=False)]

    if pest_matches.empty:
        possible = crop_matches['Pest'].unique().tolist()
        return "No match found", f"Try one of these pests: {', '.join(possible)}"
    else:
        row = pest_matches.iloc[0]
        return row['Biocontrol Agent'], row['Usage Method']

# Page setup
st.set_page_config(page_title="AgriBot - Voice Based", layout="wide")

# Header
st.markdown("""
# 🌾 AgriBot - Voice Based Biocontrol Assistant  
🎙️ Speak or type the crop and pest to get eco-friendly suggestions 💚  
""")

# Layout: 2 columns
left, right = st.columns([1.2, 1])

# 📊 LEFT: Charts
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

# 🎙️ RIGHT: Inputs + Mic + Suggestion
with right:
    st.markdown("## 🎤 Type or Speak Inputs")

    # Native text inputs
    crop = st.text_input("🌿 Crop", key="crop_input")
    pest = st.text_input("🐛 Pest", key="pest_input")

    # Mic buttons - INLINE, no float
    st.markdown("#### 🎙 Click to speak")
    mic_html = """
    <script>
    function recordSpeech(field) {
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'en-IN';
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            const inputs = window.parent.document.querySelectorAll('input[data-baseweb="input"]');
            for (let i = 0; i < inputs.length; i++) {
                if (inputs[i].id.includes(field)) {
                    inputs[i].value = transcript;
                    inputs[i].dispatchEvent(new Event('input', { bubbles: true }));
                }
            }
        };

        recognition.onerror = function(event) {
            alert('Speech recognition error: ' + event.error);
        };

        recognition.start();
    }
    </script>
    <button onclick="recordSpeech('crop_input')">🎙 Speak Crop</button>
    <button onclick="recordSpeech('pest_input')">🎙 Speak Pest</button>
    """
    components.html(mic_html, height=100)

    # Suggestion button right below inputs
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
