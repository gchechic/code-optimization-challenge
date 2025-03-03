import pandas as pd
import sqlite3

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

# Cursor for executing queries
cursor = conn.cursor()

# Function to execute and display query results
def execute_query(query, description):
    print(f"Executing: {description}\n")
    explain_query = f"EXPLAIN QUERY PLAN {query}"
    explain_result = pd.read_sql_query(explain_query, conn)
    print("Execution Plan:")
    print(explain_result)
    print("\n" + "-"*50 + "\n")
    result = pd.read_sql_query(query, conn)
    print("Query Result:")
    print(result)
    print("\n" + "-"*50 + "\n")

query_1 = """
SELECT u.User, c.`Card Number`, 
       (SELECT SUM(t.Amount)
        FROM User0_credit_card_transactions t
        WHERE t.User = u.User) as TotalSpent,
       (SELECT MAX(t.Amount)
        FROM User0_credit_card_transactions t
        WHERE t.User = u.User) as MaxTransaction
FROM sd254_users u
JOIN sd254_cards c ON u.User = c.User
WHERE c.`Card Type` = 'Credit'
AND (SELECT SUM(t.Amount)
     FROM User0_credit_card_transactions t
     WHERE t.User = u.User) > 10000;
"""
execute_query(query_1, "Query 1")

query_2 = """
SELECT t.User, t.Amount, t.`Merchant Name`
FROM User0_credit_card_transactions t
JOIN (
    SELECT u.User
    FROM sd254_users u
    WHERE u.`Current Age` > 50
) u ON t.User = u.User
WHERE t.Amount > 500;
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
