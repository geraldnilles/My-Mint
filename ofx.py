import xml.etree.ElementTree as et

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
    # Establish an SSL connection
    c = HTTPSConnection(bank["url"])
    # Create <CHALLENGERQ> request
    
    ch = et.Element("CHALLENGERQ")
    uid = et.Element("USERID")
    ch.append(uid)
    body = create_ofx_body(ch)
    c.request("POST","/??",body,headers) 
    # Recieve <CHALLENGERS> from server.  
    r = c.getresponse()
    data = r.read()
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
    output = "<?xml version=\"1.0\"?>\r\n\r\n"
    output = "<?OFX OFXHEADER=\"200\" VERSION=\"211\" SECURITY=\"TYPE1\" OLDFILEUID=\"NONE\" NEWFILEUID=\"NONE\" ?>\r\n\r\n"

    root = et.Element("ofx")
    for r in reqs:
        root.append(req)

    output += et.ElementTree.tostring(root)

    return output

def parse_ns_cert(data):
    m = re.search("MIME type.*?; boundary =(.*?)",data)

    if (m):
        sp = data.split(m.group(1))
    else:
        print "Cert Not INcluded"
        return 0

    m = re.search("<NS></NS>",sp[2])

    return {"ns"=m.group(1),"cert":sp[3]}

