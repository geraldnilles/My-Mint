import xml.etree.ElementTree as et

# This is the main function that should be called.
# bank is a dictonary containing info about the financial institution
def get_trns(bank):
    # Create Signon Message
    signonmsg = et.Element("SIGNONMSGSRQV1")
    # Create Signon Request and add to signon message
    sonrq = et.Element("SONRQ") 
    signonmsg.append(sonrq)
    # Create Time element and add to signon request
    dtc = et.Element("DTCLIENT")
    dtc.text = time.time() # TODO Fix format
    sonrq.append(dtc)
    # Create User ID Element and add to signon reqeust
    userid = et.Element("USERID")
    userid.text = bank["username"]
    sonrq.append(userid)
    # Create User Password Eleement and add to signon request
    userpass = et.Element("USERPASS")
    userpass.text = encrypt_password(bank)
    sonrq.append(userpass)
    #...
    
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
    output = """
<?xml version="1.0"?>

<?OFX OFXHEADER="200" VERSION="211" SECURITY="TYPE1" OLDFILEUID="NONE" NEWFILEUID="NONE" ?>

"""
    root = et.Element("ofx")
    for r in reqs:
        root.append(req)

    output += et.ElementTree.tostring(root)

    return output

def parse_ns(data):
    pass

def parse_cert(data):
    pass
