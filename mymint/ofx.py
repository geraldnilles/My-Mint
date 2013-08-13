################################
################################
#
# OFX.py - This module is used to grab OFX data from financial servers
#
################################
################################

import xml.etree.ElementTree as et
import jinja2


#-----------------------
# OFX Templates
#-----------------------

TMPL_XML_DOCUMENT = """
<?xml version=1.0 encoding=UTF-8?>
<?OFX OFXHEADER=200 VERSION=211 SECURITY=NONE OLDFILEUID=NONE NEWFILEUID=NONE ?>

<OFX>
	{{ ofx_body }}
</OFX>

"""

TMPL_SIGNON_REQUEST_ELEMENT = """
<SIGNONMSGSRQV1>
	<SONRQ>
		<DTCLIENT>{{ time.strftime("%Y%m%d%H%M%S") }}</DTCLIENT>
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

TMPL_ENV = jinja2.Environment()



#############################
# Gets OFX data from server 

# Parameters:
    # bank - THis is a dictionary containing the bank info and signon info
    #       It will normally be in the following format:
    #       {   
    #           "bank_id"="[routing number]",
    #           "acct_type"="CHECKIKNG/SAVINGS/CREDITCARD",
    #           "acct_id"="[account number/creditcard number",
    #           "username"="[username]",
    #           "password"="[password]",
    #           "ofx_url"="https://www.url/to/OFX/server",
    #           "fid"="[banks finantial ID",
    #           "org"="[Bank's ORG]"
    #       }

# Returns: 
    # String - OFX string (an XML file)
def get_data(bank):
    # Create Signon Element
    tmpl = TMPL_ENV.from_string(TMPL_SIGNON_REQUEST_ELEMENT)
    ofx_body = tmpl.render(bank)
    
    # Create Request (depends on Account type)
    if bank["acct_type"] in ["CHECKING"]:
        tmpl = TMPL_ENV.from_string(TMPL_BANK_REQUEST_ELEMENT)
        ofx_body += tmpl.render(bank)
    elif bank["acct_type"] in ["CREDITCARD"]:
        tmpl =  TMPL_ENV.from_string(TMPL_CREDITCARD_REQUEST_ELEMENT)
        ofx_body += tmpl.render(bank)
    
    tmpl = TMPL_ENV.from_string(TMPL_XML_DOCUMENT)
    
    request = tmpl.render({"ofx_body":ofx_body})

    # Sends request and returns the data packet
    return send_request(request,bank["ofx_url"])

###########################
# Sends OFX request and receives OFX data from bank server

# Parameters
    # bank - Dictonary containing the banks info and signon info
# Returns
    # string - OFX Data 

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

# Splits the URL into base and path
def split_url(url):
    theRE = "https://(.*?)/(.*)"
    m = re.search(theRE,url)
    if m:
        return (m.group(1),"/"+m.group(2))

