import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------
# 🎨 COLOR PALETTE
# ----------------------------
COLORS = {
    "blue": "#007bc2",
    "green": "#00891a",
    "purple": "#74149c",
    "red": "#c10000",
    "orange": "#f45100",
    "yellow": "#f9b928",
    "gray": "#707782"
}

# ----------------------------
# PAGE SETUP
# ----------------------------
st.set_page_config(page_title="Agricultural Dashboard", layout="wide")

st.markdown(
    "<h1 style='color:#00891a;'>🌍 IITA Agricultural KPI Dashboard</h1>",
    unsafe_allow_html=True
)

# ----------------------------
# LOAD DATA
# ----------------------------
df = pd.read_csv("data/fao_data.csv")
df.columns = df.columns.str.strip()

# ----------------------------
# SIDEBAR FILTERS
# ----------------------------
st.sidebar.header("Filters")

crop = st.sidebar.selectbox("Select Crop", df["Crop_Type"].unique())
irrigation = st.sidebar.selectbox("Select Irrigation Type", df["Irrigation_Type"].unique())

filtered_df = df[
    (df["Crop_Type"] == crop) &
    (df["Irrigation_Type"] == irrigation)
]

# ----------------------------
# KPI METRICS (WITH COLOR LOGIC)
# ----------------------------
st.subheader("📈 KPI Summary")

avg_yield = filtered_df["Yield(tons)"].mean()
avg_water = filtered_df["Water_Usage(cubic meters)"].mean()
avg_area = filtered_df["Farm_Area(acres)"].mean()

col1, col2, col3 = st.columns(3)

with col1:
    color = "green" if avg_yield > 30 else "orange" if avg_yield > 15 else "red"
    st.metric("Yield (tons)", round(avg_yield, 2))

with col2:
    color = "red" if avg_water > 80000 else "orange" if avg_water > 60000 else "green"
    st.metric("Water Usage", round(avg_water, 2))

with col3:
    st.metric("Farm Area", round(avg_area, 2))

# ----------------------------
# VISUAL ANALYSIS
# ----------------------------
st.subheader("📊 Visual Analysis")

# Layout in columns (more professional)
col1, col2 = st.columns(2)

# Yield Chart
with col1:
    st.markdown("### 🌿 Yield Trend")

    fig1, ax1 = plt.subplots()
    ax1.plot(
        filtered_df["Yield(tons)"].values,
        color=COLORS["green"],
        linewidth=2
    )
    ax1.set_xlabel("Records")
    ax1.set_ylabel("Yield (tons)")
    ax1.grid(True, linestyle="--", alpha=0.5)

    st.pyplot(fig1)

# Water Usage Chart
with col2:
    st.markdown("### 💧 Water Usage")

    fig2, ax2 = plt.subplots()
    ax2.bar(
        range(len(filtered_df)),
        filtered_df["Water_Usage(cubic meters)"],
        color=COLORS["blue"]
    )
    ax2.set_xlabel("Records")
    ax2.set_ylabel("Water Usage")
    ax2.grid(True, axis="y", linestyle="--", alpha=0.5)

    st.pyplot(fig2)

# ----------------------------
# ADD INSIGHT SECTION (VERY IMPORTANT)
# ----------------------------
st.subheader("🧠 Insights")

if avg_yield > 30:
    st.success("High yield performance observed.")
elif avg_yield > 15:
    st.warning("Moderate yield. There is room for improvement.")
else:
    st.error("Low yield detected. Investigate farming practices.")

if avg_water > 80000:
    st.error("High water usage detected.")
elif avg_water > 60000:
    st.warning("Water usage is moderate.")
else:
    st.success("Efficient water usage.")

# ----------------------------
# RAW DATA
# ----------------------------
if st.checkbox("Show Raw Data"):
    st.subheader("📄 Raw Dataset")
    st.write(df)