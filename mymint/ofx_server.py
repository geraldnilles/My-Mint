################################
################################
#
# OFX.py - This module is used to grab OFX data from financial servers
#
################################
################################

import jinja2
import time
import uuid
import httplib
import re

#---------------#
# OFX Templates #
#---------------#

## Document Header Template
#
# Contains the XML and OFX headers
TMPL_XML_DOCUMENT = """<?xml version=1.0 encoding=UTF-8?>
<?OFX OFXHEADER=200 VERSION=211 SECURITY=NONE OLDFILEUID=NONE NEWFILEUID=NONE ?>

<OFX>
	{{ ofx_body }}
</OFX>

"""

## Signon Request Template
#
# Template for the OFX signon message
TMPL_SIGNON_REQUEST_ELEMENT = """
<SIGNONMSGSRQV1>
	<SONRQ>
		<DTCLIENT>{{ time }}</DTCLIENT>
		<USERID>{{ username }}</USERID>
		<USERPASS>{{ password }}</USERPASS>
		<LANGUAGE>ENG</LANGUAGE>
		<FI>
			<ORG>{{ org }}</ORG>
			<FID>{{ fid }}</FID>
		</FI>
		<APPID>QWIN</APPID>
		<APPVER>1700</APPVER>
	</SONRQ>
</SIGNONMSGSRQV1>
"""

## Bank Transaction Request Template
#
# This template contains a request for bank account transactions.
TMPL_BANK_REQUEST_ELEMENT = """
<BANKMSGSRQV1>
	<STMTTRNRQ>
		<TRNUID>{{ uuid }}</TRNUID>
		<STMTRQ>
			<BANKACCTFROM>
				<BANKID>{{ bank_id }}</BANKID>
				<ACCTID>{{ acct_id }}</ACCTID>
				<ACCTTYPE>{{ acct_type }}</ACCTTYPE>
			</BANKACCTFROM>
			<INCTRAN>
				<INCLUDE>Y</INCLUDE>
			</INCTRAN>
		</STMTRQ>
	</STMTTRNRQ>
</BANKMSGSRQV1>
"""

## Credit Card Transaction request Template
#
# This template contains a request for credit card account transactions
TMPL_CREDITCARD_REQUEST_ELEMENT = """
<CREDITCARDMSGSRQV1>
	<CCSTMTTRNRQ>
		<TRNUID>{{ uuid }}</TRNUID>
		<CCSTMTRQ>
			<CCACCTFROM>
				<ACCTID>{{ acct_id }}</ACCTID>
			</CCACCTFROM>
			<INCTRAN>
				<INCLUDE>Y</INCLUDE>
			</INCTRAN>
		</CCSTMTRQ>
	</CCSTMTTRNRQ>
</CREDITCARDMSGSRQV1>
"""
## Template Environment
TMPL_ENV = jinja2.Environment()


## Get OFX data from a server
#
# This function grabs a list of transactions.  The bank object provides all of
# the required data needed to fetch the OFX data from the server
#
# @param bank a dictionary containing information abou the account.  See the 
# db.py file for the correct format of the bank object.
# @return the OFX data string
def get_data(bank):
    # Create Signon Element
    tmpl = TMPL_ENV.from_string(TMPL_SIGNON_REQUEST_ELEMENT)

    # Add Unique items to the bank object before creating the request
    bank ["time"] =  time.strftime("%Y%m%d%H%M%S")
    bank ["uuid"] = uuid.uuid1().hex
    # Render the Request text
    ofx_body = tmpl.render(bank)
    
    # Create Request (depends on Account type)
    if bank["acct_type"] in ["CHECKING"]:
        tmpl = TMPL_ENV.from_string(TMPL_BANK_REQUEST_ELEMENT)
        ofx_body += tmpl.render(bank)
    elif bank["acct_type"] in ["CREDITCARD"]:
        tmpl =  TMPL_ENV.from_string(TMPL_CREDITCARD_REQUEST_ELEMENT)
        ofx_body += tmpl.render(bank)
    
    tmpl = TMPL_ENV.from_string(TMPL_XML_DOCUMENT)
    # Render the OFX request
    request = tmpl.render({"ofx_body":ofx_body})

    # Sends request and returns the data packet
    return send_request(request,bank["url"])

## Sends OFX request string to the server
#
# This function sends the OFX body object to the server pointed to by the given
# url.  This function transmits the OFX string as POST data.  It uses HTTPS
# so the data will be encrypted and cannot be intercepted.  The returned OFX
# data will be returned as a string
#
# @param body a string contains the OFX request
# @param url a string containing the ofx server url
# @return a string containing the OFX response
def send_request(body,url):
    # Creates HTTPS Connection
    c = httplib.HTTPSConnection(split_url(url)[0])
    # Creates Headers (Pretending to be Quiken 1.7 for WIndows)
    headers = { "Content-Type":"application/x-ofx",
                "User-Agent":"QWIN 1.7"}
    # Send Request
    c.request("POST",split_url(url)[1],body,headers)
    # Get Response
    r = c.getresponse()
    # Print Status
    print (r.status,r.reason)
    data = r.read()
    c.close()

    return data

## Splits the URL into base and path
#
# Splits the domain and the path of a URL.  This is used by the HTTP request
#
# @param url The URL you want to spilt up
# @return A list of length 2.  The first item is the domain and the second is 
# the path
def split_url(url):
    theRE = "https://(.*?)/(.*)"
    m = re.search(theRE,url)
    if m:
        return (m.group(1),"/"+m.group(2))

