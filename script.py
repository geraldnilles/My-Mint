#!/usr/bin/python




import os,re,urllib

## For Help, see this http://blog.philippklaus.de/2010/02/aqbanking-cli/
# TODO - Remove dependancy on aqbanking-cli program
def grab_transactions():
	## Use aqbanking-cli to download the bank transactions
	cmd = "aqbanking-cli request -a ACCT_Number --transactions -c out.txt"

	## Instead of using an inermediate file, we can simply read the STDOUT of the
	## above command

	return text

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
	

## Add the list of transactions to the database
def add_transaction(acct_id,desc,date,amount):
	## Open DB

	## If trns is already in the DB, return "Error: Already Exists"
	## Add to db

	## Close DB
	return "Success"

	
def apply_rules():
	## Scan through all of the transactions and apply the rules
	pass

	## scans through the transactions and looks for 2 transactions from the same date that
	## are opposite each other.  For example, when i pay my AMEX, it removes $100 from my 
	## bank account and adds $100 to my AMEX account.  These 2 transactions need to be merged
def find_opposites():
	pass

def add_account(name,acct_type,categories,username,password,acct_num):
	pass

def add_rule(desc_regex,acct_to,acct_from):
	pass


f = open("text/amex.txt",'r')
text = f.read()
parse_txt(text)
	


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


