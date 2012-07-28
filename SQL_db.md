
The point of this file is to define the SQL database used by MyMint.

There will be 3 tables: Rules, Transactions, and Accounts

# Rules
* ID - Int - Rule ID
* Memo - String - A RegEx to be applied on the memo field
* Min Amount - Float - Minimum amount 
* Max Amount - Float - Maximum amount of the transaction

# Transactions
* ID - Int -  Transaction ID
* From Account - Int - ID Number of the 'from' account
* To Account - Int - ID number of the 'to' account
* Memo - String - Memo for the transaction
* Amount - Float - Amount of money for the transaction.  We will aim to keep this value positive and reverse the From/To numbers to invert any negative numbers

# Accounts
* ID - Int - Account ID
* Name - String - Account name
* Parent Account - Int - Points to the account it is appart of.  If it is a root account, set this to -1
* Categories - String - A list of categories.  This is just for easier grouping of accounts for graphing and summaries.


