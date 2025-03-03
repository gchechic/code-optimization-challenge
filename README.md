<!-- @format -->

# AI Challenge - Code optimization

## Welcome! 👋

This challenge is brought to you by the Endava AI Champions. It’s designed to demonstrate how GitHub Copilot can help optimize SQL queries for better performance.

## Requirements

- Solid SQL knowledge
- License for GitHub Copilot

IMPORTANT: Check the [Artifacts](#expected-artifacts) before start.

## Goal:

Optimize SQL queries to improve performance in a database scenario with card and transaction details. Focus on:

- Analyzing query execution plans
- Creating appropriate indexes
- Rewriting queries for efficiency

## Constraints:

- Use GitHub Copilot as your primary resource for insights and solutions.
- Avoid external searches or official documentation initially.

Important: Commit and push your progress regularly to ensure your work is backed up and accessible.

## The challenge

You are provided with a dataset and we expect you improve the performance of set of queries. The data has almost no obfuscation and is provided in a CSV file This data has more than 20 million transactions generated from a multi-agent virtual world simulation performed by IBM. The data covers 2000 (synthetic) consumers resident in the United States, but who travel the world. The data also covers decades of purchases, and includes multiple cards from many of the consumers. Your task is to optimize the performance of existing SQL queries, specifically focusing on operations like detecting fraudulent transactions and identifying suspicious activities.

Query 1: Retrieve users with at least one credit card, whose total transactions exceed $10,000, along with the highest transaction amount.

```sql
SELECT u.Person, c.`Card Number`,
       (SELECT SUM(t.Amount)
        FROM User0_credit_card_transactions t
        WHERE t.User = u.Person) as TotalSpent,
       (SELECT MAX(t.Amount)
        FROM User0_credit_card_transactions t
        WHERE t.User = u.Person) as MaxTransaction
FROM sd254_users u
JOIN sd254_cards c ON u.Person = c.User
WHERE c.`Card Type` = 'Credit'
AND (SELECT SUM(t.Amount)
     FROM User0_credit_card_transactions t
     WHERE t.User = u.Person) > 10000;
```

Query 2: List all transactions for users over 50 years old, where the transactions exceed $500.

```sql
SELECT t.User, t.Amount, t.`Merchant Name`
FROM User0_credit_card_transactions t
JOIN (
    SELECT u.Person
    FROM sd254_users u
    WHERE u.`Current Age` > 50
) u ON t.User = u.Person
WHERE t.Amount > 500;
```

Query 3: Retrieve the total number of cards issued to each user, along with their yearly income.

```sql
SELECT u.Person, u.`Yearly Income - Person`,
       (SELECT COUNT(*)
        FROM sd254_cards c
        WHERE c.User = u.Person) as NumCards
FROM sd254_users u;
```

Query 4: Find the distinct users who have made transactions at merchants located in 'CA' (California), along with the total amount they spent.exceed $500.

```sql
SELECT DISTINCT u.Person,
       (SELECT SUM(t.Amount)
        FROM User0_credit_card_transactions t
        WHERE t.User = u.Person
        AND t.`Merchant State` = 'CA') as TotalSpentInCA
FROM sd254_users u
JOIN User0_credit_card_transactions t ON u.Person = t.User
WHERE t.`Merchant State` = 'CA';
```

> IMPORTANT: All queries currently use a small set of transactions as examples. Please remember to update the User0_credit_card_transactions table with the full transaction dataset (credit_card_transactions-ibm_v2.csv). Each query contains an issue that you'll need to identify. Use GitHub Copilot and the dataset rows to help you find these issues. Hint: Review the example Python code for guidance.

The expected outcome is a comprehensive optimization of SQL queries. This includes a documented analysis of query execution plans, the impact of indexes, and query rewrites, accompanied by a performance comparison demonstrating the benefits of these optimizations through metrics like execution time and resource usage. Additionally, the outcome provides insights into how Copilot can assist in SQL optimization tasks, from analyzing execution plans to suggesting more efficient query patterns.

Want some support on the challenge? Go to Microsoft Teams and ask questions in the **GitHub Copilot Dev Academy 2024** group.

## Where to find everything

The database can be accessed via the provided [Kaggle dataset](https://www.kaggle.com/datasets/ealtman2019/credit-card-transactions/data).

An example of query implementation is in the root folder. [Python file](./example.py)

## What are you going to practice?

- You will practice optimizing SQL queries by identifying performance bottlenecks and logical errors.
- You will also enhance your skills in using GitHub Copilot to assist in query optimization and problem-solving.

## Building the Challenge - Instructions

1. Set Up

- Clone the repository and create a branch named {your-name}.
- Ensure GitHub Copilot is configured in Visual Studio Code.

2. Analyze Queries

- Use Copilot to review query execution plans and identify issues.
- Document initial metrics (execution time, resource usage).

3. Create Indexes

- Identify columns for indexing and use Copilot to generate CREATE INDEX statements.
- Measure performance improvements after applying indexes.

4. Rewrite Queries

- Use Copilot to suggest optimizations (e.g., restructuring joins, using CTEs).
- Document performance gains.

5. Submit Results

- Submit a Pull Request (PR) with optimized code, performance metrics, and documentation.

## Expected Artifacts

The final deliverable for this challenge should be a Pull Request (PR) submitted to the repository. This PR should include all the code and resources completed during the challenge. It will serve as the primary artifact for reviewing and assessing your work.

> The PR must also include your insights on using GitHub Copilot during the exercise, following the schema below:

```
## Pull Request Title

## Description
- **Technology Used:** Describe the tools, frameworks, or languages you utilized.
- **What I Learned:** Summarize key takeaways or skills acquired during the challenge.
- **Useful Resources:** List any references, articles, or documentation that were helpful.

## Testing
- **Testing Approach:** Outline the strategy used for testing the challenge.
- **Test Methods:** Include details on any unit tests, integration tests, or manual testing performed.

## Visual Evidence
- **GitHub Copilot Interactions:** Attach relevant screenshots, screen recordings, or GIFs that highlight valuable interactions with GitHub Copilot.

## Checklist
- [ ] I have documented relevant GitHub Copilot scenarios (if applicable).
- [ ] The challenge is fully completed.

## Additional Comments
- **Further Insights:** Provide any additional information or notes, such as potential risks, edge cases, or alternative approaches considered.
```

## Feedback on GitHub Copilot

Please include the following in your PR:

- Strengths: How did Copilot help during the challenge?
- Limitations: Where did it struggle?
- Suggestions: How could Copilot improve for SQL optimization?
- Prompt: Revelant/Useful prompts
- Strategies: Approaches to solve the challenge

## Got feedback for us?

We love receiving feedback! We're always looking to improve our process. So if you have anything you'd like to mention, please email us.

**Have fun building!** 🚀
