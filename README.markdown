My Mint
=======

# Motivation
Mint.com is a great tool for managing expenses.  However, the fact that this is a "free" internet service concerns me.  I am not sure what they are doing with my data and I'm not sure how safe my bank information is.

# Goal
Create a python program that organizes my expenses.  


# Plan
1. Donwload a List of Transactions from bank servers and store in a database
    * OFX DOwnload Functional.
    * STill need to work on parsing and adding to database
2. Categorize the expenses using a list of rules
3. Display Expenses based on Category
4. Balance the Transactions using the double-entry method

# Technical Details

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

