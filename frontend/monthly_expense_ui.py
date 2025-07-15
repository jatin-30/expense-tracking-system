import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

API_URL = "http://localhost:8000"

def monthly_expense_tab():
    st.title("📆 View Monthly Expenses")

    # Month & Year Selectors
    current_year = datetime.now().year
    years = list(range(2020, current_year + 1))
    months = {
        1: "January", 2: "February", 3: "March", 4: "April",
        5: "May", 6: "June", 7: "July", 8: "August",
        9: "September", 10: "October", 11: "November", 12: "December"
    }

    col1, col2 = st.columns(2)
    with col1:
        selected_year = st.selectbox("Select Year", years, index=len(years) - 1)

    with col2:
        selected_month = st.selectbox("Select Month", list(months.keys()), format_func=lambda x: months[x])

    # Button to trigger the API call
    if st.button("Get Monthly Summary"):
        response = requests.get(f"{API_URL}/monthly-summary/{selected_year}/{selected_month}")

        if response.status_code == 200:
            data = response.json()
            total = data["total"]
            expenses = data["expenses"]

            st.subheader(f"💵 Total Expenses in {months[selected_month]} {selected_year}: ${total:.2f}")

            if expenses:
                df = pd.DataFrame(expenses)

                # Table
                st.dataframe(df[["expense_date", "amount", "category", "notes"]])

                # Bar Graph: category-wise distribution for the month
                category_totals = df.groupby("category")["amount"].sum().reset_index()
                fig = px.bar(
                    category_totals,
                    x="category",
                    y="amount",
                    title="Category-wise Expense Breakdown",
                    labels={"amount": "Total Spent", "category": "Category"},
                    color="category",
                    color_discrete_sequence=px.colors.qualitative.Set2
                )

                fig.update_layout(title_x=0.5, template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No expenses recorded for this month.")
        else:
            st.error("Failed to retrieve data.")
            st.write("Status Code:", response.status_code)
            st.write("Response:", response.text)