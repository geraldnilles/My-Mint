import xml.etree.ElementTree as et
import httplib
import re
import time
import uuid

# TODO s
# Add ability to only download certain time periods

# This is the main function that should be called
# bank is a dictonary containing info about the financial institution
def get_trns(bank):
    sign = get_signon_element(bank)
    if bank["accttype"] in ["CHECKING"]:
        msg = get_bankmsg_element(bank)
    elif bank["accttype"] in ["CREDITCARD"]:
        msg = get_ccmsg_element(bank)
    body = create_ofx_body([sign,msg])
    print body+"\n\n"
    return send_request(body,bank["ofx_url"])


def get_bankmsg_element(bank):
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

def get_ccmsg_element(bank):
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
    

# Create a OFX request Skeleton
# The argument is a list ofrequest element.  
# These will be placed inside the OFX element
def create_ofx_body(reqs):
    
    output = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
    output += "<?OFX OFXHEADER=\"200\" VERSION=\"211\" SECURITY=\"NONE\" OLDFILEUID=\"NONE\" NEWFILEUID=\"NONE\" ?>\n"

    root = et.Element("OFX")
    for r in reqs:
        root.append(r)

    output += et.tostring(root)

    return output


def get_signon_element(bank):
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

def send_request(body,url):
    c = httplib.HTTPSConnection(split_url(url)[0])
    headers = { "Content-Type":"application/x-ofx",
                "User-Agent":"QWIN 1.7"}
    c.request("POST",split_url(url)[1],body,headers)
    r = c.getresponse()
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

