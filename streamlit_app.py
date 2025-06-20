import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load CSV
df = pd.read_csv("biocontrol_data.csv")

# Agent suggestion function with substring pest match
def suggest_agent(crop, pest):
    crop = crop.lower().strip()
    pest = pest.lower().strip()
    
    match = df[df['Crop'].str.lower() == crop]
    match = match[match['Pest'].str.lower().str.contains(pest)]
    
    if not match.empty:
        return match.iloc[0]['Biocontrol Agent'], match.iloc[0]['Usage Method']
    else:
        return "No match found", "Try a different crop or pest"

# Configure page
st.set_page_config(page_title="AgriBot - Smart Biocontrol", layout="wide")

# 🌟 Header / Welcome Page
st.markdown("""
# 🌱 Welcome to **AgriBot**
### Your Smart Organic Biocontrol Recommendation Assistant 🧪🐞

AgriBot helps farmers, researchers, and students find **eco-friendly solutions** for pest control — powered by **real ICAR data**.  
Enter your crop & pest to get personalized suggestions, and explore insightful analytics that guide sustainable farming 🌾

---
""")

# 🔄 Main Layout: Two Columns Side-by-Side
left, right = st.columns([1.2, 1])

# 👉 LEFT SIDE: Charts + Dataset
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

    crop = st.text_input("🌿 Enter Crop (e.g., Maize)")
    pest = st.text_input("🐛 Enter Pest (e.g., Stem Borer)")

    if st.button("🔍 Suggest Biocontrol Agent"):
        agent, usage = suggest_agent(crop, pest)
        if agent != "No match found":
            st.success(f"✅ Recommended Agent: {agent}")
            st.info(f"📌 Usage Instructions: {usage}")
        else:
            st.warning("❗ No match found. Please try again with a valid crop & pest.")

# Footer
st.markdown("""
---
🔬 Source: [ICAR - Integrated Pest Management Package (Maize)](https://ncipm.icar.gov.in/)  
🛠️ Developed with ❤️ by **Srima** | Version 1.0 | Powered by **Streamlit**
""")
