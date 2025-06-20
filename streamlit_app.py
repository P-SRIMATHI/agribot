import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("biocontrol_data.csv")

# ✅ Updated Suggestion Function (flexible pest input)
def suggest_agent(crop, pest):
    pest = pest.lower().strip()
    crop = crop.lower().strip()

    # Match crop exactly & pest as substring
    match = df[df['Crop'].str.lower() == crop]
    match = match[match['Pest'].str.lower().str.contains(pest)]

    if not match.empty:
        return match.iloc[0]['Biocontrol Agent'], match.iloc[0]['Usage Method']
    else:
        return "No match found", "Try a different crop/pest"

# App UI
st.set_page_config(page_title="AgriBot - Biocontrol Recommender", layout="centered")
st.title("🌱 AgriBot – Smart Biocontrol Recommendation System")

st.markdown("""
Welcome to **AgriBot**!  
Enter your crop and pest below to get a recommended organic biocontrol agent 🐞🧪  
You can also view analytics of the most common pests and agents 📊
""")

# Inputs
crop = st.text_input("🌿 Enter Crop Name (e.g., Maize):")
pest = st.text_input("🐛 Enter Pest Name (e.g., Stem Borer):")  

# Suggestion
if st.button("🔍 Suggest Agent"):
    agent, usage = suggest_agent(crop, pest)
    st.success(f"✅ Biocontrol Agent: {agent}")
    st.info(f"📌 Usage Instructions: {usage}")

# Visualizations
st.markdown("---")
st.subheader("📊 Pest & Biocontrol Analytics")

if st.checkbox("📌 Show Quick Charts"):
    st.markdown("**Top Reported Pests:**")
    st.bar_chart(df['Pest'].value_counts())

    st.markdown("**Most Recommended Biocontrol Agents:**")
    st.bar_chart(df['Biocontrol Agent'].value_counts())

if st.checkbox("🌟 Show Styled Graphs"):
    # Bar Chart - Pests
    st.markdown("### 🌾 Pest Frequency (Styled)")
    pest_counts = df['Pest'].value_counts()
    fig, ax = plt.subplots()
    pest_counts.plot(kind='bar', color='seagreen', ax=ax)
    ax.set_title("Top Pests Reported")
    ax.set_ylabel("Frequency")
    ax.set_xlabel("Pests")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Pie Chart - Biocontrol Agents
    st.markdown("### 🧬 Biocontrol Agent Usage (Pie Chart)")
    agent_counts = df['Biocontrol Agent'].value_counts()
    fig2, ax2 = plt.subplots()
    agent_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90, ax=ax2)
    ax2.set_ylabel("")
    st.pyplot(fig2)

st.markdown("---")
st.caption("📄 Data source: ICAR-IPM Package for Maize | 💻 Project by Srima 🌾")
