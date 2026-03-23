import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
# ADD DERIVED METRICS
# ----------------------------
filtered_df["Efficiency"] = (
    filtered_df["Yield(tons)"] / filtered_df["Water_Usage(cubic meters)"]
)

# ----------------------------
# KPI METRICS
# ----------------------------
st.subheader("📈 KPI Summary")

avg_yield = filtered_df["Yield(tons)"].mean()
avg_water = filtered_df["Water_Usage(cubic meters)"].mean()
avg_area = filtered_df["Farm_Area(acres)"].mean()
avg_efficiency = filtered_df["Efficiency"].mean()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Yield (tons)", round(avg_yield, 2))

with col2:
    st.metric("Water Usage", round(avg_water, 2))

with col3:
    st.metric("Farm Area", round(avg_area, 2))

with col4:
    st.metric("Efficiency", round(avg_efficiency, 6))

# ----------------------------
# VISUAL ANALYSIS
# ----------------------------
st.subheader("📊 Visual Analysis")

col1, col2 = st.columns(2)

# ----------------------------
# Yield Trend (Meaningful X-axis)
# ----------------------------
with col1:
    st.markdown("### 🌿 Yield by Farm")

    fig1, ax1 = plt.subplots()

    ax1.bar(
        filtered_df["Crop_Type"],  # meaningful category
        filtered_df["Yield(tons)"],
        color=COLORS["green"]
    )

    ax1.set_xlabel("Crop Type")
    ax1.set_ylabel("Yield (tons)")
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(True, axis="y", linestyle="--", alpha=0.5)

    st.pyplot(fig1)

# ----------------------------
# Water vs Yield Relationship
# ----------------------------
with col2:
    st.markdown("### 💧 Water vs Yield")

    fig2, ax2 = plt.subplots()

    ax2.scatter(
        filtered_df["Water_Usage(cubic meters)"],
        filtered_df["Yield(tons)"],
        color=COLORS["blue"]
    )

    ax2.set_xlabel("Water Usage")
    ax2.set_ylabel("Yield (tons)")
    ax2.grid(True)

    st.pyplot(fig2)

# ----------------------------
# CORRELATION HEATMAP
# ----------------------------
st.subheader("🔥 Correlation Heatmap")

fig3, ax3 = plt.subplots()

sns.heatmap(
    filtered_df.corr(numeric_only=True),
    annot=True,
    cmap="coolwarm",
    ax=ax3
)

st.pyplot(fig3)

# ----------------------------
# TOP PERFORMERS
# ----------------------------
st.subheader("🏆 Top Performing Farms")

top_farms = filtered_df.sort_values(
    by="Yield(tons)", ascending=False
).head(5)

st.dataframe(top_farms)

# ----------------------------
# INSIGHTS
# ----------------------------
st.subheader("🧠 Insights")

if avg_yield > 30:
    st.success("High yield performance observed.")
elif avg_yield > 15:
    st.warning("Moderate yield. There is room for improvement.")
else:
    st.error("Low yield detected.")

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
    st.dataframe(df.style.background_gradient(cmap="Greens"))