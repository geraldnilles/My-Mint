# My Mint

Create a web-based personal finance tool written in Python.

# Features
* Fetch Statements from Banks using OFX protocol
* Store transaciton history and balance info
* Create and monitor budgets
* Create and view graphs of spending habbits

# Current-Status
- Uses aqbanking-cli to perform OFX requests.  I need to figure out how to handle encrypted OFX requests before i can get rid of this binary depedancy

# Concept
All of the data will be stored similary to GNUcash where every transaction has a "From" and a "Receive" account assigned to it.  So when i spend $50 at Meijer, it will be assigned From my credit card account and to the grocery store account.

Accounts can also be nested.  So there will be 1 expense accont.  Inside that account will be a Automotive Account.  Inside that will be a Gas account, an insurance account, and a maintenance account.  Wen calculating an account balance, all nested accounts must be tallied up.

The reason this is done instead of categories is because it lets you double check your numbers.  


