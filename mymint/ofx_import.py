######################
# OFX Import
#
# These functions convert OFX data into JSON objects so they can be imported
# into the database
#######################


import xml.etree.ElementTree as etree
import HTMLParser

## Convert OFX (XML) to a JSON object
#
# Load a string of OFX data directly from the bank. This function will create a
# list of dictionaries and return the object
#
# @param ofx_string An OFX (XML) string to be converted
# @return list of dictionaries that describe the transactions
def xml(ofx_string):
	# Load the OFX string into memory as an ETree
	root = etree.fromstring(ofx_string)
	# Create an empty list that will hold the transaction dictionaries
	t_list = []
	# Iterate over all Transaction elements
	for t in root.iter("STMTTRN"):
		trns = {}
		
		trns["amount"] = 	float(t.find("TRNAMT").text)
		trns["name"] = 		t.find("NAME").text
		if t.find("MEMO") == None:
			trns["memo"] = ""
		else:
			trns["memo"] =		t.find("MEMO").text
		trns["date"] = 		t.find("DTPOSTED").text
		trns["uuid"] = 		t.find("FITID").text

		


		t_list.append(trns)

	print "%d transactions imported from OFX"% len(t_list)

	return t_list



## Convert OFX (SGML) to a JSOn object
#
# Load string of OFX data directly from teh bank. This functio will create a 
# list of dictionaries and return the object
#
# @param ofx_string An OFX string in SGML format
# @return a list of transaction dictionaries
def sgml(ofx_string):
	# Create a Dictionary List
	t_list = list()
	# Create the Parser
	parser = sgml_parser(t_list)
	# Feed the OFX_Stirng intot he parser
	parser.feed(ofx_string)
	# Return the results
	return t_list


## SGML Parser Object
#
# This object reads the OFX stream, looks for specific tags, and converts it
# to a list of transaction dictionaries
class sgml_parser(HTMLParser.HTMLParser):
	## Constructor
	#
	# Adds a t_list object where the list will be stored
	def __init__(self, t_list):
		HTMLParser.HTMLParser.__init__(self)
		self.last_tag = ""	
		self.t_list = t_list

	## Start Tag Handle
	#
	# Looks for STMTTRN tag.  When it sees it, it adss a new transaction
	# dictionary to the end of the t_list.  It also saves the latest tag
	# for use in the handle_data method
	def handle_starttag(self,tag,attrs):
		# Save Latest Tag for future use
		self.last_tag = tag
		# If tag is STMTTRN, add a new dict to the list
		if tag == "stmttrn":
			self.t_list.append({})

	## Data handle
	#
	# Stores the SGML data into the latest transaction dictrionary
	def handle_data(self,data):
		# Looks at the last tag and populates the correct field in dict
		if self.last_tag =="trnamt":
			self.t_list[-1]["amount"] = float(data)
		elif self.last_tag =="name":
			self.t_list[-1]["name"] = data
		elif self.last_tag =="memo":

			self.t_list[-1]["memo"] = data
		elif self.last_tag =="dtposted":

			self.t_list[-1]["date"] = data
		elif self.last_tag =="fitid":

			self.t_list[-1]["uuid"] = data
		else:
			pass




