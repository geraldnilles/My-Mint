import argparse

# import sys



#----------------------
# Command Functions
#----------------------

def account():
	if len(sys.argv) <= 2:
		usage()
		return

	flag = sys.argv[2]
	if flag == "-a":
		print "Add new account to database"
		acct = {}
		acct["bank_id"] = raw_input("Enter the Bank ID. "+
				"This is usually the routing number:")
		acct["acct_type"] = raw_input("Enter the Accout Type "+
				"(CHECKING,SAVINGS,CREDITCARD):")
		acct["acct_it"] = raw_input("Enter the Account Number:")
		acct["username"] = raw_input("Enter the login username:")
		acct["password"] = raw_input("Enter the login password:")
		acct["url"] = raw_input("Enter the OFX server URL:")
		acct["fid"] = raw_input("Enter the bank's FID:")
		acct["org"] = raw_input("Enter the bank's ORG:")
		print acct
	elif flag == "-r":
		print "Remove Account from Database"
	elif flag == "-l":
		print "list all accounts in the database"
	else:
		usage()

def category():
	print "Category Command"

def update():
	print "Update Command"

def report():
	print "Report Command"


## CLI Usage Function
#
# This function prints the correct usage if the "-h" flag is detected.  It also
# shows how to use the CLI if the user fucks up
def usage():
	print """
Commands:
	account	  -  	Add or Remove Accounts
	category  -	Add or Remove Categories
	update	  -	Update the database
	report	  -	Print up a report
	help	  -     Prints this message
	

Account Command
	-a 		Add a new account to the database

	-r <acct_num>	Remove an account provided the account number
	
	-l 		List all of the acccounts

Category Command
	-a 		Add a new category

	-r 		Provide the Regular expression

	-l		List all
"""


## Command Types
#
# THis is alist of legal command types
CMD_TYPES = {	"account":account,
		"category":category,
		"update":update,
		"report":report,
		"help":usage
		}


def parse():
	parser = argparse.ArgumentParser(description="Command Line Interface for the My-Mint project")
	parser.add_argument("command", choices=["account","category",
		"update","report"])
	parser.add_argument("-a","--add", action="store_true")
	parser.add_argument("-r","--remove", nargs="+")
	parser.add_argument("-l","--list", action="store_true")

	print repr(parser.parse_args())



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


