
This document will describe the database file.

# database.json

To make parsing easy, the database will be contained in 1 large json file.  There is an example file called exampleDB.json that has the right format.

The root of this json struction will have 2 entries: "rules" and "accounts".

# rules[]
The rules array will be a list of rules used to auto-assign transactions to accounts.

Each rule will be a dictionary with the following format

{
    name:"Exxon Mobile" // A RegEx to be applied to the Name field.
    memo:"Memo", // A RegEx to be applied to the memo filed
    acctName:"Gas", // Name of account that this will be paired with
    minAmount:"0.00", // Minimum absolute value (optional). 
    maxAmount:"100.00" // Maximum absolute value (optional)
}

TODO Might combine name and memo regex's into 1 string.

# accounts[]

Account objects will be nestable.  For example, Inside teh Expenses account could be an Automotive Account.  With in that could be a Gas and Insurance account.

At the root of the accounts list, there will be the 4 basic accounts: ["Assets","Income","Equity","Expenses", "Liabilities"].

Each account will have the folloiwng format

{

}

IMPORTANT!  Every account must have a unique name.

## transactions[]

Each account will also have a transactions list.  THis contains all of the transactions.

Each transaction will have the following format:
{

}
