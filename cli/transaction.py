import argparse
import mymint.ofx_server
import mymint.ofx_import
import mymint.db

def parse(arg_list):

	parser = argparse.ArgumentParser(
			description="Transaction CLI commands")
	parser.add_argument("-d","--db", required=True)
	parser.add_argument("-s","--sync",action="store_true")
	parser.add_argument("-r","--remove")
	parser.add_argument("-l","--list", action="store_true")
	parser.add_argument("-m","--modify")
	parser.add_argument("-i","--import-ofx")

	args = parser.parse_args(arg_list)
	db = mymint.db.db(args.db)
	
	if args.sync:
		sync(db)
	elif args.remove != None:
		remove(db,args.remove)
	elif args.list:
		list(db)
	elif args.modify:
		modify(db,args.modify)
	elif args.import_ofx:
		import_ofx(db,args.import_ofx)
	else:
		parser.print_help()


def sync(db):
	print "Sync Transactions:"
	for bank in db.get_accounts():
		print "\t Syncing %s" % bank["acct_id"]
		data = mymint.ofx_server.get_data(bank)
		ts = mymint.ofx_import.xml(data)
		db.add_transaction(ts)

	print "Database now contains %d transactions" % len(db.get_transactions())


def remove(db,uid):
	print "Removing transaction: %s" % uid

def list(db):
	print "List of Transactions"
	for t in db.get_transactions():
		print t["amount"],t["name"]+t["memo"],t["date"]

# Modify the given trasnaction
def modify(db,uid):
	print "Modify Transaction %s"% uid


## Import OFX file to database
def import_ofx(db,ofx_file):
	# Read data from OFX file
	f = open(filename,"r")
	data=f.read()
	f.close()

	# Parse as XML
	t = mymint.ofx_import.xml(data)
	# Add Transactions to DB
	db.add_transaction(t)

	print "Transaction imported from %s" % ofx_file
	print "Database now contains %d transactions" % len(db.get_transactions())

