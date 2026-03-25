# run in terminal using ".\.venv\Scripts\activate" then "streamlit run app.py"

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Product Sales Dashboard", layout="wide")

# 1. Load the Data
try:
    df = pd.read_excel("DataTest.xlsx")
    # Ensure 'Date' is actually handled as a date by Python
    df['Date'] = pd.to_datetime(df['Date'])
except Exception as e:
    st.error(f"Error loading file: {e}")
    st.stop()

# 2. Sidebar Filters
st.sidebar.header("Filter Data")

# Filter by Product
selected_product = st.sidebar.multiselect(
    "Select Product:",
    options=df["Product"].unique(),
    default=df["Product"].unique()
)

# Filter by Region
selected_region = st.sidebar.multiselect(
    "Select Region:",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

# Apply filters to the dataframe
df_filtered = df[
    (df["Product"].isin(selected_product)) & 
    (df["Region"].isin(selected_region))
]

# 3. Main Dashboard
st.title("📊 Sales Performance Dashboard")

# 4. Key Metrics
col1, col2, col3 = st.columns(3)
total_sales = df_filtered["Sales"].sum()
avg_sales = df_filtered["Sales"].mean()
unique_products = df_filtered["Product"].nunique()

col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Average Sale", f"${avg_sales:,.2f}")
col3.metric("Products Count", unique_products)

# 5. Visualizations
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Sales by Product")
    fig_prod = px.bar(df_filtered, x="Product", y="Sales", color="Region", barmode="group")
    st.plotly_chart(fig_prod, use_container_width=True)

with chart_col2:
    st.subheader("Regional Distribution")
    fig_region = px.pie(df_filtered, values="Sales", names="Region", hole=0.4)
    st.plotly_chart(fig_region, use_container_width=True)

# 6. Timeline Chart
st.subheader("Sales Trend Over Time")
fig_line = px.line(df_filtered, x="Date", y="Sales", color="Product", markers=True)
st.plotly_chart(fig_line, use_container_width=True)

# 7. Raw Data
with st.expander("View Raw Filtered Data"):
    st.dataframe(df_filtered, use_container_width=True)