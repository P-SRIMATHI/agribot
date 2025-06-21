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

# ✅ Enable background
set_bg_from_local("agri_bg.jpg")

#Suggestion function
def suggest_agent(crop, pest):
    crop = crop.lower().strip()
    pest = pest.lower().strip()

    # Clean the dataframe
    df_clean = df.copy()
    df_clean['Crop'] = df_clean['Crop'].str.lower().str.strip()
    df_clean['Pest'] = df_clean['Pest'].str.lower().str.strip()

    # Exact crop match
    match_crop = df_clean[df_clean['Crop'] == crop]

    # Partial pest match
    match = match_crop[match_crop['Pest'].str.contains(pest, na=False)]

    if not match.empty:
        return match.iloc[0]['Biocontrol Agent'], match.iloc[0]['Usage Method']
    elif not match_crop.empty:
        # Pest not found, but crop found — suggest similar pests
        possible_pests = match_crop['Pest'].unique().tolist()
        return "No match found", f"Try one of these pests for {crop}: {', '.join(possible_pests)}"
    else:
        return "No match found", "Try different crop or pest."


# Page setup
st.set_page_config(page_title="AgriBot - Voice Based", layout="wide")

# Welcome message
st.markdown("""
# 🌾 AgriBot - Voice Based Biocontrol Assistant  
🎙️ Speak or type the crop and pest to get eco-friendly suggestions 💚  
""")

# Layout
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

# 🎙️ RIGHT: Inputs + Suggestion Button
with right:
    st.markdown("## 🎤 Type or Speak (Mic-friendly Inputs)")

    # Prepare placeholders to hold results
    result_placeholder = st.empty()

    # Initialize session_state
    if "crop_value" not in st.session_state:
        st.session_state.crop_value = ""
    if "pest_value" not in st.session_state:
        st.session_state.pest_value = ""

    # HTML for voice + type inputs
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
            window.parent.postMessage({{ type: 'streamlit:setComponentValue', key: targetKey, value: transcript }}, '*');
        }};

        recognition.onerror = function(event) {{
            alert('Speech recognition error: ' + event.error);
        }};

        recognition.start();
    }}
    </script>

    <label>🌿 Crop</label><br>
    <input type="text" id="crop_input" value="{st.session_state.crop_value}" 
           oninput="window.parent.postMessage({{ type: 'streamlit:setComponentValue', key: 'crop_value', value: this.value }}, '*');"
           style="width: 80%; padding: 6px;" />
    <button onclick="recordSpeech('crop_input', 'crop_value')">🎙 Speak</button><br><br>

    <label>🐛 Pest</label><br>
    <input type="text" id="pest_input" value="{st.session_state.pest_value}" 
           oninput="window.parent.postMessage({{ type: 'streamlit:setComponentValue', key: 'pest_value', value: this.value }}, '*');"
           style="width: 80%; padding: 6px;" />
    <button onclick="recordSpeech('pest_input', 'pest_value')">🎙 Speak</button>
    """

    # Render the mic+typing HTML
    components.html(voice_input_html, height=320)

    # Get current input values
    crop = st.session_state.crop_value
    pest = st.session_state.pest_value

    # Button and result inside the same column, right below inputs
    if st.button("🔍 Get Suggestion", key="suggest_button", use_container_width=True):
        agent, usage = suggest_agent(crop, pest)
        with result_placeholder:
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
