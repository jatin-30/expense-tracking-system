import mysql.connector
from contextlib import contextmanager
from logging_setup import setup_logger

logger = setup_logger("db_helper")

@contextmanager
def get_db_cursor(commit=False):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="expense_manager"
    )

    if connection.is_connected():
        print("Connection successful")
    else:
        print("Failed to connect to a database")

    cursor = connection.cursor(dictionary=True)
    yield cursor

    if commit:
        connection.commit()
    cursor.close()
    connection.close()

def fetch_all_records():
    with get_db_cursor(commit=False) as cursor:
        cursor.execute("SELECT * FROM expenses")
        expenses = cursor.fetchall()
        for expense in expenses:
            print(expense)

def fetch_expenses_for_date(expense_date):
    logger.info(f"fetch_expenses_for_date called with {expense_date}")
    with get_db_cursor(commit=False) as cursor:
        cursor.execute("SELECT * FROM expenses WHERE expense_date = %s",(expense_date,))
        expenses = cursor.fetchall()
        for expense in expenses:
            print(expense)
        return expenses

def insert_expense(expense_date,amount,category,notes):
    logger.info(f"insert_expense called with {expense_date}, amount:{amount}, category:{category}, notes:{notes}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)",
            (expense_date, amount, category, notes)
        )

def delete_expenses_for_data(expense_data):
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date = %s",(expense_data,))

def fetch_expense_summary(start_date, end_date):
    logger.info(f"fetch_expense_summary called with start:{start_date}, end:{end_date}")
    with get_db_cursor(commit=False) as cursor:
        cursor.execute(
            '''SELECT category, SUM(amount) as total
               FROM expenses WHERE expense_date
               BETWEEN %s and %s
               GROUP BY category;''',
            (start_date, end_date)
        )
        data = cursor.fetchall()
        return data

def fetch_expenses_for_month(year, month):
    logger.info(f"fetch_expenses_for_month called with year:{year}, month:{month}")
    with get_db_cursor(commit=False) as cursor:
        cursor.execute(
            '''
            SELECT * FROM expenses
            WHERE YEAR(expense_date) = %s AND MONTH(expense_date) = %s
            ''',
            (year, month)
        )
        data = cursor.fetchall()
        return data

if __name__ == "__main__":
    # fetch_all_records()
    # fetch_expenses_for_date("2024-08-01")
    # insert_expense("2024-08-26","320","Food","Panipuri")
    # fetch_expenses_for_date("2024-08-26")
    # delete_expenses_for_data("2024-08-26")
    # fetch_expenses_for_date("2024-08-26")
    summary = fetch_expense_summary("2024-08-01","2024-08-05")
    for items in summary:
        print(items)