import argparse
import mymint.db

def parse(arg_list):

	parser = argparse.ArgumentParser(
			description="Category CLI commands")
	parser.add_argument("-d","--db", required=True)
	parser.add_argument("-r","--remove")
	parser.add_argument("-l","--list", action="store_true")
	parser.add_argument("-a","--add")

	args = parser.parse_args(arg_list)
	db = mymint.db.db(args.db)
	
	if args.remove != None:
		remove(db,args.remove)
	elif args.list:
		list(db)
	elif args.add:
		add(db,args.add)
	else:
		parser.print_help()



def remove(db,name):
	print "Removing Category: %s" % name

	x = db.remove_category(name)
	if x:
		print x
	else:
		print "Category %s does not exist.  Nothing removed." % name

def list(db):
	print "List of Categories"
	for c in db.get_categories():
		print ""
		print c["name"]
		for r in c["rules"]:
			print "\t"+r

## Add a category
def add(db,name):
	print "Adding Category %s to the database" % name
	rule = raw_input("Enter Rule for this category: ")
	db.add_category(name,rule)


