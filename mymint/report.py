


########################
# Creates a Tree Summary

# Parameters:
    # acct - Account Object to which you want a Tree Summary
    # start - Beginning date of the summary
    # stop - Ending date of the summary

def tree_summary(acct,start=None,end=None,indent=""):
    report = indent
    # Get List of all transactions
    # Calcualte Sum of all totals
    report += acct["name"]+"\t"+total

    # Do the same for all subaccounts
    for a in acct["accounts"]:
        report += (a,start,end,indent+"  ")
    

