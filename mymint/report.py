


## Generate Transaction Report
#
# Generates a report based on the transaction in the db.  It adds up all of the 
# transactions, prints the sum, and also prints a list of transactions
#
#
def generate_report(db, days=30):
	# Get all of the transactions
	transactions = db.get_transactions()
	# Get current time
	now = time.time()
	# Create a blank list where you will put your transactions
	recent_transactions = []
	for t in transactions:
		# If transaction is new, add to the recent_transactions list
		if abs(now-t["date"]) < days*24*60*60: # Days --> seconds
			recent_transactions.append(t)
	
	# Get a list of the categories
	categories = db.get_categories()

	### Analyze the Transactions
	# Create a report list
	report = []
	for c in categories:
		# Create an item for the report
		report_item = {}
		report_item["name"] = c["name"]
		report_item["transactions"] = [] 

		# Add matching transactions to the report item
		for t in transactions:
			if matches(t,c):
				report_item["transactions"].append(t)

		# When done searching, add report_item to the report
		report.append(report_item)

	### Look for Uncategorized transactions
	# Create Uncategorized report item
	report_item = {	"name":"uncategorized",
			"transactions"=[]}
	# Scan transactions
	for t in transactions:
		found = False
		# Mark as found if already put in a category
		for r in report:
			if t in r["transactions"]:
				found = True
				break
		# If not found, put it in the uncategorized report item
		if not found:
			report_item["transactions"].append(t)
	
	report.append(report_item)

	### Print the report
	for r in report:
		total = 0
		for t in r["transactions"]:
			total += t["amount"]

		print r["name"],total


def matches(t,c):
	for r in c["rules"]:
		# If the RE match doesnt return None
		if re.matches(r,c["name"]):
			return True

	# If no match, return false
	return False

