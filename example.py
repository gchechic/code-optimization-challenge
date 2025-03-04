import pandas as pd
import sqlite3
import time
import psutil
from tabulate import tabulate

# Load the CSV files into Pandas dataframes
cards_df = pd.read_csv('sd254_cards.csv')
users_df = pd.read_csv('sd254_users.csv')
transactions_df = pd.read_csv('User0_credit_card_transactions.csv')

# Clean up the 'Amount' column in transactions_df by removing '$' and converting to float
transactions_df['Amount'] = transactions_df['Amount'].replace(r'[\$,]', '', regex=True).astype(float)

users_df['User'] = users_df.index

# Initialize an in-memory SQLite database
conn = sqlite3.connect(':memory:')

# Write the dataframes to SQL tables in the SQLite database
cards_df.to_sql('sd254_cards', conn, index=False, if_exists='replace')
users_df.to_sql('sd254_users', conn, index=False, if_exists='replace')
transactions_df.to_sql('User0_credit_card_transactions', conn, index=False, if_exists='replace')

# Create indexes to optimize query performance
conn.execute("CREATE INDEX idx_users_user ON sd254_users (User)")
conn.execute("CREATE INDEX idx_transactions_user ON User0_credit_card_transactions (User)")
conn.execute("CREATE INDEX idx_transactions_amount ON User0_credit_card_transactions (Amount)")

# Cursor for executing queries
cursor = conn.cursor()

# Function to execute and display query results along with metrics
def execute_query(query, description):
    print(f"Executing: {description}\n")
    
    # Measure execution time
    start_time = time.time()
    
    # Measure resource usage before execution
    process = psutil.Process()
    before_cpu = process.cpu_percent(interval=None)
    before_memory = process.memory_info().rss
    
    # Execute the query and get the execution plan
    explain_query = f"EXPLAIN QUERY PLAN {query}"
    explain_result = pd.read_sql_query(explain_query, conn)
    print("Execution Plan:")
    print(explain_result)
    print("\n" + "-"*50 + "\n")
    
    result = pd.read_sql_query(query, conn)
    
    # Measure resource usage after execution
    after_cpu = process.cpu_percent(interval=None)
    after_memory = process.memory_info().rss
    
    # Calculate metrics
    execution_time = time.time() - start_time
    cpu_usage = after_cpu - before_cpu
    memory_usage = after_memory - before_memory
    
    # Print metrics as a table
    metrics = [
        ["Execution Time (seconds)", f"{execution_time:.4f}"],
        ["CPU Usage (%)", f"{cpu_usage:.2f}"],
        ["Memory Usage (MB)", f"{memory_usage / (1024 * 1024):.2f}"]
    ]
    print(tabulate(metrics, headers=["Metric", "Value"], tablefmt="grid"))
    
    print("Query Result:")
    print(result)
    print("\n" + "-"*50 + "\n")

query_1 = """
SELECT u.User, 
       MAX(c.`Card Number`) as `Card Number`, 
       SUM(t.Amount) as TotalSpent, 
       MAX(t.Amount) as MaxTransaction
FROM sd254_users u
JOIN sd254_cards c ON u.User = c.User
JOIN User0_credit_card_transactions t ON u.User = t.User
WHERE c.`Card Type` = 'Credit'
GROUP BY u.User
HAVING SUM(t.Amount) > 10000;
"""
execute_query(query_1, "Query 1")

query_2 = """
SELECT t.User, t.Amount, t.`Merchant Name`
FROM User0_credit_card_transactions t
JOIN sd254_users u ON t.User = u.User
WHERE u.`Current Age` > 50
AND t.Amount > 500;
"""
execute_query(query_2, "Query 2")

query_3 = """
SELECT u.User, u.`Yearly Income - Person`,
       (SELECT COUNT(*)
        FROM sd254_cards c
        WHERE c.User = u.User) as NumCards
FROM sd254_users u;
"""
execute_query(query_3, "Query 3")

query_4 = """
SELECT DISTINCT u.User, 
       (SELECT SUM(t.Amount)
        FROM User0_credit_card_transactions t
        WHERE t.User = u.User
        AND t.`Merchant State` = 'CA') as TotalSpentInCA
FROM sd254_users u
JOIN User0_credit_card_transactions t ON u.User = t.User
WHERE t.`Merchant State` = 'CA';
"""
execute_query(query_4, "Query 4")

# Close the connection after executing all queries
conn.close()
