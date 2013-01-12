##############################
# balance.py
#
# This contains a set of tools used to balance all of the transaction.
# We want every transaction to be entered exactly twice since every transaction 
# should come FROM and account and go TO and account.
##############################

import tools

#######################
# Create a list of all unbalanced transactions

# Parameters
    # root - Entire JSON object
# Returns
    # List - of unbalanced transactions

def get_unbalanced_trns(root):
    unbal = []

    trns = tools.get_all_trns(acct)
    while(len(trns) != 0):
        # Pop off Transaction of Interest TOI
        toi = trns.pop()
        balanced = False
        # Look for a different transaction that has the same uid
        for t in trns:
            # If a match is found make TOI as balanced and, remove the match 
            #   and break from the loop
            if t["uid"] == toi["uid"]:
                trns.remove(t)
                balanced = "True"
                break

        # If toi is still unbalanced, add it.
        if not balanced:
            unbal.append(toi)

    return unbal

#########################
# Attempts to balance the unbalanced transactions

# Parameters
    # root - Entire JSON object
# Returns
    # list of remaining unbalanced transactions

def run(root):
    trns = get_unbalanced_trns(root)

    rules = root["rules"]

    leftovers = []

    for t in trns:
        match = False
        for r in rules:
            if(rule_matches(t,r)):
                apply_rule(t,r)
                match = True
                break

        if not match:
            leftovers += t

###########################
# Compares the trn to the rule and tells if there is a match

def rule_matches(trn,rule):
    pass


#############################
# Applies the Rule

def apply_rule(oldt,rule):
    # Creates an independant copy of the trnasaction
    newt = copy_trns(oldt)

    # Finds the new account
    acct = tools.find_acct(rule["acctname"])
    # Adds it to the new account
    acct["transactions"].append(newt)

    # Changes the sign of the amount if needed
    newt["amount"] = newt["amount"]*tools.multiplier(oldt,newt)
    
