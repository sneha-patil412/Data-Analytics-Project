import streamlit as st
import pandas as pd
import duckdb  # To run SQL queries on DataFrames
import matplotlib.pyplot as plt

# --- CONFIG & STYLING ---
st.set_page_config(layout="wide", page_title="Ola Data Analytics")

# --- STEP 1: LOAD & CLEAN DATA (existing logic) ---
@st.cache_data  # This makes the app fast by saving data in memory
def load_data():
    file_path = "OLA_Cleaned.xlsx" # Ensure this is in the same folder
    df = pd.read_excel(file_path, sheet_name="July")
    df['Date'] = pd.to_datetime(df['Date'])
    df['Hour'] = df['Date'].dt.hour
    df['Booking_Status'] = df['Booking_Status'].str.strip()
    # Cleaning ratings for SQL calculations
    df['Driver_Ratings'] = pd.to_numeric(df['Driver_Ratings'], errors='coerce')
    df['Customer_Rating'] = pd.to_numeric(df['Customer_Rating'], errors='coerce')
    return df

df = load_data()

# --- SIDEBAR: NAVIGATION ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["SQL Insights", "Visualizations", "Power BI Dashboard"])

# --- PAGE 1: SQL INSIGHTS ---
if page == "SQL Insights":
    st.header("🔍 SQL Query Analysis")
    st.write("Run SQL queries directly on the dataset.")

    # The SQL questions from your project
    query_dict = {
        "1. Retrieve all successful bookings": 
            "SELECT * FROM df WHERE Booking_Status = 'Success'",
        
        "2. Average ride distance for each vehicle type": 
            "SELECT Vehicle_Type, AVG(Ride_Distance) as Avg_Distance FROM df GROUP BY Vehicle_Type",
        
        "3. Total cancelled rides by customers": 
            "SELECT COUNT(*) as Total_Cancelled FROM df WHERE Booking_Status = 'Canceled by Customer'",
        
        "4. Top 5 customers by ride count": 
            "SELECT Customer_ID, COUNT(*) as Total_Rides FROM df GROUP BY Customer_ID ORDER BY Total_Rides DESC LIMIT 5",
        
        "5. Calculate total booking value of successful rides":
            "SELECT SUM(Booking_Value) AS Total_Successful_Revenue FROM df WHERE Booking_Status = 'Success'",
        "6.Rides cancelled by drivers (Personal/Car issues)":
             "SELECT COUNT(*) as Driver_Issues_Cancellations FROM df WHERE Canceled_Rides_by_Driver = 'Personal & Car related issue'",
            
        "7. List all incomplete rides with reasons":
            "SELECT Booking_ID, Incomplete_Rides_Reason FROM df WHERE Incomplete_Rides = 'Yes'",
        
        "8. Average customer rating per vehicle type": 
            "SELECT Vehicle_Type, AVG(Customer_Rating) FROM df GROUP BY Vehicle_Type",

        "9. Max/Min driver ratings for Prime Sedan":
            "SELECT MAX(Driver_Ratings) AS Max_Rating, MIN(Driver_Ratings) AS Min_Rating FROM df WHERE Vehicle_Type = 'Prime Sedan'",

        "10. Retrieve UPI payments":"SELECT * FROM df WHERE Payment_Method = 'UPI'"
    }

    selected_task = st.selectbox("Select an Insight to Extract:", list(query_dict.keys()))
    
    # Execute SQL using DuckDB
    query = query_dict[selected_task]
    result_df = duckdb.query(query).to_df()
    
    st.subheader("Resulting Data")
    st.dataframe(result_df, use_container_width=True)

# --- PAGE 2: VISUALIZATIONS ---
elif page == "Visualizations":
    st.header("📈 Operational Performance Visuals")
    
    # ROW 1: Two Columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Peak Hours for Successful Rides")
        # Filter for successful rides only
        success_df = df[df['Booking_Status'] == "Success"]
        
        fig1, ax1 = plt.subplots()
        success_df['Hour'].value_counts().sort_index().plot(kind='line', marker='o', ax=ax1, color='#f39c12')
        ax1.set_xlabel("Hour of the Day (24h)")
        ax1.set_ylabel("Number of Successes")
        ax1.grid(True, linestyle='--', alpha=0.6)
        st.pyplot(fig1)

    with col2:
        st.subheader("Successful vs. Cancelled Rides")
        # We group all 'Cancelled by...' into one 'Cancelled' category for a cleaner look
        status_map = {
            'Success': 'Successful',
            'Cancelled by Customer': 'Cancelled',
            'Cancelled by Driver': 'Cancelled'
        }
        df['Simple_Status'] = df['Booking_Status'].map(status_map).fillna('Other')
        
        fig2, ax2 = plt.subplots()
        df['Simple_Status'].value_counts().plot(kind='bar', ax=ax2, color=['#2ecc71', '#e74c3c', '#95a5a6'])
        ax2.set_ylabel("Ride Count")
        plt.xticks(rotation=0)
        st.pyplot(fig2)

    st.divider()

    # ROW 2: One Wide Column
    st.subheader("Vehicle Type Popularity (Demand)")
    
    fig3, ax3 = plt.subplots(figsize=(12, 4))
    df['Vehicle_Type'].value_counts().plot(kind='bar', ax=ax3, color='#3498db')
    ax3.set_ylabel("Number of Bookings")
    plt.xticks(rotation=45)
    st.pyplot(fig3)

# --- PAGE 3: POWER BI ---
elif page == "Power BI Dashboard":
    st.header("📊 Power BI Dashboard")
    st.info("Direct hosting requires a work email. Below are the high-resolution exports of the full dashboard suite.")

    # Create 5 tabs for your 5 dashboard pages
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Overall", "Vehicle Type", "Revenue", "Cancellation", "Ratings"
    ])

    with tab1:
        st.subheader("Overall Ride Analysis")
        st.image("overall.png", use_container_width=True)

    with tab2:
        st.subheader("Vehicle Performance")
        st.image("vehicle.png", use_container_width=True)

    with tab3:
        st.subheader("Revenue & Value Insights")
        st.image("revenue.png", use_container_width=True)

    with tab4:
        st.subheader("Cancellation Analysis")
        st.image("cancellation.png", use_container_width=True)

    with tab5:
        st.subheader("Driver & Customer Ratings")
        st.image("rating.png", use_container_width=True)
