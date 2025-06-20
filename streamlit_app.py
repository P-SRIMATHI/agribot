import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
import base64

# Load dataset
df = pd.read_csv("biocontrol_data.csv")

# Optional Background Image
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

# Uncomment this if you added a background image named 'agri_bg.jpg'
# set_bg_from_local("agri_bg.jpg")

# Smart suggestion logic (matches even part of pest name)
def suggest_agent(crop, pest):
    crop = crop.lower().strip()
    pest = pest.lower().strip()
    matches = df[df['Crop'].str.lower().str.contains(crop) & df['Pest'].str.lower().str.contains(pest)]
    if not matches.empty:
        agent = matches.iloc[0]['Biocontrol Agent']
        usage = matches.iloc[0]['Usage Method']
        return agent, usage
    else:
        return "No match found", "Try different keywords"

# Set wide layout
st.set_page_config(page_title="AgriBot", layout="wide")

# Stylish title section
st.markdown("""
<div style="background-color:#daf7dc; padding:15px; border-radius:10px">
    <h1 style="color:#2d572c">🌾 AgriBot - Voice Based Biocontrol Assistant</h1>
    <p style="color:#333; font-size:16px;">🎙️ Speak or type the crop and pest to get eco-friendly suggestions 💚</p>
</div>
""", unsafe_allow_html=True)

# Create columns
left, right = st.columns([1.3, 1])

# LEFT = Analytics
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

    with st.expander("📂 View Dataset"):
        st.dataframe(df)

# RIGHT = Voice & Suggestion
with right:
    st.markdown("## 🎤 Voice-Based Input (Mic-friendly)")

    voice_html = """
    <script>
    function recordSpeech(id) {
        var recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'en-IN';
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            document.getElementById(id).value = transcript;
            document.getElementById(id).dispatchEvent(new Event('input', { bubbles: true }));
        };

        recognition.start();
    }
    </script>

    <label>🌿 Crop</label><br>
    <input type="text" id="crop_input" style="width: 80%; padding: 6px;" />
    <button onclick="recordSpeech('crop_input')">🎙 Speak</button><br><br>

    <label>🐛 Pest</label><br>
    <input type="text" id="pest_input" style="width: 80%; padding: 6px;" />
    <button onclick="recordSpeech('pest_input')">🎙 Speak</button>
    """

    components.html(voice_html, height=250)

    crop = st.text_input("✅ Crop (type or mic)", key="crop")
    pest = st.text_input("✅ Pest (type or mic)", key="pest")

    if st.button("🔍 Get Suggestion"):
        agent, usage = suggest_agent(crop, pest)
        if agent != "No match found":
            st.success(f"🌱 Biocontrol Agent: {agent}")
            st.info(f"📌 Usage Method: {usage}")
        else:
            st.warning("⚠️ No match found. Try simpler keywords like just 'Stem Borer' or 'Helicoverpa'.")

# Footer
st.markdown("""
---
💡 Powered by Streamlit | 🔊 Voice via Web Speech API | 👩‍🌾 Built with 💚 by Srima
""")
