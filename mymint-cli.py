# Imports
import argparse
import mymint.db
import mymint.ofx_import
import mymint.ofx_server

COMMAND_LIST = [ 
		"account",
		"category",
		"transaction",
		"sync",
		"report"
		]

#----------------------
# Account Functions
#----------------------

## Gather Info and Add Account to database
def account_add(db):
	print "Add new account to database"
	acct = {}
	acct["bank_id"] = raw_input("Enter the Bank ID. "+
			"This is usually the routing number:")
	acct["acct_type"] = raw_input("Enter the Accout Type "+
			"(CHECKING,SAVINGS,CREDITCARD):")
	acct["acct_id"] = raw_input("Enter the Account Number:")
	acct["username"] = raw_input("Enter the login username:")
	acct["password"] = raw_input("Enter the login password:")
	acct["url"] = raw_input("Enter the OFX server URL:")
	acct["fid"] = raw_input("Enter the bank's FID:")
	acct["org"] = raw_input("Enter the bank's ORG:")
	print db.add_account(acct)

## Remove Account from database
def account_remove(db,acct_nums):
	for a in acct_nums:
		print "removing %s"%a

## Print List of accounts
def account_list(db):
	print "Accounts:"

	print db.get_accounts()

#------------------
# Category Functions
#------------------

## Gather Info and Add Category to Database
def category_add(db):
	print "Category Command"
	cat_name = raw_input("Enter the new category name: ")
	rule = raw_input("Enter Matching RegEx Rule: ")
	db.add_category(cat_name,rule)

## Remove Category
def category_remove(db,cat_names):
	for c in cat_names:
		print "Removing Category "+c

## Print a list of categories
def category_list(db):
	print "List of Categories:"
	for c in db.get_categories():
		print c["name"]
		for r in c["rules"]:
			print "\t"+r


#--------------------
# Transaction Functions
#--------------------

## Import an OFX file
def transaction_add(db):
	filename = raw_input("Enter the OFX file to import:")
	f = open(filename,"r")
	data=f.read()
	f.close()

	t = mymint.ofx_import.xml(data)
	print t[10]
	db.add_transaction(t)

	print "Database now contains %d transactions" % len(db.get_transactions())


## Remove a Transaction
def transaction_remove(db,trn_uuids):
	for t in trn_uuids:
		print "Removing Transaction %s" % t

## Print a list of transactions
def transaction_list(db):
	print "Printing a list of transactions"
	for t in db.get_transactions():
		print t["amount"],"\t",t["name"]

#------------------
# Sync Functions
#-----------------

def sync(db):
	print "Sync Transactions:"
	for bank in db.get_accounts():
		print "\t Syncing %s" % bank["acct_id"]
		data = mymint.ofx_server.get_data(bank)
		ts = mymint.ofx_import.xml(data)
		db.add_transaction(ts)

	print "Database now contains %d transactions" % len(db.get_transactions())


#------------------
# Report Functions
#------------------

def report(db):
	print "Report Command"
	

#-------------------
# CLI Argument Parser
#-------------------

def parse():
	parser = argparse.ArgumentParser(description="Command Line Interface for the My-Mint project")
	parser.add_argument("command", metavar="command", choices=COMMAND_LIST, 
		help="Chose the sub-command.  Options include: "+
		"account, category, transaction, sync, and report")
	parser.add_argument("-a","--add", action="store_true")
	parser.add_argument("-r","--remove", nargs="+", metavar="item_id")
	parser.add_argument("-l","--list", action="store_true")
	parser.add_argument("-d","--db", required=True,metavar="database_file.json")

	args = parser.parse_args()

	db = mymint.db.db(args.db)

	# Run Command
	if args.command == "account":
		if args.add:
			account_add(db)
		elif args.remove:
			account_remove(db,args.remove)
		elif args.list:
			account_list(db)
	elif args.command == "category":
		if args.add:
			category_add(db)
		elif args.remove:
			category_remove(db,args.remove)
		elif args.list:
			category_list(db)
	elif args.command == "transaction":
		if args.add:
			transaction_add(db)
		elif args.remove:
			transaction_remove(db,args.remove)
		elif args.list:
			transaction_list(db)
	elif args.command == "sync":
		sync(db)
	elif args.report == "report":
		report(db)
	else:
		parser.print_help()





# Main Function
if __name__ == "__main__":
	parse()


