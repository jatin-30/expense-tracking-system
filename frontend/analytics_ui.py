import streamlit as st
from datetime import datetime
import requests
import pandas as pd
import plotly.express as px

API_URL = "http://localhost:8000"  # ✅ Fixed typo

def analytics_tab():
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime(2024, 8, 1))

    with col2:
        end_date = st.date_input("End Date", datetime(2024, 8, 5))

    if st.button("Get Analytics"):
        payload = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d")
        }

        response = requests.post(f"{API_URL}/analytics/", json=payload)

        if response.status_code == 200:
            response = response.json()
            data = {
                "Category": list(response.keys()),
                "Total": [response[category]["total"] for category in response],
                "Percentage": [response[category]["percentage"] for category in response]
            }

            df = pd.DataFrame(data)
            df_sorted = df.sort_values(by="Percentage", ascending=False)

            st.title("💸 Expense Breakdown by Category")

            fig = px.bar(
                df_sorted,
                x="Category",
                y="Percentage",
                text="Percentage",
                color="Category",
                color_discrete_sequence=px.colors.qualitative.Safe,
                title="Category-wise Expense Distribution (%)"
            )

            fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig.update_layout(
                xaxis_title="Category",
                yaxis_title="Percentage of Total Expenses",
                uniformtext_minsize=8,
                uniformtext_mode='hide',
                template="plotly_dark",
                showlegend=False,
                title_x=0.5
            )

            st.plotly_chart(fig, use_container_width=True)

        else:
            st.error("Failed to fetch analytics data.")
            st.write("Status Code:", response.status_code)
            st.write("Response:", response.text)