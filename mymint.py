#
import json
import xml.etree.ElementTree in et


class mint:

    def __init__(self,fn):
        if os.exists(fn):
            f = open(fn,"r")
            self.db = json.load(f)
            f.close()
        else:
            self.db={"rules":[],"accounts":[]}
            self.base_accts = ["Assets","Income","Equity","Expenses",
                                    "Liabilities"]
            for n in self.base_accts:
                self.add_acct(self.db["accounts"],n)
        self.fn = fn

    def save(self):
        f = open(self.fn,"w")
        json.dump(f,self.db)
        f.close()

    #####################
    ### Download Methods
    #####################

    # Wrapper for the Resursive Version 
    # TODO Remove this an use loaded arguments instead
    def download_all(self):
        self.download_all_rec(self.db)

    # Scans through the Accounts Tree, Looks for accounts with OFX info and
    # downloads the info.
    def download_all_rec(self,acct):    
        for a in acct["accounts"]:
            if "ofx_info" in a:
                self.download(a)
            if "accounts" in a:
                self.download_all_rec(a)
                
    # Downloads OFX data from the server given an account with OFX credentials.
    def download(self,acct):
        print "Downloading Transactions from "+acct["name"] 

        # Get OFX XML string
        resp = self.get_ofx_data(acct["ofx_info"])

        # Convert to an eTree object
        xml = et.fromstring(resp)

       # For eatch STatMenT TRaNsaction, create a json version of the trans
        for t in xml.iter("STMTTRN"):
            trn = {}
            for c in t:
                if c.tag=="DTPOSTED":
                    trn["date"]=c.text
                if c.tag=="FITID":
                    # Generate an UID based on FID and FITID
                    trn["uid"] = acct["ofx_info"]["fid"]+c.text
                if c.tag=="TRNAMT":
                    trn["amount"] = c.text
                if c.tag=="NAME":
                    trn["name"]=c.text
                if c.tag=="MEMO":
                    trn["memo"]=c.text

            # Check same transaction alread exists
            if self.find_uid(self.db,trn["uid"]):
                # If it does, do not add it
                continue

            # Add to acct's transaction list
            acct["transactions"].append(trn)
   
    ###########
    ### Search Methods
    ############

    # Recusive function that searches for uid
    def uid_exists(self,obj,uid):
        if "uid" in obj:
            if obj["uid"] == uid:
                return True
            else:
                return False

        result = False
        if "accounts" in obj:
            for a in obj["accounts"]:
                if self.find_uid(a,uid):
                    result = True

        if "transactions" in obj:
            for t in obj["transactions"]:
                if self.find_uid(t,uid):
                    result = True

        return result

    # Generates a list of Transactions inside an account and its child accounts
    def get_all_trns(self,acct):
        trns = []

        if "transactions" in acct:
            trns += acct["transactions"]

        if "accounts" in acct:
            for a in account:
                trns += self.get_all_trns(a)

    # Check to see if a transaction has been double entered.
    # 
    def is_sorted(self,trn):
        trns = self.get_all_trns(self.db)
        # Find all transactions that match
        matches = []
        for t in trns:
            if t["uid"] == trn["uid"]:
                matches.append(t)
            
        # If there are exactly 2 matches, and each match is in a different account, then return true.  Else, return false
        if len(matches) == 2:
            if self.get_parent(matches[0]) != self.get_parent(matches[1]):
                return True

        return False
            
            

    def get_unsorted_trns(self):
        trns = get_all_trns()
        unstrn = []
        for t in trns:
            if not is_sorted(trn):
                unstrn.append(t)
        return unstrn

    def get_parent(self,root,obj):
        if "transactions" in root:
            if obj in root["trnsactions"]:
                return root
        if "accounts" in root:
            if obj in root["accounts"]:
                return root
            else:
                for a in root["accounts"]:
                    p = get_parent(a,obj)
                    if p != None:
                        return p
            
        return None

    # Returns True, if the parent/Child relationship is correct.    
    # THis include sub-children too!
    def ischild(self,parent,child):
        if child in parent:
            return True


        result = False        
        if "accounts" in parent:
            for a in parent["accounts"]:
                if self.ischild(a,child):
                    result = True
        
        if "transactions" in parent:
            for t in parent["transactions"]:
                if self.ischild(t,child):
                    result = True

        return result


    # Gets the account type: [Asset,Income,Liability,Equity,Expenses]
    def get_acct_type(self,obj):
        # For allof the root accounts 
        for a in self.root["accounts"]:
            # If obj is a child, return the root account name
            if self.ischild(a,obj):
                return a["name"]

    # Returns the acct object that matches the name
    # Wrapper for recursive function.
    def get_acct_from_name(self,name):
        self.find_acct_rec(self.root,name)

    def find_acct_rec(self,obj,name):
        if obj["name"] == name:
            return obj

        for a in obj["accounts"]:
            t = find_acct_rec(a,name)
            if t :
                return t

        return None    

    ##############
    ### Manage Methods
    ###############

    # Creates a new account and adds it to the tree.
    # If executed successfully, the new acct object is returned.
    def add_acct(self,parent,name):
        if self.find_acct_from_name(name) != None:
            print "Account with the name \""+name+"\" already exists"
            return None
        acct = {
                "name":name,
                "transactions":[]
                }
        parent["accounts"].append(acct)
        return acct

    # Adds an ofx_info dictionary to the account.
    # If one already exists, it replaces it
    def add_ofx_info(self,acct,ofx):
        acct["ofx_info"]= ofx

    # Modifies the existing OFX dictionary
    def edit_ofx_info(self,acct,ofx):
        # If OFX dict was never initialized, call the add command
        if "ofx_info" not in acct:
            add_ofx_info(acct,ofx)
            return
        
        # Modify each key separately, this will preserve existing data in the ofx dictionary
        for k in ofx:
            acct["ofx_info"][k] = ofx[k]

    # Given an account object, this function clears all transactions of the 
    # current account and all its child accounts
    def wipe_trns(self,acct):
        # If account contains a "transaction" list, replace it witn an empty 
        if "transactions" in acct:
            acct["transactions"] = []

        # If account contains more accounts, recursivly call the same function
        if "accounts" in acct:
            for a in acct["accounts"]:
                self.wipe_trns(a)

    def apply_rules(trn):
        unsorted = self.get_unsorted_trns(self.db)
        for t in unsorted:
            for r in self.db["rules"]:
                if re.match(r["re"],t["name"]) and max > t["amount"] > min :
                    a = self.get_parent(t)
                    b = self.get_acct_from_name(r["account"])
                    m = self.multiplier(a,b)
                    c = copy.copy(t)
                    c["amount"]=c["amount"]*m
                    b["transactions"].append(c)
                    
                    break
            
                            

    def apply_rules_all():
        self.get_all_trns(self.db)


    # Figure out if the sign should be inverted based on the equation:
    # Assets + Expenses = Equity + Income + Liabilities
    def multiplier(self,a,b):
        A = self.get_acct_type(a)
        B = self.get_acct_type(b)

        # Put both sides of the equation in their own sets
        set1 = ["Assets","Expenses"]
        set2 = ["Equity","Income","Liabilities"]

        # If A and B are on oposite sides of the equation, no need to invert the sign
        if A in set1 and B in set2:
            return 1
        elif B in set1 and A in set2:
            return 1
        # Othewise, you will need to invert
        else
            return -1

    ###############
    ### OFX Methods
    ############### 

    def get_ofx_data(self,bank):
        sign = self.ofx_signon_elements(bank)
        if bank["accttype"] in ["CHECKING"]:
            msg = self.ofx_bankmsg_element(bank)
        elif bank["accttype"] in ["CREDITCARD"]:
            msg = self.ofx_ccmsg_element(bank)
        body = self.ofx_body([sign,msg])
        return self.send_request(body,bank["ofx_url"])

    def ofx_bankmsg_element(self,bank):
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

    def ofx_ccmsg_element(self,bank):
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

    def ofx_body(self,reqs):
        output = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
        output += "<?OFX OFXHEADER=\"200\" VERSION=\"211\" SECURITY=\"NONE\" OLDFILEUID=\"NONE\" NEWFILEUID=\"NONE\" ?>\n"

        root = et.Element("OFX")
        for r in reqs:
            root.append(r)

        output += et.tostring(root)

        return output

    def ofx_signon_element(self,bank):
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

    def send_request(self,body,url):
        c = httplib.HTTPSConnection(self.split_url(url)[0])
        headers = { "Content-Type":"application/x-ofx",
                    "User-Agent":"QWIN 1.7"}
        c.request("POST",self.split_url(url)[1],body,headers)
        r = c.getresponse()
        print (r.status,r.reason)
        data = r.read()
        c.close()

        return data

    # Splits the URL into base and path
    def split_url(self,url):
        theRE = "https://(.*?)/(.*)"
        m = re.search(theRE,url)
        if m:
            return (m.group(1),"/"+m.group(2))

