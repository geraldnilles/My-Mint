import argparse
import mymint.db

COMMAND_LIST = [ 
		"account",
		"category",
		"sync",
		"report"
		]

#----------------------
# Command Functions
#----------------------

## Gather Info and Add Account to database
def account_add(db):
	print "Add new account to database"
	acct = {}
	acct["bank_id"] = raw_input("Enter the Bank ID. "+
			"This is usually the routing number:")
	acct["acct_type"] = raw_input("Enter the Accout Type "+
			"(CHECKING,SAVINGS,CREDITCARD):")
	acct["acct_num"] = raw_input("Enter the Account Number:")
	acct["username"] = raw_input("Enter the login username:")
	acct["password"] = raw_input("Enter the login password:")
	acct["url"] = raw_input("Enter the OFX server URL:")
	acct["fid"] = raw_input("Enter the bank's FID:")
	acct["org"] = raw_input("Enter the bank's ORG:")
	print acct

## Remove Account from database
def account_remove(db,acct_num):
	print "removing %s"%acct_num

## Print List of accounts
def account_list(db):
	print "Accounts:"

	print db.get_accounts()

## Gather Info and Add Category to Database
def category_add(db):
	print "Category Command"
	cat_name = raw_input("Enter the new category name: ")
	rule = raw_input("Enter Matching RegEx Rule: ")
	db.add_category(cat_name,rule)

## Remove Category
def category_remove(db,cat_name):
	print "Removing Category "+cat_name

## Print a list of categories
def category_list(db):
	print "List of Categories:"
	print db.get_categories()

def sync(db):
	print "Update Command"

def report(db):
	print "Report Command"


#-------------------
# CLI Argument Parser
#-------------------

def parse():
	parser = argparse.ArgumentParser(description="Command Line Interface for the My-Mint project")
	parser.add_argument("command", metavar="command", choices=COMMAND_LIST, 
		help="Chose the sub-command.  Options include: "+
		"account, category, sync, and report")
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
	elif args.cocmmand == "sync":
		sync(db)
	elif args.report == "report":
		report(db)





# Main Function
if __name__ == "__main__":
	parse()


