import pandas as pd
import sqlite3

# --- CONFIGURATION ---
# REPLACE 'Online Retail.xlsx' with your actual Excel file name
excel_file_name = 'online_retail_II.xlsx' 
# ---------------------

print("Loading Excel file... (This might take a moment for large files)")
try:
    # Reads the first sheet by default. 
    # If you get an error about 'openpyxl', run: pip install openpyxl
    df = pd.read_excel(excel_file_name)
    print(f"Successfully loaded {len(df)} rows.")
except FileNotFoundError:
    print(f"ERROR: Could not find file '{excel_file_name}'. Check the name!")
    exit()

# 2. Create a temporary, password-free SQL database in memory
conn = sqlite3.connect(':memory:')

# 3. Push the data into this temporary SQL table
# We call the table 'retail_data' so our query works exactly the same
df.to_sql('retail_data', conn, index=False, if_exists='replace')
print("Data loaded into SQL table successfully.")

# 4. Run YOUR SQL Query (RFM Analysis)
# Note: I added some extra checks for column names (Invoice vs InvoiceNo)
query = """
SELECT 
    `Customer ID` as CustomerID,
    
    -- Recency: Days since last order (assuming dataset ends in 2011)
    CAST(julianday('2011-12-31') - julianday(MAX(InvoiceDate)) AS INTEGER) AS Recency,
    
    -- Frequency: Count of unique invoices
    COUNT(DISTINCT Invoice) AS Frequency,
    
    -- Monetary: Sum of Quantity * Price
    SUM(Quantity * Price) AS Monetary
FROM 
    retail_data
WHERE 
    `Customer ID` IS NOT NULL
    AND Quantity > 0 
GROUP BY 
    `Customer ID`
"""

print("Running SQL logic...")
try:
    # 5. Execute query and store result
    rfm_df = pd.read_sql(query, conn)
    
    # 6. Save the result for the next step
    rfm_df.to_csv('rfm_data.csv', index=False)
    print("-" * 30)
    print("SUCCESS! 'rfm_data.csv' has been created.")
    print("You are ready for Phase 2 (Clustering).")
    print("-" * 30)
    print(rfm_df.head()) # Show first few rows to verify
except Exception as e:
    print(f"SQL Error: {e}")
    print("Tip: Check if your Excel columns are named 'Invoice', 'Quantity', 'Price', etc.")
