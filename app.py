import streamlit as st
import pandas as pd
import plotly.express as px

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="PhonePe Insights",
    layout="wide",
    page_icon="📊"
)

# ==============================
# LOAD DATA
# ==============================
@st.cache_data
def load_data():
    df_transaction = pd.read_csv("data/aggregated_transaction.csv")
    df_user = pd.read_csv("data/aggregated_user.csv")
    df_map_trans = pd.read_csv("data/map_transaction.csv")
    df_map_user = pd.read_csv("data/map_user.csv")
    return df_transaction, df_user, df_map_trans, df_map_user

df_transaction, df_user, df_map_trans, df_map_user = load_data()

# ==============================
# SIDEBAR
# ==============================
st.sidebar.title("🔍 Filters")

year = st.sidebar.selectbox(
    "Select Year",
    sorted(df_transaction["year"].unique())
)

state = st.sidebar.selectbox(
    "Select State",
    ["All"] + sorted(df_transaction["state"].unique())
)

# ==============================
# FILTER DATA
# ==============================
df_filtered = df_transaction[df_transaction["year"] == year]

if state != "All":
    df_filtered = df_filtered[df_filtered["state"] == state]

# ==============================
# HEADER
# ==============================
st.title("📊 PhonePe Transaction Insights Dashboard")

st.markdown("""
## 🚀 Where is India spending digitally?

This dashboard uncovers transaction trends, regional performance, and growth opportunities across India.
""")

st.markdown("---")

# ==============================
# KPI SECTION
# ==============================
total_amount = int(df_filtered["transaction_amount"].sum())
total_count = int(df_filtered["transaction_count"].sum())

df_year = df_transaction.groupby("year")["transaction_amount"].sum().sort_index()
growth = df_year.pct_change().iloc[-1] * 100

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Transaction Value", f"{total_amount:,}")
col2.metric("🔢 Total Transactions", f"{total_count:,}")
col3.metric("📈 Growth Rate", f"{growth:.2f}%")

st.markdown("---")

# ==============================
# TOP STATES
# ==============================
df_top_states = (
    df_filtered.groupby("state")["transaction_amount"]
    .sum()
    .sort_values(ascending=False)
)

top_state = df_top_states.index[0]
top_value = int(df_top_states.iloc[0])

st.success(f"🏆 {top_state} is the top-performing state in {year} with ₹{top_value:,}")

# ==============================
# DYNAMIC INSIGHTS
# ==============================
st.subheader("🧠 Key Insights")

st.info(f"""
- {top_state} leads transactions with ₹{top_value:,}, indicating strong digital adoption  
- Overall transaction growth is increasing → expanding market  
- Lower-performing states present expansion opportunities  
""")

st.markdown("---")

# ==============================
# INDIA MAP (Plotly)
# ==============================
st.subheader("🗺️ India Transaction Heatmap")
import json

with open("india_states.geojson") as f:
    geojson = json.load(f)

import json
import requests

# Load GeoJSON properly
geojson_url = "https://raw.githubusercontent.com/plotly/datasets/master/india_states.geojson"
geojson = requests.get(geojson_url).json()

state_data = df_filtered.groupby("state")["transaction_amount"].sum().reset_index()

# CLEAN STATE NAMES (CRITICAL)
state_data["state"] = state_data["state"].str.replace("-", " ").str.title()

# FIX COMMON MISMATCHES
state_data["state"] = state_data["state"].replace({
    "Andaman & Nicobar Islands": "Andaman and Nicobar Islands",
    "Dadra & Nagar Haveli & Daman & Diu": "Dadra and Nagar Haveli and Daman and Diu",
    "Delhi": "Nct Of Delhi"
})

fig = px.choropleth(
    state_data,
    geojson=geojson,
    featureidkey="properties.ST_NM",
    locations="state",
    color="transaction_amount",
    color_continuous_scale="Reds"
)

fig.update_geos(fitbounds="locations", visible=False)

st.plotly_chart(fig, use_container_width=True)# ==============================
# TOP STATES + CATEGORY
# ==============================
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Top States")
    st.bar_chart(df_top_states.head(10))

with col2:
    st.subheader("💳 Category Distribution")
    df_category = (
        df_filtered.groupby("transaction_type")["transaction_amount"]
        .sum()
        .sort_values(ascending=False)
    )
    st.bar_chart(df_category)

st.markdown("---")

# ==============================
# YEARLY TREND
# ==============================
st.subheader("📈 Growth Trend")
st.line_chart(df_year)

st.markdown("---")

# ==============================
# TOP DISTRICTS
# ==============================
st.subheader("📍 Top Districts")

df_map_filtered = df_map_trans[df_map_trans["year"] == year]

if state != "All":
    df_map_filtered = df_map_filtered[df_map_filtered["state"] == state]

df_district = (
    df_map_filtered.groupby("district")["transaction_amount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(df_district)

st.markdown("---")

# ==============================
# STATE DRILLDOWN
# ==============================
if state != "All":
    st.subheader(f"🔍 Deep Dive: {state}")

    state_data = df_transaction[df_transaction["state"] == state]

    st.bar_chart(
        state_data.groupby("transaction_type")["transaction_amount"].sum()
    )

    st.markdown("---")

# ==============================
# USER GROWTH
# ==============================
st.subheader("👥 User Growth")

df_user_growth = df_map_user.groupby("year")["user_count"].sum().sort_index()
st.line_chart(df_user_growth)

st.markdown("---")

# ==============================
# STATE RANKING TABLE
# ==============================
st.subheader("📊 State Rankings")

ranking = (
    df_top_states.reset_index()
)

st.dataframe(ranking, use_container_width=True)

st.markdown("---")

# ==============================
# DECISION SECTION
# ==============================
st.subheader("📌 What Should PhonePe Do?")

st.write(f"""
- Strengthen presence in **{top_state}** for retention and monetization  
- Expand aggressively in lower-performing states  
- Focus on high-performing transaction categories  
- Leverage growth momentum to introduce new financial products  
""")

st.markdown("---")
st.markdown("Built with ❤️ using Streamlit")
