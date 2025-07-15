import streamlit as st
from add_update_ui import add_update_tab
from analytics_ui import analytics_tab
from monthly_expense_ui import monthly_expense_tab

st.title("Expense Tracking System")

tab1, tab2, tab3 = st.tabs(["Add/Update", "Analytics", "Monthly Summary"])

with tab1:
    add_update_tab()

with tab2:
    analytics_tab()

with tab3:
    monthly_expense_tab()