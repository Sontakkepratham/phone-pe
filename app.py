import streamlit as st
import pandas as pd

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
    df_top_trans = pd.read_csv("data/top_transaction.csv")
    return df_transaction, df_user, df_map_trans, df_map_user, df_top_trans

df_transaction, df_user, df_map_trans, df_map_user, df_top_trans = load_data()

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
st.markdown("### 🚀 Turning Data into Business Decisions")

st.markdown("---")

# ==============================
# KPI SECTION
# ==============================
total_amount = int(df_filtered["transaction_amount"].sum())
total_count = int(df_filtered["transaction_count"].sum())

df_year = (
    df_transaction.groupby("year")["transaction_amount"]
    .sum()
    .sort_index()
)

growth = df_year.pct_change().iloc[-1] * 100

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Transaction Value", f"{total_amount:,}")
col2.metric("🔢 Total Transactions", f"{total_count:,}")
col3.metric("📈 Growth Rate", f"{growth:.2f}%")

st.markdown("---")

# ==============================
# INSIGHTS PANEL
# ==============================
st.subheader("🧠 Key Insights")

st.info("""
- A small number of states dominate total transaction volume → high market concentration  
- Digital payment growth is consistently rising → strong adoption trend  
- Transactions are increasing faster than users → higher engagement per user  
- Several districts remain underpenetrated → expansion opportunity  
""")

st.markdown("---")

# ==============================
# TOP STATES + CATEGORY
# ==============================
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Top States")

    df_top_states = (
        df_filtered.groupby("state")["transaction_amount"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    st.bar_chart(df_top_states)

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
st.subheader("📈 Yearly Growth Trend")

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

    st.write("Top Categories in this State:")

    st.bar_chart(
        state_data.groupby("transaction_type")["transaction_amount"].sum()
    )

    st.markdown("---")

# ==============================
# USER GROWTH
# ==============================
st.subheader("👥 User Growth Trend")

df_user_growth = (
    df_map_user.groupby("year")["user_count"]
    .sum()
    .sort_index()
)

st.line_chart(df_user_growth)

st.markdown("---")

# ==============================
# STATE RANKING TABLE
# ==============================
st.subheader("📊 State Rankings")

ranking = (
    df_filtered.groupby("state")["transaction_amount"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

st.dataframe(ranking, use_container_width=True)

# ==============================
# FOOTER
# ==============================
st.markdown("---")
st.markdown("### 📌 Conclusion")
st.markdown("""
This dashboard highlights how digital payments are evolving across India.  
It enables decision-makers to identify high-performing regions, growth trends, and expansion opportunities.
""")

st.markdown("Built with ❤️ using Streamlit")
