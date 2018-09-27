import sys

def codecutter(code,startPos,endPos):
    if len(code) == 1:
        return code
    returnCode={}
    pos=startPos
    val=0
    while pos < (endPos):
        returnCode[val] = code[pos]
        val = val + 1
        pos = pos + 1
    return returnCode

def prog():
    filename = sys.argv[1]
    file=open( filename ,"r+")
    #create variables
    code={}
    startPos = 0
    i = 0 #index
    #loop through file
    for word in file.read().split():
        word = word.lower()
        code[i] = word
        i = i + 1
    for pos in code:
        if code[pos] == "let":
            #print "let pos: ",pos
            for inpos in code:
                inpos = inpos + pos
                if code[inpos] == "end":
                    letinend(codecutter(code,pos+1,inpos));
                    #print "end pos: ",inpos
                    pos = inpos
                    break

def letinend(code):
    factors = {}
    startPos = 0
    for pos in code:
        if code[pos] == "in":
            factors = decllist(codecutter(code,startPos,pos));
            g_type = code[pos+1] #global type            
            val = (factor(codecutter(code,pos+3,len(code)-1),factors))
            print val

def decllist(code):
    factors = {}
    startPos=0
    i = 0
    for pos in code:
        if code[pos] == ";":
            factors[i] = decl(codecutter(code,startPos,pos));
            startPos = pos + 1
            i = i + 1
    return factors

def decl(code):
    value = {}
    r_id="" #r is short for return
    r_type=""
    r_expr=0
    for pos in code:
        if code[pos] == ":":
            r_id = code[pos-1]
            r_type = mytype(code[pos+1])
            r_expr = expr(codecutter(code,pos+3,len(code)))
    #print "the variable ID is ",r_id," as type ",r_type," and value ",r_expr
    value = {"id":r_id,"type":r_type,"value":r_expr}
    return value

def mytype(giventype): #because type is already taken
    giventype = giventype.lower()
    if giventype == "int" or giventype == "real":
        return giventype;
    else:
        sys.exit("ERROR 102: incorrect value type(s)");
    return;

def scrub(code):
    startPos = 0
    for pos in code:
        if code[pos] == "(" and pos > 0:
            if code[pos-1] == "real" or code[pos-1] =="int":
                scrub(codecutter,startPos,pos)


def expr(code):
    #print code
    exprs = {}
    if len(code) == 1: 
        return code[0];
    startPos = 0
    exprs_pos = 0
    for pos in code:
        if code[pos] == "+": 
            exprs[exprs_pos] = term(codecutter(code,startPos,pos));
            exprs[exprs_pos+1] = "+"
            exprs_pos = exprs_pos + 2
            startPos = pos + 1
        elif code[pos] == "-":
            exprs[exprs_pos] = term(codecutter(code,startPos,pos));
            exprs[exprs_pos+1] = "-"
            exprs_pos = exprs_pos + 2
            startPos = pos + 1
        elif pos == len(code)-1:
            exprs[exprs_pos] = term(codecutter(code,startPos,pos+1));
            #exprs[exprs_pos+1] = "eof"
        elif pos == len(code)-1 and startPos == 0:
            exprs[exprs_pos] = term(code);
    val = 0
    #print code
    if len(exprs) == 1:
        return exprs[0];
    if exprs[1] == "+":
        #print exprs[0]," + ",exprs[2]
        val = float(exprs[0]) + float(exprs[2])
    elif exprs[1] == "-":
        #print exprs[0]," - ",exprs[2]
        val = float(exprs[0]) - float(exprs[2])
    else:
        sys.exit("ERROR A1: calculating expression");
    exprs[2] = str(val)
    val = expr(codecutter(exprs,2,len(exprs)));
    return val

def term(code):
    terms = {}
    if len(code) == 1:
        #print code[0]
        return code[0];
    startPos = 0
    terms_pos = 0
    for pos in code:
        if code[pos] == "*":
            terms[terms_pos] = term(codecutter(code,startPos,pos));
            terms[terms_pos+1] = "*"
            terms_pos = terms_pos + 2
            startPos = pos + 1
        elif code[pos] == "/":
            terms[terms_pos] = term(codecutter(code,startPos,pos));
            terms[terms_pos+1] = "/"
            terms_pos = terms_pos + 2
            startPos = pos + 1
        elif pos == len(code)-1:
            terms[terms_pos] = term(codecutter(code,startPos,pos+1));
    val = 0
    if terms[1] == "*":
        #print terms[0][0]," * ",terms[2][0]
        val = float(terms[0]) * float(terms[2])
    elif terms[1] == "/":
        #print terms[0]," / ",terms[2]
        val = float(terms[0]) / float(terms[2])
    else:
        sys.exit("Error calculating expression");
    terms[2] = str(val)
    val = term(codecutter(terms,2,len(terms)));
    return val

def factor(code,factors):
    startPos=0 
    for pos in code:
        '''
        if pos == len(code):
            break
        if code[pos] == "(":
            lvl = 0
            parenPos = {}
            parenPos[lvl] = pos + 1
            pos = pos + 1
            for inpos in code:
                inpos = inpos + pos
                if code[inpos] == "(":
                    inpos = inpos + 1
                    lvl = lvl + 1
                    parenPos[lvl] = inpos
                elif code[inpos] == ")":
                    print codecutter(code,parenPos[lvl],inpos)
                    lvl = lvl - 1
                    

            #print codecutter(code,pos+1,len(code))
            code[pos] = factor(codecutter(code,pos+1,len(code)),factors)
            dis = code[pos][1] + 1
            print (dis)
            code[pos] = code[pos][0]
            pos = pos + 1
            for inpos in code:
                inpos = inpos + pos
                if inpos+dis < len(code):
                    code[inpos] = code[inpos+dis]
            code = codecutter(code,startPos,len(code)-dis)
            print code
            #sys.exit()
        elif code[pos] == ")":
            return {0:expr(codecutter(code,startPos,pos)),1:((pos+1)-(startPos+1))}
        '''
        for fpos in factors: 
            if code[pos] == factors[fpos]["id"]:
                code[pos] = factors[fpos]["value"]
    #print code
    #sys.exit()
    return expr(code);

prog();

'''
        if code[pos] == "int" or code[pos] == "real":
            if code[pos+1] == "(":
                for inpos in code:
                    if code[inpos] == "(":
                        print "exiting"
                        sys.exit()
                    elif code[inpos] == ")":
                        code = expr(code)
            else:
                sys.exit("error a2: type-cast error");
''' 
