import streamlit as st
import pyodbc
import pandas as pd
import datetime

# --- CONFIGURATION ---
# Replace 'YOUR_SERVER_NAME' with your actual SQL Server Name
SERVER_NAME = 'Rahi-D29'
DATABASE_NAME = 'RetailDB'


# --- DATABASE CONNECTION ---
def init_connection():
    """
    Establishes a connection to the MS SQL Database.
    """
    # Check available drivers to find a compatible one
    drivers = [x for x in pyodbc.drivers() if 'SQL Server' in x]
    driver_name = drivers[0] if drivers else 'SQL Server'

    # Connection string with TrustServerCertificate for newer servers
    connection_string = (
        f"DRIVER={{{driver_name}}};"
        f"SERVER={SERVER_NAME};"
        f"DATABASE={DATABASE_NAME};"
        f"Trusted_Connection=yes;"
        f"TrustServerCertificate=yes;"
    )

    try:
        connection = pyodbc.connect(connection_string)
        return connection
    except pyodbc.Error as e:
        st.error(f"❌ Connection Failed: {e}")
        st.stop()


# !!! THIS LINE WAS LIKELY MISSING OR MISPLACED !!!
# We must call the function to create the 'conn' variable globally
conn = init_connection()


# --- HELPER FUNCTIONS ---
def get_products():
    """Fetch all products to populate the dropdown menu"""
    # We use the global 'conn' variable here
    query = "SELECT ProductID, ProductName, Price FROM Products"
    df = pd.read_sql(query, conn)
    return df


def get_customers():
    """Fetch all customers to populate the dropdown menu"""
    query = "SELECT CustomerID, FirstName, LastName FROM Customers"
    df = pd.read_sql(query, conn)
    return df


def insert_sale(product_id, customer_id, quantity, total_amount):
    """Insert a new transaction into the Sales table"""
    cursor = conn.cursor()
    query = """
    INSERT INTO Sales (ProductID, CustomerID, QuantitySold, TotalAmount, SaleDate)
    VALUES (?, ?, ?, ?, ?)
    """
    # Use datetime.datetime.now() to get current time
    cursor.execute(query, (product_id, customer_id, quantity, total_amount, datetime.datetime.now()))
    conn.commit()


# --- STREAMLIT FRONTEND ---
st.title("🛒 Retail Ops Manager")
st.markdown("---")

# 1. SIDEBAR: DATA ENTRY
st.sidebar.header("Log New Sale")

# Load data for dropdowns
try:
    products_df = get_products()
    customers_df = get_customers()

    # Create Dropdowns
    product_list = products_df['ProductName'].tolist()
    selected_product_name = st.sidebar.selectbox("Select Product", product_list)

    customer_list = customers_df['FirstName'] + " " + customers_df['LastName']
    selected_customer_name = st.sidebar.selectbox("Select Customer", customer_list)

    quantity = st.sidebar.number_input("Quantity", min_value=1, value=1)

    # Logic to find IDs and Price based on selection
    if st.sidebar.button("Submit Transaction"):
        # Find the ID and Price of the selected product
        selected_row = products_df[products_df['ProductName'] == selected_product_name].iloc[0]
        product_id = int(selected_row['ProductID'])
        price = float(selected_row['Price'])

        # Calculate Total
        total_amount = price * quantity

        # Find Customer ID
        customer_index = customer_list.tolist().index(selected_customer_name)
        customer_id = int(customers_df.iloc[customer_index]['CustomerID'])

        # Insert into SQL
        insert_sale(product_id, customer_id, quantity, total_amount)
        st.sidebar.success(f"Sale Recorded! Total: ${total_amount}")

        # Rerun to update the table immediately
        st.rerun()

except Exception as e:
    st.error(f"Error loading data: {e}")

# 2. MAIN DASHBOARD: VIEW DATA
st.subheader("📊 Recent Transactions (Live from SQL)")

view_query = """
SELECT TOP 10
    s.SaleID,
    p.ProductName, 
    c.FirstName + ' ' + c.LastName as Customer, 
    s.QuantitySold, 
    s.TotalAmount, 
    s.SaleDate
FROM Sales s
JOIN Products p ON s.ProductID = p.ProductID
JOIN Customers c ON s.CustomerID = c.CustomerID
ORDER BY s.SaleDate DESC
"""

try:
    sales_data = pd.read_sql(view_query, conn)
    st.dataframe(sales_data)
except Exception as e:
    st.warning("No sales found or database error.")

# Refresh Button
if st.button("Refresh Data"):
    st.rerun()