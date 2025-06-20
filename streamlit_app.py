import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import streamlit.components.v1 as components
import base64

# Load Dataset
df = pd.read_csv("biocontrol_data.csv")

# Optional background
# def set_bg_from_local(image_file):
#     with open(image_file, "rb") as img_file:
#         encoded = base64.b64encode(img_file.read()).decode()
#     css = f"""
#     <style>
#     .stApp {{
#         background-image: url("data:image/jpg;base64,{encoded}");
#         background-size: cover;
#         background-attachment: fixed;
#         background-position: center;
#     }}
#     </style>
#     """
#     st.markdown(css, unsafe_allow_html=True)

# set_bg_from_local("agri_bg.jpg")  # Optional

# Match function
def suggest_agent(crop, pest):
    crop = crop.lower().strip()
    pest = pest.lower().strip()
    match = df[df['Crop'].str.lower() == crop]
    match = match[match['Pest'].str.lower().str.contains(pest)]
    if not match.empty:
        return match.iloc[0]['Biocontrol Agent'], match.iloc[0]['Usage Method']
    else:
        return "No match found", "Try different inputs"

# Streamlit layout
st.set_page_config(page_title="AgriBot Voice", layout="wide")

# Welcome
st.markdown("""
# 🌾 AgriBot - Voice Powered Biocontrol Tool
🎙 Use your voice to fill crop and pest info — then get eco-friendly agent suggestions!
""")

left, right = st.columns([1.2, 1])

# LEFT COLUMN: Charts + Data
with left:
    st.markdown("## 📊 Pest & Agent Analytics")

    if st.checkbox("Bar Chart of Pests"):
        pest_counts = df['Pest'].value_counts()
        st.bar_chart(pest_counts)

    if st.checkbox("Pie Chart of Agent Usage"):
        agent_counts = df['Biocontrol Agent'].value_counts()
        fig, ax = plt.subplots()
        agent_counts.plot(kind='pie', autopct='%1.1f%%', ax=ax)
        ax.set_ylabel("")
        st.pyplot(fig)

    with st.expander("📁 View Dataset"):
        st.dataframe(df)

# RIGHT COLUMN: Input + Voice Capture
with right:
    st.markdown("## 🧠 Suggestion Area")

    # JS Component: Browser Voice to Text
    st.markdown("### 🎤 Record Using Your Voice")

    record_html = """
    <script>
    var streamlitCropInput = window.streamlitCropInput || "";
    var streamlitPestInput = window.streamlitPestInput || "";

    function recordSpeech(id) {
        var recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'en-IN';
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            const input = document.getElementById(id);
            input.value = transcript;
            input.dispatchEvent(new Event('input', { bubbles: true }));
        };

        recognition.start();
    }
    </script>

    <label>🌿 Crop</label><br>
    <input type="text" id="crop_input" oninput="window.streamlitCropInput = this.value" style="width: 80%; padding: 6px;">
    <button onclick="recordSpeech('crop_input')">🎙 Speak</button>
    <br><br>

    <label>🐛 Pest</label><br>
    <input type="text" id="pest_input" oninput="window.streamlitPestInput = this.value" style="width: 80%; padding: 6px;">
    <button onclick="recordSpeech('pest_input')">🎙 Speak</button>

    <script>
    // Send values to Streamlit
    const observer = new MutationObserver(() => {
        window.parent.postMessage({
            isStreamlitMessage: true,
            type: "streamlit:setComponentValue",
            value: {
                crop: window.streamlitCropInput,
                pest: window.streamlitPestInput
            }
        }, "*");
    });
    observer.observe(document.body, { childList: true, subtree: true });
    </script>
    """

    components.html(record_html, height=250)

    # Get data from JS
    crop = st.text_input("✅ Crop (from mic or type)", key="crop")
    pest = st.text_input("✅ Pest (from mic or type)", key="pest")

    if st.button("🔍 Get Suggestion"):
        agent, usage = suggest_agent(crop, pest)
        if agent != "No match found":
            st.success(f"✅ Agent: {agent}")
            st.info(f"📌 Usage: {usage}")
        else:
            st.warning("❗ No match. Try again.")

# Footer
st.markdown("---")
st.markdown("🎤 Voice Input via Web Speech API | 💚 Built by Srima | 🌿 Powered by Streamlit + JavaScript")
