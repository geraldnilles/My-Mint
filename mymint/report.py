import time
import re

## Generate Transaction Report
#
# Generates a report based on the transaction in the db.  It adds up all of the 
# transactions, prints the sum, and also prints a list of transactions
#
#
def generate(db, days=30):
	# Get all of the transactions
	transactions = db.get_transactions()
	# Get current time
	now = time.time()
	# Create a blank list where you will put your transactions
	recent_transactions = []
	for t in transactions:
		# If transaction is new, add to the recent_transactions list
		if now-t["date"] < days*24*60*60: # Days --> seconds
			recent_transactions.append(t)
	
	print "Reporting based on last %d days, (%d transactions)"%(
				days,
				len(recent_transactions)
			)

	# Get a list of the categories
	categories = db.get_categories()

	

	### Analyze the Transactions
	# Create a report list
	report = []
	for c in categories:
		# Create a report item to add to the report list
		report_item = {}
		report_item["name"] = c["name"]
		report_item["transactions"] = [] 

		# Add matching transactions to the report item
		for t in recent_transactions:
			if matches(t,c):
				report_item["transactions"].append(t)

		# When done searching, add report_item to the report
		report.append(report_item)

	### Look for Uncategorized transactions
	# Create Uncategorized report item
	report_item = {	"name":"uncategorized",
			"transactions":[]}
	# Scan transaction list and add uncategorized to this report_item
	for t in recent_transactions:
		found = False
		# Mark as found if already put in a category
		for r in report:
			if t in r["transactions"]:
				found = True
				break
		# If not found, put it in the uncategorized report item
		if not found:
			report_item["transactions"].append(t)
	
	# Add the report time to the report
	report.append(report_item)

	### Calculate Total for each report item
	for r in report:
		total = 0
		for t in r["transactions"]:
			total += t["amount"]
		
		r["total"] = total

	
	for r in report:
		print "\n"+r["name"]
		for t in r["transactions"]:
			print t["amount"],t["name"]+t["memo"],t["date"]
	for r in report:
		print r["total"],r["name"]
	
	expenses = 0
	for r in report:
		if not (r["name"] in ["uncategorized","Investment","Income"]):
			expenses += r["total"]
	print "\nTotal Expenses:",expenses

def matches(t,c):
	for r in c["rules"]:
		# If the RE match doesnt return None
		if re.search(r,t["name"]+t["memo"],re.IGNORECASE):
			return True

	# If no match, return false
	return False

