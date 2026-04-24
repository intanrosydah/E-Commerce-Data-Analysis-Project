import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ======================
# CONFIG
# ======================
st.set_page_config(page_title="Dashboard E-Commerce", layout="wide")

st.title("Dashboard Analisis Data E-Commerce")

# ======================
# LOAD DATA
# ======================
df = pd.read_csv('dashboard/main_data.csv')

# ======================
# PREPROCESSING
# ======================
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])

df['order_year'] = df['order_purchase_timestamp'].dt.year
df['order_month'] = df['order_purchase_timestamp'].dt.to_period('M').astype(str)

df['revenue'] = df['price'] + df['freight_value']

# ======================
# SIDEBAR FILTER
# ======================
st.sidebar.header("Filter Data")

year = st.sidebar.selectbox(
    "Pilih Tahun",
    sorted(df['order_year'].unique())
)

df_filtered = df[df['order_year'] == year]

# ======================
# METRIC RINGKAS
# ======================
st.subheader("Ringkasan")

col1, col2, col3 = st.columns(3)

col1.metric("Total Order", df_filtered['order_id'].nunique())
col2.metric("Total Revenue", f"R$ {df_filtered['revenue'].sum():,.0f}")
col3.metric("Jumlah Pelanggan", df_filtered['customer_unique_id'].nunique())

# ======================
# VISUALISASI 1
# ======================
st.subheader("📈 Tren Bulanan Order & Revenue")

monthly = df_filtered.groupby('order_month').agg({
    'order_id': 'nunique',
    'revenue': 'sum'
}).reset_index()

fig, ax1 = plt.subplots(figsize=(12,5))

ax1.plot(monthly['order_month'], monthly['order_id'], marker='o')
ax1.set_ylabel("Jumlah Order")
ax1.set_xlabel("Bulan")
ax1.tick_params(axis='x', rotation=45)

ax2 = ax1.twinx()
ax2.plot(monthly['order_month'], monthly['revenue'], linestyle='--', marker='s')
ax2.set_ylabel("Revenue")

st.pyplot(fig)

st.write("Insight: Terlihat tren pertumbuhan order dan revenue, namun masih terdapat fluktuasi antar bulan.")

# ======================
# VISUALISASI 2
# ======================
st.subheader("Top 10 Provinsi Berdasarkan Revenue")

state = df_filtered.groupby('customer_state')['revenue'] \
    .sum() \
    .sort_values(ascending=False) \
    .head(10)

st.bar_chart(state)

st.write("Insight: Provinsi dengan revenue tertinggi menjadi pasar utama yang perlu dipertahankan.")

# ======================
# RFM ANALYSIS
# ======================
st.subheader("Analisis RFM (Provinsi Tertinggi)")

# Ambil provinsi tertinggi
top_state = state.index[0]

df_top = df_filtered[df_filtered['customer_state'] == top_state]

max_date = df_top['order_purchase_timestamp'].max()

rfm = df_top.groupby('customer_unique_id').agg({
    'order_purchase_timestamp': lambda x: (max_date - x.max()).days,
    'order_id': 'nunique',
    'revenue': 'sum'
}).rename(columns={
    'order_purchase_timestamp': 'Recency',
    'order_id': 'Frequency',
    'revenue': 'Monetary'
})

# Score
rfm['R_Score'] = pd.qcut(rfm['Recency'], 4, labels=[4,3,2,1])
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 4, labels=[1,2,3,4])
rfm['M_Score'] = pd.qcut(rfm['Monetary'], 4, labels=[1,2,3,4])

rfm['RFM_Score'] = (
    rfm['R_Score'].astype(str) +
    rfm['F_Score'].astype(str) +
    rfm['M_Score'].astype(str)
)

st.write(f"Provinsi dengan revenue tertinggi: **{top_state}**")

fig2, ax = plt.subplots(figsize=(10,4))
rfm['RFM_Score'].value_counts().head(10).plot(kind='bar', ax=ax)
ax.set_title("Top RFM Segment")
st.pyplot(fig2)

# ======================
# REPEAT CUSTOMER
# ======================
st.subheader("Repeat Customer Analysis")

customer_freq = df_filtered.groupby('customer_unique_id')['order_id'].nunique()

repeat = (customer_freq > 1).sum()
one_time = (customer_freq == 1).sum()

col1, col2 = st.columns(2)

col1.metric("Repeat Customer", repeat)
col2.metric("One-time Buyer", one_time)

# Pie chart
fig3, ax = plt.subplots()
ax.pie([one_time, repeat],
       labels=['One-time', 'Repeat'],
       autopct='%1.1f%%')

st.pyplot(fig3)

st.write("Insight: Mayoritas pelanggan masih one-time buyer → peluang besar untuk meningkatkan retensi.")

# ======================
# FOOTER
# ======================
st.markdown("---")
st.write("Dashboard dibuat untuk analisis data e-commerce menggunakan Streamlit.")