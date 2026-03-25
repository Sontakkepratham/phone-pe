import streamlit as st
import pandas as pd

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(page_title="PhonePe Insights", layout="wide")

st.title("📊 PhonePe Transaction Insights Dashboard")
st.markdown("Analyze digital payment trends across India")

# ==============================
# LOAD DATA
# ==============================
@st.cache_data
def load_data():
    df_transaction = pd.read_csv("data/aggregated_transaction.csv")
    df_user = pd.read_csv("data/aggregated_user.csv")
    df_map_trans = pd.read_csv("data/map_transaction.csv")
    df_map_user = pd.read_csv("data/map_user.csv")
    df_top_trans = pd.read_csv("data/top_transaction.csv")
    return df_transaction, df_user, df_map_trans, df_map_user, df_top_trans

df_transaction, df_user, df_map_trans, df_map_user, df_top_trans = load_data()

# ==============================
# SIDEBAR FILTERS
# ==============================
st.sidebar.header("🔍 Filters")

year = st.sidebar.selectbox(
    "Select Year",
    sorted(df_transaction["year"].unique())
)

state = st.sidebar.selectbox(
    "Select State",
    ["All"] + sorted(df_transaction["state"].unique())
)

# Apply filters
df_filtered = df_transaction[df_transaction["year"] == year]

if state != "All":
    df_filtered = df_filtered[df_filtered["state"] == state]

# ==============================
# KPI SECTION
# ==============================
total_amount = int(df_filtered["transaction_amount"].sum())
total_count = int(df_filtered["transaction_count"].sum())

col1, col2 = st.columns(2)

col1.metric("💰 Total Transaction Amount", f"{total_amount:,}")
col2.metric("🔢 Total Transaction Count", f"{total_count:,}")

# ==============================
# TOP STATES
# ==============================
st.subheader("🏆 Top States by Transaction Value")

df_top_states = (
    df_filtered.groupby("state")["transaction_amount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(df_top_states)

st.write("Insight: A few states dominate transactions → strong market concentration")

# ==============================
# CATEGORY DISTRIBUTION
# ==============================
st.subheader("💳 Transaction by Category")

df_category = (
    df_filtered.groupby("transaction_type")["transaction_amount"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(df_category)

st.write("Insight: Certain categories drive majority of revenue → focus areas for growth")

# ==============================
# YEARLY TREND
# ==============================
st.subheader("📈 Yearly Growth Trend")

df_year = (
    df_transaction.groupby("year")["transaction_amount"]
    .sum()
    .sort_index()
)

st.line_chart(df_year)

st.write("Insight: Consistent growth indicates increasing digital adoption")

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

st.write("Insight: High-performing districts indicate strong micro-markets")

# ==============================
# USER GROWTH
# ==============================
st.subheader("👥 User Growth")

df_user_growth = (
    df_map_user.groupby("year")["user_count"]
    .sum()
    .sort_index()
)

st.line_chart(df_user_growth)

st.write("Insight: User growth vs transaction growth shows engagement depth")

# ==============================
# FOOTER
# ==============================
st.markdown("---")
st.markdown("Built using Streamlit | Data Source: PhonePe Pulse")
