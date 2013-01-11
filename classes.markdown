
In order to prevent creating a God Object, i decided to break up my project into various classes.

# OFX

This class will communicate to an OFX server.
It will send and receive OFX requests and responses.

## Consructor
* Arguements
    * URL
    * Username
    * Password
    * .. Other acct info

## get\_transactions
* Arguments
    * None
* Returns a json object containing all of the transactions from the server

# MyMint
This will be the main object.
It will contain the UI that interact with all of the other objects.


# Search
This object will be used to do search like routines

# Manager
THis object will be used to add/delete/modify accounts and transactions
