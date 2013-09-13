import json, os

## Database Class
#
# This class will manage the My Mint database.  In the current state, this 
# simply stores the database as a JSON string and the entire database is loaded
# in memory every time.  This is not the most efficient method and will need
# to be revised once the transaction database grows.
class db:
	## Constructor
	#
	# Opens or Creates a databased depending on whether or not the file
	# already exists
	def __init__(self, filename):
		self.filename = filename;

		# Load DB into Memory
		if os.path.exists(filename):
			self._open()
		else:
			# if the path does not exist, create a DB
			self.db = {
					"transactions":[],
					"categories":[],
					"accounts":[]
				}


	#--------------------#
	# Private Methods    #
	#--------------------#

	## Save json database to disk as a string
	#
	# Private method for writing the database to the disk.  By making this
	# a separate method, we can prevent needless disk writes
	def _save(self):
		f = open(self.filename,"w")
		json.dump(self.db,f)
		f.close()

	## Load JSON database from the disk to memory
	#
	# Private method fro loading the database to memory
	def _open(self):
		f = open(self.filename,"r")
		self.db = json.load(f)
		f.close()



	## Find the UUID in the database 
	#
	# The UUID is a unique ID for each transaction.  It is a combination of 
	# the bank's ID (FID) and the transactions ID (TID). This string is
	# unique to every transaction in every bank.  This function finds the
	# transaction that has the same UUID (if it exists)
	#
	# @param uuid - The UUID you are looking for
	# @return None if it doesnt exist, otherwise it returns the transaction
	def _find_uuid(self,uuid):
		for t in self.get_transactions():
			if t["uuid"] == uuid:
				return t

		return None


	#-------------------#
	# Retrieval methods #
	#-------------------#

	## Get List of All Transactions
	#
	# @return A list containing transaction dictionaries """ 
	def get_transactions(self):
		return self.db["transactions"]

	## Get List of all Rules
	#
	# @return A List containing rule dictionaries """
	def get_categories(self):
		return self.db["categories"]

	## Get List of accounts
	#
	# @return A list containing Account dictionaries
	def get_accounts(self):
		return self.db["accounts"]

	#------------------#
	# Addition Methods #
	#------------------#

	## Add Transaction(s) to the database
	#
	# This method is given a single transaction or a list of transactions.
	# It parses the transaction(s), checks if it already exists in the 
	# database.  If a transaction exists, it makes sure the info is 
	# up-to-date (sometimes credit-card transaction are modified... like 
	# adding the tip after a meal).  If the transaction does not exist,
	# it adds it to the database
	#
	# @param transaction A single transaction dictionary or a list of 
	# transaction dictionaries
	def add_transaction(self,transaction):
		# Create a container to hold the transactions
		ts = []
		# Checks the format of the transaction
		if self._check_transaction_format(transaction):
			# If the transaction matches the format, then we know
			# this is a single transaction.  It is then added to
			# the ts container
			ts.append(transaction)
		else:
			# If the transaction doesnt match, check if its 
			# the children match
			for t in transaction:
				# If the children match, add them to ts
				if self._check_transaction_format(t):
					ts.append(t)
		# Scan through the ts list, and see if they already exist
		for t in ts:
			t_db = self._find_uuid(t["uuid"])
			if t_db:
				# Update the transaction with the latest data
				t_db["memo"] = t["memo"]
				t_db["amount"] = t["amount"]
			else:
				# Add this T to the db
				self.db["transactions"].append(t)

		# Save Changes to the disk
		self._save()

	

	## Add Category to database
	#
	# Adds a Category to the database if it doesnt already exist.  If it 
	# already exists, add the provided rule to the existing category
	#
	# @param name The name of the Category (string)
	# @param rule The matching rule RegEx for this rule
	# @return 0 if a new category was added.  Return 1 if a new rule was 
	# added
	def add_category(self,name,rule):
		# Check if Category name already exists
		for c in self.db["categories"]:
			if c["name"] == name:
				# Add rule to the Category's rule list and exit
				c["rules"].append(rule)
				self._save()
				return 1

		# Create a new category
		self.db["categories"].append({
				"name":name,
				"rules":[
					rule
				]
			})

		self._save()
		return 0
	
	## Add Account to database
	#
	# @param acct An Account dictionary object to add
	def add_account(self,acct):
		# Check Format
		if not(self._check_account_format(acct)):
			return -1
		
		# Check if accout already exists, return -1
		for a in self.db["accounts"]:
			if acct["acct_id"]==a["acct_id"]:
				return -1

		self.db["accounts"].append(acct)

		self._save()
		return 0


	#-----------------#
	# Removal Methods #
	#-----------------#

	## Remove Transaction from the database 
	#
	# @param uuid The Unique ide of the transaction
	def remove_transaction(self,uuid):
		# Scan through the transactions
		for t in self.db["transactions"]:
			# Remove if UUID matches
			if t["uuid"] == uuid:
				self.db["transaction"].remove(t)

	## Remove a Category from the database
	#
	# @param name the name of the category you want to move 
	def remove_category(self,name):
		# Scan through the categories
		for c in self.db["categories"]:
			# Remove if the name matches
			if c["name"] == name:
				self.db["categories"].remove(c)

	## Remove an account from the database
	#
	# @param acct_id the account number of the account you want to remove
	def remove_account(self,acct_id):
		# Scan through the accounts
		for a in self.db["accounts"]:
			# Remove if the acct_id matches
			if a["acct_id"] == acct_id:
				self.db["accounts"].remove(a)

		

	#----------------#
	# Format Methods #
	#----------------#
	# These methods are used to make sure the user input jibes with 
	# the database format

	## Transaction Prototype
	#
	# This object contains the transactions prototype format.  All 
	# transactions must contain the following fields
	FORMAT_TRANSACTION = {
			"date":str,
			"name":str,
			"memo":str,
			"uuid":str,
			"amount":float
			}
	## Rule Prototype
	#
	# THis object contains the rule prototype format.  All rules must
	# contain the following fields.
	FORMAT_CATEGORY = {
			"name":str,
			"rules":list
			}

	## Bank Protoype
	#
	# This object contains the bank object prototype.  All bank objects 
	# must contain the following fields
	FORMAT_ACCOUNT = {
			"bank_id":str,
			"acct_type":str,
			"acct_id":str,
			"username":str,
			"password":str,
			"url":str,
			"fid":str,
			"org":str
			}


	## Check Transaction Format
	#
	# Checks that the transaction matches the prototype
	#
	# @param transaction Transaction objet you are checking
	# @return Boolean - True if format is correct
	def _check_transaction_format(self,transaction):
		return self._check_format(transaction,self.FORMAT_TRANSACTION)


	## Check Rule Format
	#
	# Checks that the rule matches the prototype
	#
	# @param rule The rule object you are checking
	# @return Returns true if format is correct
	def _check_category_format(self,cat):
		return self._check_format(cat,self.FORMAT_CATEGORY)


	## Check Bank Format
	#
	# Checks that the bank objct matches the prototype
	#
	# @param bank the bank object being checked
	# @return Boolean - True if format is correct
	def _check_account_format(self,bank):
		return self._check_format(bank,self.FORMAT_ACCOUNT)

	## Check Format (Generic Method)
	#
	# Generic Method that check the format of a dictionary
	#
	# @param obj Check the format of this dictionary
	# @param prototype The format prototype you are checking against
	# @return True if obj format matches prototype, else False
	def _check_format(self,obj,prototype):
		# Scan through each object in the prototype
		for field in prototype:
			# if the object contains the field and uses the right
			# type, continue the scan.  Otherwise, kill it
			if ((field in obj) 
				and type(obj[field]) == prototype[field]):
					continue;
			else:
				return False
		return True
	
