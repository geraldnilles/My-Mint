import xml.etree.ElementTree as et


####################
# Converts OFX data string to JSON for parsing

# Parameters:
    # ofx - String containing the OFX request data
# Returns:
    # json - List of transactions

def ofx_to_json(ofx):
    xml = et.fromstring(ofx)

    retJSON = []

    # TODO Read FID from XML data
    # fid = ...

    for t in xml.iter("STMTTRN"):
        trn = {}
        for c in t:
            if c.tag=="DTPOSTED":
                trn["date"]=c.text
            elif c.tag=="FITID":
                trn["uid"] = fid+c.text
            elif c.tag=="TRNAMT":
                trn["amount"] = c.text
            elif c.tag=="NAME":
                trn["name"]=c.text
            elif c.tag=="MEMO":
                trn["memo"]=c.text

        retJSON.append(trn)

#######################
# Looks through the JSON object for the same UID
#   Recusive funtion

# Parameters:
    # obj - THe JSON object to search through
    # uid - the UID being searched for
# Return
    # Bool - True if the UID exists, False if it does not

def uid_exists(obj,uid):

    # If current object has a UID, see if it matches
    if "uid" in obj:
        if obj["uid"] == uid:
            return True
        else:
            return False

    # Set Default Value
    result = False
    # If object contains an "Accounts" object, 
    if "accounts" in obj:
        # Run the same funciton for each account
        for a in obj["accounts"]:
            if .uid_exists(a,uid):
                result = True

    # if Object contains a Transactions object, 
    if "transactions" in obj:
        # Run the same function for each transaction
        for t in obj["transactions"]:
            if .uid_exists(t,uid):
                result = True

    return result

#####################
# Generates an unnested list of every transaction

# Parameters:
    # acct - the JSON account object
# Returns
    # List - Contains every transaction in that account (and in subaccounts)

def get_all_trns(acct):
        # Create Empty LIst to return
        trns = []

        # Add all "transactions" in the current account
        if "transactions" in acct:
            trns += acct["transactions"]

        # Jump to the next accoutn down and do the same
        if "accounts" in acct:
            for a in account:
                trns += get_all_trns(a)

        # Return the complete list
        return trns



#########################
# Gets the immediate parent object of a child

# Parameters:
    # root - Root JSON object (needed since JSON only points down the tree)
    # child - Child object (looking for its parent)
# Return
    # JSON Object - Parent object

def get_parent(root,child):

    # Check if Child is in the current account's Transaction list
    if "transactions" in root:
        if child in root["trnsactions"]:
            return root
    # Check if child is in the current account's subaccount list.
    if "accounts" in root:
        if child in root["accounts"]:
            return root
        # If not, look in the subaccounts
        else:
            for a in root["accounts"]:
                p = get_parent(a,child)
                if p != None:
                    return p
    # If no dice, return None
    return None

    
################################
# Determines if the Parent/Child relationship is true (Maury Povich Show)

# Parameters
    # parent - the parent object in the search
    # child - the child object in the search

# Returns
    # Bool - True if the relationship is true, False if not

def ischild(parent,child):
    if child in parent:
        return True

    result = False
    if "accounts" in parent:
        for a in parent["accounts"]:
            if ischild(a,child):
                result = True

    if "transactions" in parent:    def multiplier(self,a,b):
        A = self.get_acct_type(a)
        B = self.get_acct_type(b)

        # Put both sides of the equation in their own sets
        set1 = ["Assets","Expenses"]
        set2 = ["Equity","Income","Liabilities"]

        # If A and B are on oposite sides of the equation, no need to invert the sign
        if A in set1 and B in set2:
            return 1
        elif B in set1 and A in set2:
            return 1
        # Othewise, you will need to invert
        else
            return -1

        for t in parent["transactions"]:
            if ischild(t,child):
                result = True

    return result


###########################
# Determines the account type [Asset, Income, Liability, Equity, Expenses]

# Parameters
    # root - the Root of the entire JSON object
    # obj - We are looking for the account type of this obj
# Returns
    # String - Account Type

def get_acct_type(root,obj):
    # Searches the 5 main accounts
    for a in root["accounts"]:
        # If object is under this account, return its Name
        if ischild(a,obj):
            return a["name"]

##########################
# Searches the main JSON object for an account with the matching name

# Parameters
    # root - The Root of the entire JSOn object
    # name - The name of the account youa re looking for
# Returns
    # JSON Obj - The Account object (or None if not found)


def find_acct(root,name):
    # Look at current accoutn name
    if root["name"] = name:
        return root

    # Look in subaccounts
    for a in root["accounts"]:
        acct = find_acct(a,name)
        if acct != None:
            return acct

    return None


############################
# Determines the multiplier (sign) for a transaction between 2 accounts

# Parameters
    # Root - Root of the entire JSON object
    # a - Account A
    # b - account B

# Returns
    # -1 or 1 depending on if a sign inversion is required.

def multiplier(root,a,b):
    A = self.get_acct_type(a)
    B = self.get_acct_type(b)

    # Put both sides of the equation in their own sets
    set1 = ["Assets","Expenses"]
    set2 = ["Equity","Income","Liabilities"]

    # If A and B are on oposite sides of the equation, no need to invert the sign
    if A in set1 and B in set2:
        return 1
    elif B in set1 and A in set2:
        return 1
    # Othewise, you will need to invert
    else
        return -1

#######################
# Creates an independant copy of the transaction.

def copy_trns(oldt):
    # Marks the new transaction as a copy (just in case it needs to be undone)
    newt = {"copy":True}

    for k in oldt:
        # TODO Add check to make sure the TRN is only numbers or strings
        newt[k] = oldt[x]


