# expense_tracker_app.py

import json
import os
from datetime import datetime
import streamlit as st

# Expense Class
class Expense:
    def __init__(self, amount, category, description, date=None):
        self.amount = amount
        self.category = category
        self.description = description
        self.date = date or datetime.now().strftime('%Y-%m-%d')

    def to_dict(self):
        return {
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date
        }

# Expense Tracker Class
class ExpenseTracker:
    def __init__(self, filename="expenses.json"):
        self.filename = filename
        self.expenses = self.load_expenses()

    def load_expenses(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                return json.load(file)
        return []

    def save_expenses(self):
        with open(self.filename, 'w') as file:
            json.dump(self.expenses, file, indent=4)

    def add_expense(self, amount, category, description, date):
        expense = Expense(amount, category, description, date)
        self.expenses.append(expense.to_dict())
        self.save_expenses()

    def delete_expense(self, index):
        if 0 <= index < len(self.expenses):
            del self.expenses[index]
            self.save_expenses()
            return True
        return False

    def total_expenses(self):
        return sum(exp['amount'] for exp in self.expenses)

    def get_expenses(self):
        return self.expenses
    
    def filter_by_month(self, month):
        filtered_expenses = []
        for exp in self.expenses:
            exp_date = datetime.strptime(exp['date'], '%Y-%m-%d')
            if exp_date.month == month:
                filtered_expenses.append(exp)
        return filtered_expenses
    

# Streamlit UI
def main():
    st.set_page_config(page_title="Expense Tracker by Muskan Irfan Ahmed", page_icon="🔍")
    st.title("🔍 Expense Tracker by Muskan Irfan Ahmed ...!")

    tracker = ExpenseTracker()

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["➕ Add Expense", "📋 View Expenses", "🧮 Total", "🗑️ Delete", "🔍 Filter By Month"])

    with tab1:
        st.header("Add a New Expense")
        with st.form("expense_form"):
            amount = st.number_input("Amount (Rs)", min_value=0.0, step=0.01)
            category = st.text_input("Category")
            description = st.text_area("Description")
            date = st.date_input("Date", value=datetime.today())
            submitted = st.form_submit_button("Add Expense")
            if submitted:
                tracker.add_expense(amount, category, description, date.strftime('%Y-%m-%d'))
                st.success("✅ Expense added successfully!")

    with tab2:
        st.header("Your Expenses")
        expenses = tracker.get_expenses()
        if expenses:
            for i, exp in enumerate(expenses, start=1):
                with st.expander(f"{i}. {exp['date']} - {exp['category']} - Rs {exp['amount']}"):
                    st.markdown(f"**Description:** {exp['description']}")
        else:
            st.info("No expenses recorded yet.")

    with tab3:
        st.header("Total Spent")
        total = tracker.total_expenses()
        st.metric("🔍 Total Expenses", f"Rs {total}")

    with tab4:
        st.header("Delete an Expense")
        expenses = tracker.get_expenses()
        if expenses:
            options = [f"{i+1}. {e['date']} - {e['category']} - Rs {e['amount']}" for i, e in enumerate(expenses)]
            to_delete = st.selectbox("Select an expense to delete", options)
            index = options.index(to_delete)
            if st.button("Delete Selected Expense"):
                if tracker.delete_expense(index):
                    st.success("✅ Expense deleted successfully!")
                    st.rerun()
        else:
            st.info("No expenses to delete.")

    with tab5:
        st.header("Filter Expenses by Month")
        month = st.selectbox("Select Month", list(range(1, 13)), format_func=lambda x: datetime(2023, x, 1).strftime('%B'))
        filtered_expenses = tracker.filter_by_month(month)
        if filtered_expenses:
            for i, exp in enumerate(filtered_expenses, start=1):
                with st.expander(f"{i}. {exp['date']} - {exp['category']} - Rs {exp['amount']}"):
                    st.markdown(f"**Description:** {exp['description']}")
        else:
            st.info("No expenses found for this month.")


if __name__ == "__main__":
    main()

#footer
st.write("------")
st.write("✅ Created By Muskan Irfan Ahmed 🎉")    
    
