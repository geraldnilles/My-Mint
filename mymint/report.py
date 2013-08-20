


## Generate Transaction Report
#
# Generates a report given a list of transactions.  It adds up all of the 
# transactions, prints the sum, and also prints a list of transactions
#
#
def generate_report(db, days=30):
	# Get a list of the last 30 days  of transactions
	# Get a list of the categories
	output = []
	for c in categories:
		cat = {}
		cat["total"] = 0
		cat["name"] = c["name"]
		for t in transactions:
			if re.matches(c["name"],t["name"]):
				cat["total"] += t["ammount"]

	# Sum up the total expenses
	for o in output:
		o["percent"] = o["amount"]/total

		print o["name"],o["percent"]
	

