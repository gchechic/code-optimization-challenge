# Before fix
Executing: Query 2

Execution Plan:
   id  parent  notused                                             detail
0   3       0        0                                             SCAN t
1  10       0        0                         BLOOM FILTER ON u (User=?)
2  22       0        0  SEARCH u USING AUTOMATIC PARTIAL COVERING INDE...

--------------------------------------------------

+--------------------------+---------+
| Metric                   |   Value |
+==========================+=========+
| Execution Time (seconds) |  0.0055 |
+--------------------------+---------+
| CPU Usage (%)            |  0      |
+--------------------------+---------+
| Memory Usage (MB)        |  0.07   |
+--------------------------+---------+

# After fix


Executing: Query 2

Execution Plan:
   id  parent  notused                                             detail
0   5       0        0  SEARCH t USING INDEX idx_transactions_amount (...
1   9       0        0       SEARCH u USING INDEX idx_users_user (User=?)

--------------------------------------------------

+--------------------------+---------+
| Metric                   |   Value |
+==========================+=========+
| Execution Time (seconds) |  0.0102 |
+--------------------------+---------+
| CPU Usage (%)            |  0      |
+--------------------------+---------+
| Memory Usage (MB)        |  0.07   |