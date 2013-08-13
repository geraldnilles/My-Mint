import json

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
			self.db = {
					"transactions":[],
					"rules":[]
				}


	#--------------------#
	# Private Methods    #
	#--------------------#

	## Save json database to disk as a string
	#
	# Private method for writing the database to the disk.  By making this
	# a separate method, we can prevent needless disk writes
	def _save(self):
		json.dump(self.filename, self.db)

	## Load JSON database from the disk to memory
	#
	# Private method fro loading the database to memory
	def _open(self):
		self.db(json.load(self.filename))

	## Determine if transaction matches the rule
	#	
	# Private method that compares a transaction and a rule and determines
	# if they match.  If so, the method returns True
	#
	# @param transaction - A transaction dictionary object
	# @param rule - A Rule Dictionary object
	# @return  True if the rule matches the transaction 
	def _matches(self,transaction,rule):
		# Check if the memo string matches
		memo = re.matches(rule["memo"],transaction["memo"])
		# TODO Check if the amount range matches
		amount = True
		return memo and amount

	""" @brief Find the UUID in the database 
	
	The UUID is a unique ID for each transaction.  It is a combination of 
	the bank's ID (FID) and the transactions ID (TID).  This number will be
	unique to every transaction in every bank.

	@param uuid - The UUID you are looking for
	@return None if it doesnt exist, otherwise, it returns the transaction """
	def _find_uuid(self,uuid):
		for t in self.get_all_transaction():
			if t["uuid"] == uuid:
				return t

		return None


	#-------------------#
	# Retrieval methods #
	#-------------------#

	""" @brief Get List of All Transactions
	
	@return A list containing transaction dictionaries """ 
	def get_all_transactions(self):
		return self.db["transaction"]

	""" @brief Get List of all Rules
	
	@return A List containing rule dictionaries """
	def get_all_rules(self):
		return self.db["rules"]

	""" @brief Get List of Matching Transactions

	Scans the list of transactions, compares them to the given rule, and 
	generates a list of transactions that match the rule

	@param rule = A Rule dictionary object
	@return A list of transactions dictionaries"""
	def get_matching_transactions(self,rule):
		ms = []
		for t in self.get_all_transactions():
			if(self._matches(t,rule)):
				ms.append(t)

		return ms

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
			t_db = self._find_uuid(t["uuid"]):
			if t_db:
				# Update the transaction with the latest data
				t_db["memo"] = t["memo"]
				t_db["amount"] = t["amount"]
			else:
				# Add this T to the db
				self.db["transactions"].append(t)

		# Save Changes to the disk
		self._save()

	


	def add_rule(self,rules):
		# TODO Check format of rule is correct
		format_correct = True;
		rls = []
		if format_correct:
			rls = [rules]



	#-----------------#
	# Removal Methods #
	#-----------------#

	"""" @brief Remove Transaction from the database 
	
	@param transaction The transaction you want to remove """
	def remove_transaction(self,transaction):
		self.db["transaction"].remove(transaction)

	""" @brief Remove a Rule from the database

	@param rule the rule you want to remove """
	def remove_rule(self,rule):
		self.db["rules"].remove(rule)


	#----------------#
	# Format Methods #
	#----------------#

	## Transaction Prototype
	#
	# This object contains the transactions prototype format.  All 
	# transactions must contain the following fields
	FORMAT_TRANSACTION = {
			"memo":str,
			"uuid":str,
			"ammount":float,
			"bank":str
			}
	## Rule Prototype
	#
	# THis object contains the rule prototype format.  All rules must
	# contain the following fields.
	FORMAT_RULE = {
			"memo":str,
			}

	def create_transaction(self,memo,uuid,ammount,bank,extra):
		pass

	def create_rule(self,memo,extra):
		pass

	def _check_transaction_format(self,transaction):
		return self._check_format(transaction,FORMAT_TRANSACTION)

	def _check_rule_format(self,rule):
		return self._check_format(rule,FORMAT_RULE)

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
	
