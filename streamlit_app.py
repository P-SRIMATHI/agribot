import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
import base64

# Load data
df = pd.read_csv("biocontrol_data.csv")

# 🌄 Set background image
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

# ✅ Set the background image
set_bg_from_local("agri_bg.jpg")  # Make sure this file exists in the same folder

# Suggestion function
def suggest_agent(crop, pest):
    crop = crop.lower().strip()
    pest = pest.lower().strip()
    match = df[df['Crop'].str.lower() == crop]
    match = match[match['Pest'].str.lower().str.contains(pest)]
    if not match.empty:
        return match.iloc[0]['Biocontrol Agent'], match.iloc[0]['Usage Method']
    else:
        return "No match found", "Try different crop or pest."

# Page setup
st.set_page_config(page_title="AgriBot - Voice Based", layout="wide")

# Welcome message
st.markdown("""
# 🌾 AgriBot - Voice Based Biocontrol Assistant  
🎙️ Speak or type the crop and pest to get eco-friendly suggestions 💚  
""")

# Layout: 2 columns
left, right = st.columns([1.2, 1])

# 📊 LEFT: Analytics
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

# 🎙️ RIGHT: Input (with voice + typing in single boxes)
with right:
    st.markdown("## 🎤 Type or Speak (Mic-friendly Inputs)")

    # Create empty inputs in session state
    if "crop_value" not in st.session_state:
        st.session_state.crop_value = ""
    if "pest_value" not in st.session_state:
        st.session_state.pest_value = ""

    # HTML + JS mic input (binds to hidden JS that updates Streamlit)
    voice_input_html = f"""
    <script>
    function recordSpeech(id, targetKey) {{
        var recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'en-IN';
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        recognition.onresult = function(event) {{
            const transcript = event.results[0][0].transcript;
            document.getElementById(id).value = transcript;

            // Send value to Streamlit via postMessage
            window.parent.postMessage({{ type: 'streamlit:setComponentValue', key: targetKey, value: transcript }}, '*');
        }};

        recognition.onerror = function(event) {{
            alert('Speech recognition error: ' + event.error);
        }};

        recognition.start();
    }}
    </script>

    <label>🌿 Crop</label><br>
    <input type="text" id="crop_input" value="{st.session_state.crop_value}" oninput="window.parent.postMessage({{ type: 'streamlit:setComponentValue', key: 'crop_value', value: this.value }}, '*');" style="width: 80%; padding: 6px;" />
    <button onclick="recordSpeech('crop_input', 'crop_value')">🎙 Speak</button><br><br>

    <label>🐛 Pest</label><br>
    <input type="text" id="pest_input" value="{st.session_state.pest_value}" oninput="window.parent.postMessage({{ type: 'streamlit:setComponentValue', key: 'pest_value', value: this.value }}, '*');" style="width: 80%; padding: 6px;" />
    <button onclick="recordSpeech('pest_input', 'pest_value')">🎙 Speak</button>
    """

    # Display HTML fields
    components.html(voice_input_html, height=300)

    # Now just use session state values — no extra inputs
    crop = st.session_state.crop_value
    pest = st.session_state.pest_value

    if st.button("🔍 Get Suggestion"):
        agent, usage = suggest_agent(crop, pest)
        if agent != "No match found":
            st.success(f"✅ Biocontrol Agent: {agent}")
            st.info(f"📌 Usage: {usage}")
        else:
            st.warning("❗ No match found. Try different keywords.")



# Footer
st.markdown("""
---
📊 Built by Srima 💚 | 🎙 Voice via Web Speech API | 🧪 Powered by Python & Streamlit
""")
