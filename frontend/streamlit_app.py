
# frontend/streamlit_app.py
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="CHI-311 Copilot", layout="wide")

# --- Header ---
st.title("CHI-311 Copilot")
st.caption("Predictive insights for a smarter, more equitable city.")

# TODO: R3 to fetch this from the /api/refresh_meta endpoint
st.sidebar.info("Data last refreshed: 2025-08-25")

# --- Main App ---
tab1, tab2, tab3 = st.tabs([
    "**Track My Request**", 
    "**Neighborhood Insights**", 
    "**Planner View**"
])

# --- Tab 1: Track My Request ---
with tab1:
    st.header("Track a 311 Service Request")
    sr_number = st.text_input("Enter your Service Request Number (e.g., SR24-12345678)", "")

    if st.button("Track Request") and sr_number:
        # TODO: R3 to call the backend API (e.g., /api/request/{sr} and /api/predict/{sr})
        st.info(f"Fetching details for **{sr_number}**...")
        
        # --- Placeholder Data ---
        st.subheader("Current Status: Open")
        st.metric(label="Estimated Completion Date", value="2025-09-15")
        st.progress(75, text="75% Confidence Interval: Sept 12 - Sept 18")

        with st.expander("See factors influencing this estimate"):
            st.write("**Top Positive Factors (speeding up resolution):**")
            st.success("- Low number of recent requests in Ward 12")
            st.success("- Request type is typically resolved quickly")
            
            st.write("**Top Negative Factors (slowing down resolution):**")
            st.warning("- High backlog of open Pothole requests city-wide")
            st.warning("- Holiday weekend approaching")

    elif sr_number:
        st.write("Click the button to track your request.")

# --- Tab 2: Neighborhood Insights ---
with tab2:
    st.header("Explore Equity and Service Levels")
    col1, col2 = st.columns(2)
    with col1:
        area_type = st.selectbox("View by:", ["Community Area", "Ward"], index=1)
    with col2:
        # TODO: R3 to populate this list from an API call
        area_name = st.selectbox(f"Select a {area_type}:", ["1", "2", "3", "...", "50"], index=0)

    st.write(f"Showing median time-to-close for **Pothole** requests in **Ward {area_name}**.")

    # TODO: R3 to call /api/equity and display real data
    # --- Placeholder Data ---
    st.metric(label=f"Ward {area_name} Median", value="12 days", delta="-2 days vs. city median", delta_color="inverse")
    st.metric(label="Citywide Median", value="14 days")
    st.caption("Based on 1,234 requests in this area over the last 12 months.")

    # --- Placeholder Chart ---
    st.subheader("Median Resolution Time by Category")
    chart_data = pd.DataFrame(
        {
           "Category": ["Potholes", "Streetlights", "Sanitation"],
           f"Ward {area_name}": [12, 18, 25],
           "City Median": [14, 22, 21],
        }
    ).set_index("Category")
    st.bar_chart(chart_data)

# --- Tab 3: Planner View ---
with tab3:
    st.header("City-Wide Operations View")
    st.subheader("Service Request Hotspots (Last 30 Days)")

    # TODO: R3 to call /api/hotspots and use st.map()
    # --- Placeholder Map Data ---
    map_data = pd.DataFrame(
        np.random.randn(5, 2) / [20, 20] + [41.87, -87.62],
        columns=['lat', 'lon'])
    st.map(map_data, zoom=11)
    st.caption("Showing active hotspots for Pothole requests.")

    st.subheader("Backlog & Forecast")
    # TODO: R3 to add KPIs and forecast charts
    col1, col2, col3 = st.columns(3)
    col1.metric("Active Pothole Backlog", "12,405", "+5% vs 7d avg")
    col2.metric("Avg. Resolution Time", "14.2 Days", "-0.5d vs 7d avg", delta_color="inverse")
    col3.metric("14-Day Forecast", "+2,500 New Requests", "-3% vs prior period")

# To run this app:
# streamlit run frontend/streamlit_app.py
