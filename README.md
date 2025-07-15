# Expense Manager

This project is an **Expense Manager** application that allows users to track their expenses using a Python backend with **FastAPI** and a MySQL database. The frontend is built using **Streamlit** for a simple and interactive user interface.

## Features

- Add or update expenses for a specific date.
- View expenses for a specific date/range of dates.
- Generate expense summaries and analytics for a specified month, grouped by category.

## Backend Setup

The backend is implemented using **FastAPI** and interacts with a **MySQL** database to store and retrieve expense data.

### Requirements

- Python 3.x
- MySQL Server
- Required Python Libraries:
  - `fastapi`
  - `uvicorn`
  - `mysql-connector-python`
  - `pydantic`

### Installation

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up the MySQL database:
    - Create a database called `expense_manager`.
    - Run the following SQL to create the required table:
    
    ```sql
    CREATE TABLE expenses (
        id INT AUTO_INCREMENT PRIMARY KEY,
        expense_date DATE,
        amount DECIMAL(10, 2),
        category VARCHAR(255),
        notes TEXT
    );
    ```

### Running the Backend

To run the FastAPI backend, use **Uvicorn** to start the server:

```bash
uvicorn server:app --reload
