import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import numpy as np

# Title and intro
st.set_page_config(page_title="AgriBot: Digital Crop Twin", layout="wide")
st.title("🌾 AgriBot: Digital Twin for Crop Yield Simulation")
st.markdown("📊 This tool uses real historical data to simulate and forecast crop yields based on region, year, and crop type.")

# Load the dataset
@st.cache_data
def load_data():
    df = pd.read_csv("Custom_Crops_yield_Historical_Dataset.csv")
    return df

data = load_data()

# Preview
if st.checkbox("Show Raw Data"):
    st.dataframe(data)

# Select Inputs
crops = data["Crop"].unique()
states = data["State"].unique()
years = sorted(data["Year"].unique())

col1, col2, col3 = st.columns(3)
with col1:
    selected_crop = st.selectbox("Select Crop", crops)
with col2:
    selected_state = st.selectbox("Select State", states)
with col3:
    selected_year = st.selectbox("Select Year", years)

# Filter data
filtered_data = data[(data["Crop"] == selected_crop) & 
                     (data["State"] == selected_state)]

# Visualization
st.subheader(f"📈 Yield Trend for {selected_crop} in {selected_state}")
fig, ax = plt.subplots()
sns.lineplot(data=filtered_data, x="Year", y="Yield", marker="o", ax=ax)
plt.xlabel("Year")
plt.ylabel("Yield (kg/ha)")
plt.grid(True)
st.pyplot(fig)

# Forecasting
st.subheader("🔮 Forecast Future Yield (Linear Regression)")

# Prepare data for prediction
X = filtered_data["Year"].values.reshape(-1, 1)
y = filtered_data["Yield"].values
model = LinearRegression()
model.fit(X, y)

future_years = np.arange(years[-1] + 1, years[-1] + 6).reshape(-1, 1)
future_preds = model.predict(future_years)

forecast_df = pd.DataFrame({
    "Year": future_years.flatten(),
    "Predicted Yield": future_preds
})

st.write(f"📌 Predicted Yield for next 5 years for {selected_crop} in {selected_state}:")
st.dataframe(forecast_df)

fig2, ax2 = plt.subplots()
sns.lineplot(x=filtered_data["Year"], y=filtered_data["Yield"], label="Historical", marker="o", ax=ax2)
sns.lineplot(x=forecast_df["Year"], y=forecast_df["Predicted Yield"], label="Forecast", marker="o", ax=ax2)
plt.xlabel("Year")
plt.ylabel("Yield")
plt.legend()
plt.grid(True)
st.pyplot(fig2)

st.success("✅ Simulation complete using real dataset!")
