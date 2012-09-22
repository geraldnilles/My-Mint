import xml.etree.ElementTree as et
import httplib
import re
import time

# This is the main function that should be called.
# bank is a dictonary containing info about the financial institution
def get_trns(bank):

    ### Create Signon Message
    signonmsg = et.Element("SIGNONMSGSRQV1")
    # Create Signon Request and add to signon message
    sonrq = et.SubElement(signonmsg,"SONRQ")
    # Create Time element and add to signon request
    dtc = et.SubElement(sonrq,"DTCLIENT")
    dtc.text = time.time() # TODO Fix format
    # Create User ID Element and add to signon reqeust
    userid = et.SubElement(sonrq,"USERID")
    userid.text = bank["username"]
    # Create User Password Eleement and add to signon request
    userpass = et.SubElement(sonrq,"USERPASS")
    userpass.text = encrypt_password(bank)
    # Create Languate Element and add to signon Rq
    lang = et.SubElement(sonrq,"LANGUAGE")
    lang.text = "ENG"
    # Creat FI Eleement
    fi = et.SubElement(sonrq,"FI")
    # Creat Org Element and FID Element
    org = et.SubElement(fi,"ORG")
    org.text = bank["org"]
    fid = et.SubElement(fi,"FID")
    fid.text = bank["fid"]
    # Create App ID and Version Elements
    appid = et.SubElement(sonrq,"APPID")
    appid.text = "MyPyOFX"
    appver = et.SubElement(sonrq,"APPVER")
    appver.text = "0001"

    # Create Bank Message
    bankmsg = et.Element("BANKMSGSRQV1")
    # Create Statement Transaction Request
    stmttrnrq = et.SubElement(bankmsg,"STMTTRNRQ")
    # Create Transaction UID
    trnuid = et.SubElement(stmttrnrq,"TRNUID")
    trnuid.text = uuid #TODO FIgureo out a UID
    # Create Statement Request
    stmtrq = et.SubElement(stmttrnrq,"STMTRQ")
    # Create Bank Account Element
    bankacctfrom = et.SubElement(stmtrq,"BANKACCTFROM")
    # Create Bank ID element
    bankid = et.SubElement(bankacctfrom,"BANKID")
    bankid.text = bank["routing_number"]
    # Create Account Number element
    acctid = et.subElement(bankacctfrom,"ACCTID")
    accit.text = bank["acct_number"]
    # Create Account Type element
    accttype = et.SubElement(bankacctfrom,"ACCTTYPE")
    accttype.text = bank["acct_type"]
    # Create Include Transaction Element
    inctran = et.SubElement(stmtrq,"INCTRAN")
    # Create Include Element
    include = et.SubElement(inctran,"INCLUDE")

    # Add XML and OFX headers and put messages in an <OFX> element
    create_ofx_body([signonmsg,bankmsg])    

    # Create HTTP connection with
    c = urllib(bank["url"])
    c.request(data)
    resp = c.read()
    c.close()

    return resp

def encrypt_password(bank):
    # Obtain Server's Profile. This gathers information on the capabilities of the FI server
    # Grab the Challange Data
    data = get_challenge_data(bank)
    # Separate data.  There should be a plain text OFX resopnse as well as a cert
    NS = parse_ns(data)
    SCert = parse_cert(data)

    # Generate 16 random Octets.  Save as NC
    NC = random(16)
    # Pad password (P) with null on the right
    P = bank["password"]
    P = P+((32-len(P))*"NULL")
    T = sha1(NS+P+NC) # I assume this means the bytes are concatinated?
    PS = random(57)
    D = NC+P+T
    EB = 0x00+BT+PS+0x00+D
    # Encrypt Password using RSA Public Key
    key = RSA.importKey(SCert)
    cipher = PKSC1.new(key)
    CT = cipher.encrypt(EB)
    CT2 = base64.standard_b64encode(CT1) # converts it to text for transport
    return CT2


# Create a OFX request Skeleton
# The argument is a list ofrequest element.  
# These will be placed inside the OFX element
def create_ofx_body(reqs):
    
    output = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
    output += "<?OFX OFXHEADER=\"200\" VERSION=\"211\" SECURITY=\"TYPE1\" OLDFILEUID=\"NONE\" NEWFILEUID=\"NONE\" ?>\n"

    root = et.Element("OFX")
    for r in reqs:
        root.append(r)

    output += et.tostring(root)

    return output

def parse_ns_cert(data):
    m = re.search("MIME type.*?;\s*boundary\s*=\s*(.*?)",data)
    #TODO Strip any \r or \n characters
    if (m):
        sp = data.split("--"+m.group(1))
    else:
        print "Cert Not INcluded"
        return 0

    m = re.search("<NS></NS>",sp[2])

    return {"ns":m.group(1),"cert":sp[3]}

## Performas a Chalenge request to get encryption info

def get_challenge_data(bank):
     # Establish an SSL connection
    c = httplib.HTTPSConnection(split_url(bank["ofx_url"])[0])
    # Create <CHALLENGERQ> request
    sign = et.Element("SIGNONMSGSRQV1")
    #TODO Add SONRQ with anonymous
    sonrq = et.SubElement(sign,"SONRQ")
    dt = et.SubElement(sonrq,"DTCLIENT")
    dt.text = time.strftime("%Y%m%d%H%M%S")
    userid = et.SubElement(sonrq,"USERID")
    userid.text = "anonymous"
    userpass = et.SubElement(sonrq,"USERPASS")
    userpass.text = "anonymous"
    lang = et.SubElement(sonrq,"LANGUAGE")
    lang.text= "ENG"
    fi = et.SubElement(sonrq,"FI")
    org = et.SubElement(fi,"ORG")
    org.text = bank["org"]
    fid = et.SubElement(fi,"FID")
    fid.text = bank["fid"]
    appid = et.SubElement(sonrq,"APPID")
    appid.text = "MyPyOFX"
    appver = et.SubElement(sonrq,"APPVER")
    appver.text = "0.1"
    chtrn = et.SubElement(sign,"CHALLENGETRNRQ")
    ch = et.SubElement(chtrn,"CHALLENGERQ")
    uid = et.SubElement(ch,"USERID")
    uid.text = bank["username"]
    body = create_ofx_body([sign])
    print body
    headers = { "Content-Type":"application/x-ofx",
                "User-Agent":"MyPyOFX 0.1"}
    c.request("POST",split_url(bank["ofx_url"])[1],body,headers)
    # Recieve <CHALLENGERS> from server.  
    r = c.getresponse()
    data = r.read()
    c.close()

    return data

# Splits the URL into base and path
def split_url(url):
    theRE = "https://(.*?)/(.*)"
    m = re.search(theRE,url)
    if m:
        return (m.group(1),"/"+m.group(2)) 

