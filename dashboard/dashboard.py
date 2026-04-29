import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np

# ==========================================================
# CONFIG
# ==========================================================
st.set_page_config(
    page_title="E-Commerce Dashboard",
    page_icon="📊",
    layout="wide"
)

sns.set_style("whitegrid")

# ==========================================================
# LOAD DATA
# ==========================================================
@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/main_data.csv")

    # Convert datetime
    datetime_cols = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]

    for col in datetime_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    return df


all_df = load_data()

# ==========================================================
# SIDEBAR
# ==========================================================
st.sidebar.title("📌 Filter Data")

min_date = all_df["order_purchase_timestamp"].min().date()
max_date = all_df["order_purchase_timestamp"].max().date()

date_range = st.sidebar.date_input(
    "Pilih Rentang Waktu",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# supaya aman jika user pilih 1 tanggal
if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date = min_date
    end_date = max_date

main_df = all_df[
    (all_df["order_purchase_timestamp"] >= pd.to_datetime(start_date)) &
    (all_df["order_purchase_timestamp"] <= pd.to_datetime(end_date))
].copy()

# ==========================================================
# HEADER
# ==========================================================
st.title("📊 Dashboard E-Commerce Brazil")
st.markdown("Analisis data Brazilian E-Commerce Public Dataset")

# ==========================================================
# KPI
# ==========================================================
total_orders = main_df["order_id"].nunique()
total_revenue = main_df["price"].sum()
total_customer = main_df["customer_unique_id"].nunique()

avg_order = total_revenue / total_orders if total_orders > 0 else 0

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Orders", f"{total_orders:,}")
col2.metric("Revenue", f"R$ {total_revenue:,.0f}")
col3.metric("Customers", f"{total_customer:,}")
col4.metric("Avg Order Value", f"R$ {avg_order:,.0f}")

st.markdown("---")

# ==========================================================
# PERTANYAAN 1
# ==========================================================
st.header("1️⃣ Monthly Orders & Revenue Trend")

monthly_df = main_df.resample(
    rule="ME",
    on="order_purchase_timestamp"
).agg({
    "order_id": "nunique",
    "price": "sum"
}).reset_index()

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(8,4))
    sns.lineplot(
        data=monthly_df,
        x="order_purchase_timestamp",
        y="order_id",
        marker="o",
        ax=ax
    )
    ax.set_title("Monthly Orders")
    ax.set_xlabel("")
    ax.set_ylabel("Orders")
    plt.xticks(rotation=45)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(8,4))
    sns.lineplot(
        data=monthly_df,
        x="order_purchase_timestamp",
        y="price",
        marker="o",
        ax=ax
    )
    ax.set_title("Monthly Revenue")
    ax.set_xlabel("")
    ax.set_ylabel("Revenue")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# ==========================================================
# PERTANYAAN 2
# ==========================================================
st.header("2️⃣ Province with Highest Revenue")

state_df = main_df.groupby("customer_state").agg({
    "price": "sum"
}).reset_index()

state_df = state_df.sort_values(
    by="price",
    ascending=False
)

fig, ax = plt.subplots(figsize=(10,5))
sns.barplot(
    data=state_df.head(10),
    x="price",
    y="customer_state",
    ax=ax
)
ax.set_title("Top 10 Province Revenue")
ax.set_xlabel("Revenue")
ax.set_ylabel("Province")
st.pyplot(fig)

if len(state_df) > 0:
    top_state = state_df.iloc[0]["customer_state"]
else:
    top_state = "-"

st.success(f"Province with Highest Revenue: {top_state}")

# ==========================================================
# PERTANYAAN 3
# ==========================================================
st.header("3️⃣ RFM Customer Segmentation")

top_df = main_df[
    main_df["customer_state"] == top_state
].copy()

if len(top_df) > 0:

    rfm_df = top_df.groupby("customer_unique_id").agg({
        "order_purchase_timestamp": "max",
        "order_id": "nunique",
        "price": "sum"
    }).reset_index()

    rfm_df.columns = [
        "customer_id",
        "last_order",
        "frequency",
        "monetary"
    ]

    recent_date = top_df["order_purchase_timestamp"].max()

    rfm_df["recency"] = (
        recent_date - rfm_df["last_order"]
    ).dt.days

    # Aman dari duplicate qcut
    rfm_df["R_score"] = pd.qcut(
        rfm_df["recency"].rank(method="first"),
        4,
        labels=[4,3,2,1]
    ).astype(int)

    rfm_df["F_score"] = pd.qcut(
        rfm_df["frequency"].rank(method="first"),
        4,
        labels=[1,2,3,4]
    ).astype(int)

    rfm_df["M_score"] = pd.qcut(
        rfm_df["monetary"].rank(method="first"),
        4,
        labels=[1,2,3,4]
    ).astype(int)

    rfm_df["RFM_score"] = (
        rfm_df["R_score"] +
        rfm_df["F_score"] +
        rfm_df["M_score"]
    )

    rfm_df["segment"] = pd.cut(
        rfm_df["RFM_score"],
        bins=[0,4,7,10,12],
        labels=[
            "At Risk",
            "Potential",
            "Loyal",
            "Top Customer"
        ]
    )

    segment_df = rfm_df.groupby(
        "segment"
    ).size().reset_index(name="customer_count")

    fig, ax = plt.subplots(figsize=(10,5))
    sns.barplot(
        data=segment_df,
        x="customer_count",
        y="segment",
        ax=ax
    )
    ax.set_title(f"RFM Segmentation ({top_state})")
    st.pyplot(fig)

else:
    st.warning("Tidak ada data RFM.")

# ==========================================================
# PERTANYAAN 4
# ==========================================================
st.header("4️⃣ Revenue Distribution All Provinces")

fig, ax = plt.subplots(figsize=(12,7))
sns.barplot(
    data=state_df,
    x="price",
    y="customer_state",
    ax=ax
)
ax.set_title("Revenue by Province")
st.pyplot(fig)

# ==========================================================
# PERTANYAAN 5
# ==========================================================
st.header("5️⃣ Customer Spending Cluster")

if len(top_df) > 0:

    rfm_df["spending_group"] = pd.cut(
        rfm_df["monetary"],
        bins=3,
        labels=[
            "Low Spender",
            "Medium Spender",
            "High Spender"
        ]
    )

    cluster_df = rfm_df.groupby(
        "spending_group"
    ).size().reset_index(name="customer_count")

    fig, ax = plt.subplots(figsize=(10,5))
    sns.barplot(
        data=cluster_df,
        x="spending_group",
        y="customer_count",
        ax=ax
    )
    ax.set_title("Customer Spending Cluster")
    st.pyplot(fig)

else:
    st.warning("Tidak ada data cluster.")

# ==========================================================
# FOOTER
# ==========================================================
st.markdown("---")
st.caption("Created for Dicoding Submission 🚀")