code = """
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Dashboard E-Commerce", layout="wide")

# ======================
# LOAD DATA
# ======================
df = pd.read_csv('dashboard/main_data.csv')

df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
df['order_year'] = df['order_purchase_timestamp'].dt.year
df['order_month'] = df['order_purchase_timestamp'].dt.to_period('M').astype(str)

df['revenue'] = df['price'] + df['freight_value']

st.title("Dashboard Analisis E-Commerce")

# ======================
# FILTER
# ======================
st.sidebar.header("Filter")

year = st.sidebar.selectbox("Pilih Tahun", sorted(df['order_year'].unique()))

df_filtered = df[df['order_year'] == year]

# ======================
# VISUALISASI 1
# ======================
st.subheader("Tren Order & Revenue")

monthly = df_filtered.groupby('order_month').agg({
    'order_id': 'nunique',
    'revenue': 'sum'
}).reset_index()

fig, ax1 = plt.subplots(figsize=(10,5))

ax1.plot(monthly['order_month'], monthly['order_id'], marker='o')
ax1.set_ylabel("Jumlah Order")
ax1.tick_params(axis='x', rotation=45)

ax2 = ax1.twinx()
ax2.plot(monthly['order_month'], monthly['revenue'], linestyle='--', marker='s')
ax2.set_ylabel("Revenue")

st.pyplot(fig)

# ======================
# VISUALISASI 2
# ======================
st.subheader("Top Provinsi")

state = df_filtered.groupby('customer_state')['revenue'].sum().sort_values(ascending=False).head(10)

st.bar_chart(state)

# ======================
# ANALISIS LANJUTAN
# ======================
st.subheader("Repeat Customer")

customer_freq = df_filtered.groupby('customer_unique_id')['order_id'].nunique()

repeat = (customer_freq > 1).sum()
one_time = (customer_freq == 1).sum()

col1, col2 = st.columns(2)

col1.metric("Repeat Customer", repeat)
col2.metric("One-time Buyer", one_time)

fig2, ax = plt.subplots()
ax.pie([one_time, repeat], labels=['One-time', 'Repeat'], autopct='%1.1f%%')

st.pyplot(fig2)
"""

with open("dashboard/dashboard.py", "w") as f:
    f.write(code)

print("dashboard.py berhasil dibuat!")