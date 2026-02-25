import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="OLA Ride Analytics",
    page_icon="🚕",
    layout="wide"
)

# -----------------------------
# Background Style
# -----------------------------
st.markdown(
    """
    <style>
    .stApp { background-color: #EAF2FF; }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Sidebar Navigation
# -----------------------------
page = st.sidebar.selectbox(
    "Navigate",
    ["Home", "SQL Query Explorer"]
)

# -----------------------------
# Load Data
# -----------------------------
df = pd.read_csv("ola_cleaned_data.csv")

# ==================================================
# HOME PAGE
# ==================================================
if page == "Home":

    st.title("🚕 OLA Ride Analytics Application")

    st.markdown("""
    ### 📌 Project Overview
    This Streamlit application provides interactive analytics on **OLA ride data**.
    It demonstrates how **SQL, Python, Power BI, and Streamlit** work together
    in a real-world analytics project.
    """)

    st.markdown("""
    ### 🛠 Tools & Technologies
    - SQL  
    - Python (Pandas)  
    - Power BI  
    - Streamlit  
    """)

    st.markdown("""
    ### 📊 What You Can Explore
    ✔ SQL query results  
    ✔ Interactive visualizations  
    ✔ Business insights  
    ✔ Power BI dashboards  
    """)
    st.markdown("### 🧭 How This Application Works")

    st.markdown("""
    1️⃣ Navigate using the **sidebar**  
    2️⃣ Select a **SQL query** in Query Explorer  
    3️⃣ View **query results & visualizations**  
    4️⃣ Analyze **business insights**  
    5️⃣ Explore **Power BI dashboards & reports**
    """)
    st.markdown("### 🚀 Why This Project Matters")

    st.markdown("""
    This project simulates a **real-world analytics workflow** where:
    - Raw data is cleaned using **Python**
    - Business questions are answered using **SQL**
    - Insights are visualized using **Power BI**
    - Results are presented through an **interactive Streamlit app**
    """)

    st.info("👉 Use the sidebar to open **SQL Query Explorer**")

# ==================================================
# SQL QUERY EXPLORER
# ==================================================
elif page == "SQL Query Explorer":

    st.title("📊 SQL Query Explorer")
    st.caption("Select a query to view results, visualization, and business insight.")

    # -----------------------------
    # KPI CARDS
    # -----------------------------
    total_rides = len(df)
    successful_rides = df[df["Booking_Status"] == "Success"].shape[0]
    cust_cancel = df[df["Booking_Status"] == "Cancelled by Customer"].shape[0]
    drv_cancel = df[df["Booking_Status"] == "Cancelled by Driver"].shape[0]
    revenue = df[df["Booking_Status"] == "Success"]["Booking_Value"].sum()

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Rides", total_rides)
    c2.metric("Successful", successful_rides)
    c3.metric("Customer Cancellation", cust_cancel)
    c4.metric("Driver Cancellation", drv_cancel)
    c5.metric("Revenue", f"₹ {revenue/1_000_000:.1f} M")

    st.divider()

    # -----------------------------
    # SQL QUERY DATA
    # -----------------------------
    queries = {
        "1. Successful bookings":
            df[df["Booking_Status"] == "Success"],

        "2. Avg ride distance per vehicle type":
            df.groupby("Vehicle_Type")["Ride_Distance"].mean().reset_index(),

        "3. Cancelled rides by customers":
            df[df["Booking_Status"] == "Cancelled by Customer"],

        "4. Top 5 customers by ride count":
            df["Customer_ID"].value_counts().head(5).reset_index(name="Ride_Count"),

        "5. Cancelled rides by drivers":
            df[df["Booking_Status"] == "Cancelled by Driver"],

        "6. Driver ratings (Prime Sedan)":
            df[df["Vehicle_Type"] == "Prime Sedan"]
            .agg(Max_Rating=("Driver_Ratings", "max"),
                 Min_Rating=("Driver_Ratings", "min"))
            .reset_index(),

        "7. Rides paid via UPI":
            df[df["Payment_Method"] == "UPI"],

        "8. Avg customer rating per vehicle type":
            df.groupby("Vehicle_Type")["Customer_Rating"].mean().reset_index(),

        "9. Total revenue from completed rides":
            pd.DataFrame({"Total_Revenue": [revenue]}),

        "10. Incomplete rides by reason":
            df[df["Booking_Status"]
               .isin(["Cancelled by Driver", "Cancelled by Customer", "Driver Not Found"])]
            ["Booking_Status"]
            .value_counts()
            .reset_index(name="Count")
    }

    # -----------------------------
    # SINGLE SELECTBOX
    # -----------------------------
    selected_query = st.selectbox(
        "🔎 Select SQL Query",
        list(queries.keys())
    )

    result_df = queries[selected_query]

    # -----------------------------
    # RESULT TABLE
    # -----------------------------
    st.subheader("🧾 Query Result")
    st.dataframe(result_df, use_container_width=True)

    # -----------------------------
    # VISUALIZATION (ALWAYS SHOWN)
    # -----------------------------
    st.subheader("📈 Visualization")

    if selected_query == "2. Avg ride distance per vehicle type":
        fig = px.bar(result_df, x="Vehicle_Type", y="Ride_Distance")

    elif selected_query == "4. Top 5 customers by ride count":
        fig = px.bar(result_df, x="Customer_ID", y="Ride_Count")

    elif selected_query == "8. Avg customer rating per vehicle type":
        fig = px.line(result_df, x="Vehicle_Type", y="Customer_Rating", markers=True)

    elif selected_query == "10. Incomplete rides by reason":
        fig = px.bar(result_df, x="Booking_Status", y="Count")

    else:
        fig = px.histogram(df, x="Vehicle_Type", color="Vehicle_Type")

    st.plotly_chart(fig, use_container_width=True)

    # -----------------------------
    # KEY INSIGHT (ALWAYS SHOWN)
    # -----------------------------
    st.subheader("💡 Key Insight")

    if selected_query == "1. Successful bookings":
        st.info(f"{len(result_df)} rides were completed successfully.")

    elif selected_query == "2. Avg ride distance per vehicle type":
        top = result_df.sort_values("Ride_Distance", ascending=False).iloc[0]
        st.info(f"{top['Vehicle_Type']} is used for longer rides on average.")

    elif selected_query == "3. Cancelled rides by customers":
        st.info(f"{len(result_df)} rides were cancelled by customers.")

    elif selected_query == "4. Top 5 customers by ride count":
        st.info("A small group of customers contributes a large share of rides.")

    elif selected_query == "5. Cancelled rides by drivers":
        st.info(f"{len(result_df)} rides were cancelled by drivers.")

    elif selected_query == "6. Driver ratings (Prime Sedan)":
        st.info("Prime Sedan drivers maintain high rating consistency.")

    elif selected_query == "7. Rides paid via UPI":
        st.info("UPI is a highly preferred payment method.")

    elif selected_query == "8. Avg customer rating per vehicle type":
        st.info("Customer satisfaction varies by vehicle category.")

    elif selected_query == "9. Total revenue from completed rides":
        st.info(f"Total revenue generated is ₹{revenue:,.0f}.")

    elif selected_query == "10. Incomplete rides by reason":
        st.info("Cancellations are the main reason for incomplete rides.")

    # -----------------------------
    # POWER BI SECTION
    # -----------------------------
    st.divider()
    st.markdown("## 📊 Power BI Dashboards")

    dashboards = [
        "Overall Performance.png",
        "Vehicle Type Performance Analysis.png",
        "Cancellation Analysis – Customer vs Driver.png",
        "Revenue & Payment Analysis.png",
        "Ratings & Service Quality Analysis.png",
    ]

    for img in dashboards:
        st.image(img, use_container_width=True)

    st.markdown("## 🎥 Dashboard Walkthrough Video")
    st.video("ola_dashboard_demo.mp4")

    st.markdown("## 📦 Power BI Files")

    with open("Ola_PowerBI_Dashboard.pbix", "rb") as f:
        st.download_button(
            "⬇️ Download Power BI (.pbix)",
            f,
            file_name="Ola_PowerBI_Dashboard.pbix"
        )

    st.markdown("## 📄 Project Documentation")

    with open("Ola_PowerBI_Project_Documentation.pdf", "rb") as f:
        st.download_button(
            "📄 Download Documentation (PDF)",
            f,
            file_name="Ola_PowerBI_Project_Documentation.pdf"
        )