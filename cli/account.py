#-----------------
# Account CLI
#
# Parses account CLI commands
#-------------------

import argparse
import mymint.db

def parse(arg_list):
	parser = argparse.ArgumentParser(description="Account Argument Parser")
	parser.add_argument("-a","--add", action="store_true")
	parser.add_argument("-r","--remove")
	parser.add_argument("-l","--list", action="store_true")
	parser.add_argument("-m","--modify")
	parser.add_argument("-d","--db", required=True,metavar="database_file.json")

	args = parser.parse_args(arg_list)

	db = mymint.db.db(args.db)


	if args.add:
		add(db)
	elif args.remove != None:
		remove(db,args.remove)
	elif args.list:
		list(db)
	elif args.modify:
		modify(db,args.modify)
	else:
		parser.print_help()



## Gather Info and Add Account to database
def add(db):
	print "Add new account to database"
	acct = {}
	
	acct["acct_type"] = raw_input("Enter the Accout Type "+
			"(CHECKING,SAVINGS,CREDITCARD):")
	if acct["acct_type"] in ["CHECKING","SAVINGS"]:	
		acct["bank_id"] = raw_input("Enter the Bank ID. "+
			"This is usually the routing number:")
	acct["acct_id"] = raw_input("Enter the Account Number:")
	acct["username"] = raw_input("Enter the login username:")
	acct["password"] = raw_input("Enter the login password:")
	acct["url"] = raw_input("Enter the OFX server URL:")
	acct["fid"] = raw_input("Enter the bank's FID:")
	acct["org"] = raw_input("Enter the bank's ORG:")
	print db.add_account(acct)

## Remove Account from database
def remove(db,acct_id):
	print "Removing Acct ID: %s" % acct_id

## Print List of accounts
def list(db):
	print "Accounts:"

	for a in db.get_accounts():
		b = sorted(a)
		print ""
		print a["acct_id"]
		for key in b:
			print "\t"+key+": "+a[key]


## Modify an Account
def modify(db, acct_id):
	print "Modify Account: %s"%acct_id

	
	
	
