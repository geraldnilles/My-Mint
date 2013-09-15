# Imports
import sys
import cli.account
import cli.transaction
import cli.category
import cli.report

#------------------
# Report Functions
#------------------

def report(db):
	mymint.report.generate(db)
	

def print_help():
	print "Help Info!"

#-------------------
# CLI Argument Parser
#-------------------

def parse():

	try:
		command = sys.argv[1]
	except IndexError:
		print_help()
		return -1
	

	if command == "account":
		return cli.account.parse(sys.argv[2:])
	elif command == "transaction":
		return cli.transaction.parse(sys.argv[2:])
	elif command == "category":
		return cli.category.parse(sys.argv[2:])
	elif command == "report":
		return cli.report.parse(sys.argv[2:])
	else:
		print_help()
		return -1


# Main Function
if __name__ == "__main__":
	parse()


