import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt
import plotly.express as px

st.title("Retail Sales Analytics Dashboard")
st.sidebar.header("Upload Dataset")

file = st.sidebar.file_uploader("Upload your dataset (CSV)", type=["csv"])  

if file is not None:
    df = pd.read_csv(file)

    # Clean column names (remove spaces)
    df.columns = df.columns.str.strip()

    st.subheader("Dataset Preview:")
    st.write(df)

    # ---------------- KPI Metrics ---------------- #
    # Safe column handling
    total_sales = df['Sales'].sum() if 'Sales' in df.columns else 0
    total_profit = df['Profit'].sum() if 'Profit' in df.columns else 0

    # Handle Order column variations
    if 'Order' in df.columns:
        total_orders = df['Order'].count()
    elif 'Order ID' in df.columns:
        total_orders = df['Order ID'].nunique()
    else:
        total_orders = len(df)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", f"{total_sales:,.2f}")
    col2.metric("Total Profit", f"{total_profit:,.2f}")
    col3.metric("Total Orders", f"{total_orders}")

    # ---------------- Sales by Region ---------------- #
    if 'Region' in df.columns and 'Sales' in df.columns:
        st.subheader("Sales By Region")
        region_sales = df.groupby('Region')['Sales'].sum().reset_index()
        fig1 = px.bar(region_sales, x='Region', y='Sales', color='Region')
        st.plotly_chart(fig1)
    else:
        st.warning("Region/Sales column not found")

    # ---------------- Top Products ---------------- #
    if 'Product' in df.columns and 'Sales' in df.columns:
        st.subheader("Top Selling Products")
        product_sales = df.groupby('Product')['Sales'].sum().reset_index()
        fig2 = px.pie(product_sales, values='Sales', names='Product')
        st.plotly_chart(fig2)
    else:
        st.warning("Product/Sales column not found")

    # ---------------- Profit Analysis ---------------- #
    if all(col in df.columns for col in ['Sales', 'Profit', 'Category']):
        st.subheader("Profit Analysis")
        fig3 = px.scatter(df, x='Sales', y='Profit', color='Category')
        st.plotly_chart(fig3)
    else:
        st.warning("Sales/Profit/Category column missing")

    # ---------------- Sales Trend ---------------- #
    if 'Date' in df.columns and 'Sales' in df.columns:
        st.subheader("Sales Trend")

        df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
        df = df.dropna(subset=['Date'])

        daily_sales = df.groupby('Date')['Sales'].sum().reset_index()
        fig4 = px.line(daily_sales, x='Date', y='Sales')
        st.plotly_chart(fig4)
    else:
        st.warning("Date/Sales column not found")

else:
    st.info("Please upload a CSV file to visualize the sales data.")