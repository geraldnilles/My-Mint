import argparse


COMMAND_LIST = [ 
		"account",
		"category",
		"update",
		"report"
		]

#----------------------
# Command Functions
#----------------------

## Gather Info and Add Account to database
def account_add():
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
def account_remove(acct_num):
	print "removing %s"%acct_num

## Print List of accounts
def account_list():
	print "A list of accounts"

## Gather Info and Add Category to Database
def category_add():
	print "Category Command"
	cat_name = raw_input("Enter the new category name: ")
	rule = raw_input("Enter Matching RegEx Rule: ")

## Remove Category
def category_remove(cat_name):
	print "Removing Category "+cat_name

## Print a list of categories
def category_list():
	print "A list of categories and their rules"

def update():
	print "Update Command"

def report():
	print "Report Command"


#-------------------
# CLI Argument Parser
#-------------------

def parse():
	parser = argparse.ArgumentParser(description="Command Line Interface for the My-Mint project")
	parser.add_argument("command", metavar="command", choices=COMMAND_LIST, 
		help="Chose the sub-command.  Options include: "+
		"account, category, update, and report")
	parser.add_argument("-a","--add", action="store_true")
	parser.add_argument("-r","--remove", nargs="+", metavar="item_id")
	parser.add_argument("-l","--list", action="store_true")

	args = parser.parse_args()

	# Run Command
	if args.command == "account":
		if args.add:
			account_add()
		elif args.remove:
			account_remove(args.remove)
		elif args.list:
			account_list()
	elif args.command == "category":
		if args.add:
			category_add()
		elif args.remove:
			category_remove(args.remove)
		elif args.list:
			category_list()
	elif args.cocmmand == "update":
		update()
	elif args.report == "report":
		report()





# Main Function
if __name__ == "__main__":
	parse()
	exit()
	# Parse the Command Type
	if len(sys.argv) <= 1:
		print "No Commend Specified: \n\n"
		usage()
	else:
		cmd_t = sys.argv[1]
		# Verify Command TYpe is legal
		if cmd_t in CMD_TYPES:
			CMD_TYPES[cmd_t]()
		else:
			usage()


