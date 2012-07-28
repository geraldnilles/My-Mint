
The point of this file is to define the SQL database used by MyMint.

There will be 3 tables: Rules, Transactions, and Accounts

# Rules
* ID - Int - Rule ID
* Memo - String - A RegEx to be applied on the memo field
* Account ID - Account ID to be assigned to this transaction if the RegEx Matches
* Min Amount - Float - Minimum amount 
* Max Amount - Float - Maximum amount of the transaction

# Transactions
* ID - Int -  Transaction ID
* From Account - Int - ID Number of the 'from' account
* To Account - Int - ID number of the 'to' account
* Memo - String - Memo for the transaction
* Amount - Float - Amount of money for the transaction.  We will aim to keep this value positive and reverse the From/To numbers to invert any negative numbers

# Accounts
* key - Unique Int - WIll be used internally to identify a list item
* Name - String - Account name
* Parent Account - Int - Points to the account it is appart of.  If it is a root account, set this to -1
* Tags - String - A list of categories.  This is just for easier grouping of accounts for graphing and summaries.  Tags will be separated using commas or semi,colons
* FID	- string - An ID of the financial instidution linked to this account.  This will be required for ODX and QIF importing.  "None" will be the default if not used
* AcctNum - string - The Actual account number used by the FID.  This will also be used during Auto importing. "None" will be the default if not used

