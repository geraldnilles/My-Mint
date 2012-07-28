#!/usr/bin/python




import os,re,urllib

''' Backup
def parse_txt(text):
	theRE =  "transaction {.*?"
	theRE += "date {.*?day=\"([0-9]*?)\".*?month=\"([0-9]*?)\".*?year=\"([0-9]*?)\".*?"
	theRE += "value {.*?value=\"(.*?)\".*?purpose=\"(.*?)\"\n"
	matches = re.findall(theRE,text,re.DOTALL)

	trns = []

	for m in matches:
		t = {}
		t["day"] = int(m[0])
		t["month"] = int(m[1])
		t["year"] = int(m[2])
		t["value"] =m[3]
		t["description"] = m[4]

		t["date"] = "%(year)04d%(month)02d%(day)02d"%t
		t["value"] = t["value"].replace("%2F","/")+".0"
		t["value"] = eval(t["value"])
		t["description"] = urllib.unquote(t["description"].replace("\"",""))

		print t["date"],t["value"],t["description"]
		trns.append(t)

	return trns
'''
	

class MyMint:
	def __init__(self,dbpath):
		## Define the path to the db
		## TODO conver to full system path (/path/to/db.db)
		self.dbpath = dbpath
		if not os.path.exists(self.dbpath):
			self.create_db()

	# This will parse the QIF file and grab transactions. 
	# if accountID is not specified,
	def import_QIF_text(self,text):
		pass

	# This will read a QIF file and call the QIF_text method
	def import_QIF_file(self,qif_path):
		f = open(qif_path,"r")
		self.import_QIF_text(f.read())
		f.close()

	def import_ODX_text(self,text):
		# Look for the Bank and Accnt numbers
		# Verify that there is an accout that matches them
		# If not, return the numbers and ask the user to create an account first.
	
		# Parse each transaction
		trans = []
		# For each Trn
			# Create a dict and add to list

		self.add_transactions(trans)
		pass

	def import_ODX_file(self,odx_path):
		f = open(odx_path,"r")
		self.import_ODX_text(f.read())
		f.close()

	# Download the ODX file from the interwebs, 
	#	then call the import_ODX_text 
	def import_internet(self,accountID):
		pass

	# Apply rules to all transactions that have missing accounts
	def apply_rules(self):
		pass

	# Automatically remove all duplicate transactions
	def autoremove_duplicates(self):
		l = self.list_duplicates()
		## TODO, trim one from each duplicate
		self.delete_transactions(l)

	def autoremove_opposites(self):
		l = self.list_opposites()
		## TODO, Trim one from each opposite pair
		self.delete_transactions(l)
	
	# creates a list of all suspected duplicates
	def list_duplicates(self):
		pass

	# Creates a list of transactions that are the same, but from 
	# 2 different sources.  Example, If is payoff my credit card
	# using my checking account, the same transaction will be 
	# imported by both banks.
	def list_opposites(self):
		pass

	# Deletes all transactions in the transactions list
	def delete_transactions(self,transactions):
		pass

	# Adds a list of transactions.  
	# Each transaction is a dict object
	def add_transactions(self,transactions):
		pass

	def add_account(self,...):
		pass

	def add_rule(self,...):
		pass
		
	
	def create_db(self):
		## SQL Shit

		# Add the 4 Major account groups
		self.add_account("Expenses",-1)
		self.add_account("Liabilities",-1)
		slef.add_account("Equity",-1)	
		self.add_account("Income",-1)



if __name__ == "__main__":
	try:
		opts,args = getopt.getopt(sys.argv[1:],"")
	except getopt.GetoptError, err:
		print str(err)
		usage()
		exit()
	add = {}
	delete = {}
	
	for o,a in opts:
		if o == "-a":
			## Add mode
			pass
		elif o == "-d"
			## delete Mode


