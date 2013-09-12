Database
========

# Intorduction
A long JSON string is a very easy database, but it does not grow well.  I would like to create my own database schema based on BDB.

# Overview
The database will consist of Key-Value pairs.  They Key will consist of the ancestors as well as a Unique ID.  The ancestor path will be separated from the UID using the '/' character.  

Lets assume we have a group of accounts.  Each account in this fir group will have the same ancestor of "account".  The key for one of these accoutns might be "account/0123".  Now say we add a new account under that 0123 account.  This accoutn will have a key of "account/0123/4567"

# Searchability
It is important that we can easily search the database.  

For example, say i want to find all transactions between June 1 and June 15.  For this, you would have to find every transaction and see if its data meets the requirement.  

Another example would be to find a transaction from its FITID.  
