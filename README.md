# Retail Ops Manager: End-to-End Retail Management System

## 📌 Project Overview
A full-stack data application designed to streamline retail operations. This project integrates a **Python/Streamlit** frontend for real-time transaction logging, an **MS SQL Server** database for robust data storage, and a **Power BI** dashboard for live profitability analysis.

## 🏗️ Tech Stack
* **Frontend:** Python (Streamlit)
* **Backend Logic:** Python (Pandas, PyODBC)
* **Database:** Microsoft SQL Server (Relational Schema, T-SQL)
* **Analytics:** Power BI (DAX, DirectQuery)

## 🚀 Key Features
* **CRUD Operations:** Users can log sales and view transaction history in real-time.
* **Relational Modeling:** Normalized SQL schema linking Products, Customers, and Sales.
* **Business Intelligence:** Custom DAX measures to calculate Net Profit and Profit Margins dynamically.

## 📸 Screenshots
*(Place a screenshot of your Python App here)*
*(Place a screenshot of your Power BI Dashboard here)*

## ⚙️ How to Run
1.  Clone the repo.
2.  Install dependencies: `pip install -r requirements.txt`.
3.  Run the SQL script in `database_setup.sql` to create the tables.
4.  Update `app.py` with your SQL Server credentials.
5.  Run command: `streamlit run app.py`.
