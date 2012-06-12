My-Mint
=======

Create a web-based personal finance tool written in Python.

Features
========
- Fetch Statements from Banks using OFX protocol
- Store transaciton history and balance info
- Create and monitor budgets
- Create and view graphs of spending habbits

Current-Status
==============
- Uses aqbanking-cli to perform OFX requests.  I need to figure out how to handle encrypted OFX requests before i can get rid of this binary depedancy

Concept
========
All of the data will be stored similary to GNUcash where every transaction has a "From" and a "Receive" account assigned to it.  So when i spend $50 at Meijer, it will be assigned From my credit card account and to the grocery store account.

Accounts will also be stackable.  So the expenses account can contain multiple accounts inside of it.  


