import streamlit as st
import pandas as pd

st.title("Global Seismic Trends Dashboard")
st.write("Interactive Earthquake Analysis")

# Load data
df = pd.read_csv("cleaned_earthquakes.csv")

st.subheader("Earthquake Dataset Preview")
st.dataframe(df.head())

# Sidebar filters
st.sidebar.header("Filter Earthquakes")

selected_years = st.sidebar.multiselect(
    "Select Year",
    options=sorted(df["year"].unique()),
    default=sorted(df["year"].unique())
)

selected_countries = st.sidebar.multiselect(
    "Select Country",
    options=df["country"].unique(),
    default=df["country"].unique()
)

mag_range = st.sidebar.slider(
    "Magnitude Range",
    min_value=float(df["mag"].min()),
    max_value=float(df["mag"].max()),
    value=(4.0, float(df["mag"].max()))
)

# Apply filters
filtered_df = df[
    (df["year"].isin(selected_years)) &
    (df["country"].isin(selected_countries)) &
    (df["mag"] >= mag_range[0]) &
    (df["mag"] <= mag_range[1])
]

st.subheader("Filtered Earthquake Data")
st.dataframe(filtered_df)
st.subheader("Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Earthquakes", len(filtered_df))
col2.metric("Maximum Magnitude", round(filtered_df["mag"].max(), 2))
col3.metric("Average Depth (km)", round(filtered_df["depth_km"].mean(), 2))
st.subheader("Earthquakes per Year")
year_counts = filtered_df.groupby("year").size()
st.bar_chart(year_counts)
st.subheader("Magnitude Distribution")
mag_counts = filtered_df["mag"].round().value_counts().sort_index()
st.bar_chart(mag_counts)
