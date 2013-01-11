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

There will be 5 Master accounts:
* Income - Money you bring in
* Assets - Money in your posession (Bank Accounts)
* Liabilities - Money you owe (Credit Cards)
* Equity - Your overall net worth (Assets - Liabilities).  Your openning balances will fall into this account
* Expenses - Money your spend

Under each of these master accounts will be sub accounts.
THis will help us organize and categorize money flow.

The overal equations are
    Assets - Liabilties = Equity
        and
    Assets - Liabilities = Equity + (Income - Expenses)

So under normal conditions, each master account will have a positive balance.

Each transaction will be entered into 2 different accounts.
This double entry method is a way of verifying that everything balances out right.



## Transaction Examples

### Buying Groceries With Credit card
A positive value will be entered into a Liability Credit Card account.
In addition, a Positive value will also be entered into the Groceries.

Looking at the equations, since Liabilities and Expenses are both negative and both on the opposite side of the equation, the sign will not be inverted.

### Paying Rent with Check
A negative value will be entered in the Assets (checking) account.
While a positive value will be entered in the Rent expense account.

### Paying a credit card bill
A negative value will be entered in the checking account as well as the credit card liability account.
Assets and liabilities are on the same side of the equation but the signs are flipped.  

### Business Expense Credit Card
1. Buy Hotel, Flight, etc.. Using a company credit card.  This is a positive value in Liabilities and a Positive value in Expenses
2. Pay Off Company Credit card using personal checking account.  Negative in assets.  Negative in Liabilities
3. Reembursed by company into personal checking account.  Positive in Assets.  Negative in Expenses.

## Sign Flipping Matrix
<table>
 <tr>
  <th>X</th>
  <th>Asset</th>
  <th>Equity</th>
  <th>Income</th>
  <th>Liability</th>
  <th>Expense</th>
 </tr>
</table>

