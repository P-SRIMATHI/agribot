# Save as app.py and run: streamlit run app.py

import streamlit as st
import pandas as pd

# Load the dataset
df = pd.read_csv("biocontrol_data.csv")

# Suggestion Function
def suggest_agent(crop, pest):
    match = df[(df['Crop'].str.lower() == crop.lower()) &
               (df['Pest'].str.lower() == pest.lower())]
    if not match.empty:
        return match.iloc[0]['Biocontrol Agent'], match.iloc[0]['Usage Method']
    else:
        return "No match found", "Try a different crop/pest"

# UI
st.title("🌱 AgriBot – Organic Biocontrol Recommendation")

crop = st.text_input("Enter Crop Name (e.g., Brinjal):")
pest = st.text_input("Enter Pest Name (e.g., Fruit Borer):")

if st.button("Suggest Agent"):
    agent, usage = suggest_agent(crop, pest)
    st.success(f"Biocontrol Agent: {agent}")
    st.info(f"Usage Instructions: {usage}")

# Optional: Show basic visualizations
if st.checkbox("Show Analytics Charts"):
    st.subheader("📊 Common Pests in Dataset")
    st.bar_chart(df['Pest'].value_counts())

    st.subheader("🧪 Most Suggested Biocontrol Agents")
    st.write(df['Biocontrol Agent'].value_counts())
