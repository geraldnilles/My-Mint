################################
################################
#
# OFX.py - This module is used to grab OFX data from financial servers
#
################################
################################

import xml.etree.ElementTree as et

#############################
# Gets OFX data from server 

# Parameters:
    # bank - THis is a dictionary containing the bank info and signon info
    #       It will normally be in the following format:
    #       {   
    #           "bankid"="[routing number]",
    #           "accttype"="CHECKIKNG/SAVINGS/CREDITCARD",
    #           "acctid"="[account number/creditcard number",
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
    sign = signon_elements(bank)
    # Create Request (depends on Account type)
    if bank["accttype"] in ["CHECKING"]:
        msg = bankmsg_element(bank)
    elif bank["accttype"] in ["CREDITCARD"]:
        msg = ccmsg_element(bank)
    # Combines the sign-on and Request into the complete message
    body = create_body([sign,msg])
    # Sends request and returns the data packet
    return send_request(body,bank["ofx_url"])

#########################
# Creates a Bank Request

# Parameters:
    # bank - Dictonary containing the banks info and signon info
# Returns:
    # XML Element Tree - containing the bank request
def bankmsg_element(bank):
    # Create Bank Message
    bankmsg = et.Element("BANKMSGSRQV1")
    # Create Statement Transaction Request
    stmttrnrq = et.SubElement(bankmsg,"STMTTRNRQ")
    # Create Transaction UID
    trnuid = et.SubElement(stmttrnrq,"TRNUID")
    trnuid.text = uuid.uuid1().hex
    # Create Statement Request
    stmtrq = et.SubElement(stmttrnrq,"STMTRQ")
    # Create Bank Account Element
    bankacctfrom = et.SubElement(stmtrq,"BANKACCTFROM")
    # Create Bank ID element
    bankid = et.SubElement(bankacctfrom,"BANKID")
    bankid.text = bank["bankid"]
    # Create Account Number element
    acctid = et.SubElement(bankacctfrom,"ACCTID")
    acctid.text = bank["acctid"]
    # Create Account Type element
    accttype = et.SubElement(bankacctfrom,"ACCTTYPE")
    accttype.text = bank["accttype"]
    # Create Include Transaction Element
    inctran = et.SubElement(stmtrq,"INCTRAN")
    # Create Include Element
    include = et.SubElement(inctran,"INCLUDE")
    include.text = "Y"
    return bankmsg


#########################
# Creates a CreditCard Request

# Parameters:
    # bank - Dictonary containing the banks info and signon info
# Returns:
    # XML Element Tree - containing the CreditCard request

def ccmsg_element(bank):
    ccmsgset = et.Element("CREDITCARDMSGSRQV1")
    ccstmttrnrq = et.SubElement(ccmsgset,"CCSTMTTRNRQ")
    trnuid = et.SubElement(ccstmttrnrq,"TRNUID")
    trnuid.text = uuid.uuid1().hex
    ccstmtrq = et.SubElement(ccstmttrnrq,"CCSTMTRQ")
    ccacctfrom = et.SubElement(ccstmtrq,"CCACCTFROM")
    acctid = et.SubElement(ccacctfrom,"ACCTID")
    acctid.text = bank["acctid"]
    inctran = et.SubElement(ccstmtrq,"INCTRAN")
    include = et.SubElement(inctran,"INCLUDE")
    include.text = "Y"

    return ccmsgset

######################
# Combines the signong and bank requests to for an OFX request string

# Paramter:
    # reqs - List of ElementTree Requests
# Returns
    # String - OFX Request String

def create_body(reqs):
    output = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
    output += "<?OFX OFXHEADER=\"200\" VERSION=\"211\" SECURITY=\"NONE\" OLDFILEUID=\"NONE\" NEWFILEUID=\"NONE\" ?>\n"

    root = et.Element("OFX")
    for r in reqs:
        root.append(r)

    output += et.tostring(root)

    return output

#########################
# Creates a  Signon Request

# Parameters:
    # bank - Dictonary containing the banks info and signon info
# Returns:
    # XML Element Tree - containing the Signon request

def signon_element(bank):
    sign = et.Element("SIGNONMSGSRQV1")
    sonrq = et.SubElement(sign,"SONRQ")
    dt = et.SubElement(sonrq,"DTCLIENT")
    dt.text = time.strftime("%Y%m%d%H%M%S")
    userid = et.SubElement(sonrq,"USERID")
    userid.text = bank["username"]
    userpass = et.SubElement(sonrq,"USERPASS")
    userpass.text = bank["password"]
    lang = et.SubElement(sonrq,"LANGUAGE")
    lang.text= "ENG"
    fi = et.SubElement(sonrq,"FI")
    org = et.SubElement(fi,"ORG")
    org.text = bank["org"]
    fid = et.SubElement(fi,"FID")
    fid.text = bank["fid"]
    appid = et.SubElement(sonrq,"APPID")
    appid.text = "QWIN"
    appver = et.SubElement(sonrq,"APPVER")
    appver.text = "1700"
    return sign


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

