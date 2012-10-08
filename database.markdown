
This document will describe the various JSON files that store all of the financial data.

There will be 3 JSON documents: Rules, Transactions, and Accounts.


Now that i think about it, maybe all of this can be dumped into 1 JSON file?
THe only thing to consider is if the file grows too big, it might require too much memory to run.

This will also make it easier to encrypt and decrypt info

# Rules.json
This file will describe all of the transaction assignment rules.
It will contain a list of dictionaries.
Each dictionary will be a rule described in the list below:

* Memo - String - A RegEx to be applied on the memo field
* AccountID - Account ID to be assigned to this transaction if the RegEx Matches
* MinAmount - Float - Minimum amount 
* MaxAmount - Float - Maximum amount of the transaction

# Transactions.json
This file (or files) will contain all of the transactions.
It will contain a list of dictionaries.
Each dictionary will describe a single transaction.

* TransactionID - A string that uniquely identifies each transaction.  It will likely contain the banks UID and the bank name.
* From Account - Int - ID Number of the 'from' account
* To Account - Int - ID number of the 'to' account
* Memo - String - Memo for the transaction
* Amount - Float - Amount of money for the transaction.  We will aim to keep this value positive and reverse the From/To numbers to invert any negative numbers

# Accounts
This file will contain all of the accounts.
It will contain a dictionary.
Each item of the dictionary will contain another dictionary describing the account

* Name - String - Account name
* Parent Account - Int - Points to the account it is appart of.  If it is a root account, set this to -1
* Tags - String - A list of categories.  This is just for easier grouping of accounts for graphing and summaries.  Tags will be separated using commas or semi,colons
* FID	- string - An ID of the financial instidution linked to this account.  This will be required for ODX and QIF importing.  "None" will be the default if not used
* AcctNum - string - The Actual account number used by the FID.  This will also be used during Auto importing. "None" will be the default if not used

## Format

    {"Accounts":{
        "Income": {
            "Tags":[...],
            "FID":"",
            "AccountNum":"",
            "Accounts":{
                "RIM":{
                    "Tags":[],
                    "FID":
                }
            }
        },
        "Expenses":{
            "Accounts":{
                "Auto":{
                    
                }
            }
        },
        "Liabilities":{
            "Accounts":{
                "Gerald AMEX":{
                    "Tags":[],
                    "FID":""
                }
            }
        }
    }}
