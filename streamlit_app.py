import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("biocontrol_data.csv")

# 🧠 Smart pest match
def suggest_agent(crop, pest):
    pest = pest.lower().strip()
    crop = crop.lower().strip()

    match = df[df['Crop'].str.lower() == crop]
    match = match[match['Pest'].str.lower().str.contains(pest)]

    if not match.empty:
        return match.iloc[0]['Biocontrol Agent'], match.iloc[0]['Usage Method']
    else:
        return "No match found", "Try a different crop/pest"

# 🖥️ UI Setup
st.set_page_config(page_title="AgriBot – Biocontrol Assistant", layout="centered")
st.title("🌱 AgriBot")
st.markdown("### 🌾 Organic Biocontrol Recommendation System")
st.markdown("Built with love for farmers, researchers, and nature 🌍")

# 🌿 Input Section
st.markdown("#### 📝 Enter Your Crop & Pest")
col1, col2 = st.columns(2)
with col1:
    crop = st.text_input("Enter Crop (e.g., Maize)")
with col2:
    pest = st.text_input("Enter Pest (e.g., Stem Borer)")

if st.button("🔍 Suggest Biocontrol Agent"):
    agent, usage = suggest_agent(crop, pest)
    if agent != "No match found":
        st.success(f"✅ Recommended Agent: {agent}")
        st.info(f"📌 Usage Instructions: {usage}")
    else:
        st.warning("❗ No matching result. Please check your input.")

st.divider()

# 📊 Analytics Section
st.markdown("### 📈 Dataset Insights")

col3, col4 = st.columns(2)
with col3:
    if st.checkbox("📌 Show Pest Frequencies (Bar Chart)"):
        pest_counts = df['Pest'].value_counts()
        st.bar_chart(pest_counts)

with col4:
    if st.checkbox("🧪 Show Biocontrol Agent Distribution (Pie Chart)"):
        agent_counts = df['Biocontrol Agent'].value_counts()
        fig, ax = plt.subplots()
        agent_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90, ax=ax)
        ax.set_ylabel("")
        st.pyplot(fig)

st.divider()

# 📋 Dataset Preview (optional)
with st.expander("🔍 Preview Biocontrol Dataset"):
    st.dataframe(df)

# 📌 Footer
st.markdown("""
---
© 2025 AgriBot | Developed by Srima 💚  
Data Source: ICAR - IPM Package for Maize  
Version: 1.0 | Powered by Streamlit
""")
