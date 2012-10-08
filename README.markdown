# My Mint

Create a web-based personal finance tool written in Python.

# Features
* Fetch Statements from Banks using OFX protocol
* Store transaciton history and balance info
* Create and monitor budgets
* Create and view graphs of spending habbits

# Current-Status
* Can successfully get bank statement data (Tested on Schwab Bank)
* Can successfully get Credit Card statement data (Test on American Express)

# Concept
All of the data will be stored similary to GNUcash where every transaction has a "From" and a "Receive" account assigned to it.  
So when i spend $50 at Meijer, it will be assigned From my credit card account and to the grocery store account.

Accounts can also be nested.  
So there will be 1 expense accont.  
Inside that account will be a Automotive Account.  
Inside that will be a Gas account, an insurance account, and a maintenance account.  
When calculating an account balance, all nested accounts must be tallied up.

The reason this is done instead of categories is because it lets you double check your numbers.
If all of the accounts do not line up, we know there we an issue.  


