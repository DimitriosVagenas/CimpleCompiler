#Vagenas Dimitrios  A.M. 2941 cse52941

import sys

def  nextquad(): #added for int code
	global quadsList
	temp = str(len(quadsList))
	return temp

def genquad(op, x, y, z): #added for int code
	global quadsList
	quads = [nextquad(), [op, x, y, z]]
	quadsList.append(quads)
	return quads

def newtemp(): #added for int code
	global temp_count
	temp = 'T_' + str(temp_count)
	addEntity(temp, "tempvar", None) #s
	vars.append(temp)
	temp_count += 1
	return temp

def merge(list1, list2): #added for int code
	temp = list1 + list2
	return temp

def backpatch(mylist, z): #added for int code
	global quadsList
	for p in mylist:
		for i in quadsList:
			if p == i[0]:
				i[1][3] = z

def emptylist(): #added for int code
	temp = []
	return temp

def makelist(x): #added for int code
	temp = []
	temp.append(x)
	return temp

class Token:
# Properties : tokenType , tokenString , lineNo
	def __init__ (self , tokenType , tokenString , lineNo ):
		self. tokenType = tokenType
		self. tokenString = tokenString
		self. lineNo = lineNo

def lex():
	global lineNo
	global token
	tokenstring = ''
	tokentype = ''
	c = ' '
	letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
	numbers = '0123456789'
	keywords = ['program','declare','if','else','while','switchcase','forcase','incase','case','default','not','and',
	'or','function','procedure','call','return','in','inout','input','print']
	whitechars=[' ','\t','\n','\r']
	c = ci_prog.read(1)
	
	while c in whitechars:
		if c == '\n':
			lineNo += 1
		c = ci_prog.read(1)
		
	if c == '#':
		tokenstring = c
		while 1:
			c = ci_prog.read(1)
			if c == '\n':
				tokenstring+=c
				lineNo+=1
			elif c == '':
				print("lex error: comments did not close before eof... expected # before eof")
				exit()
			elif c == '#':		
				tokenstring+=c
				tokentype='remtk'
				token = Token(tokentype, tokenstring, lineNo)
				break
			else:
				tokenstring+=c
		return lex()
	else:			
		while c in whitechars:
			if c == '\n':
				lineNo += 1
			c = ci_prog.read(1)		
			
		if c == '':
			eof = True
		elif c in letters:
			tokenstring = c
			while (True):
				c = ci_prog.read(1)
				if c in letters or c in numbers:
					tokenstring+=c
				else:
					if tokenstring in keywords:
						tokentype=tokenstring+'tk'
					else:
						tokentype='idtk'	
					ci_prog.seek(ci_prog.tell()-1)	
					break	
				if len(tokenstring) > 30:
					print('lex error: number characters of of the identifier', tokenstring, 'are  out of bounds. line:',lineNo)
					exit()	
		elif c in numbers:
			tokenstring = c
			while (True):
				c = ci_prog.read(1)
				if c in numbers:
					tokenstring+=c
				elif c in letters:
					print('lex error: letter',c,'in number',tokenstring,'. line:',lineNo)
					exit()
				else:
					tokentype = 'numtk'	 	
					ci_prog.seek(ci_prog.tell()-1)	
					break
			if int(tokenstring) > pow(2, 32) - 1 or int(tokenstring)<-(pow(2, 32) - 1):
				print('lex error: number',tokenstring,'too big. line:',lineNo)
		elif c == '+' or c == '-':
			tokenstring = c
			tokentype='addtk'
		elif c == '*'	or c == '/':
			tokenstring = c
			tokentype = 'multk'
		elif c == '{' or c == '}' or c == '[' or c == ']' or c == '(' or c == ')':
			tokenstring=c
			tokentype='groupsymbtk'
		elif c == ',' or c == ';':
			tokenstring=c
			tokentype = 'delimtk'
		elif c == ':':
			c = ci_prog.read(1)
			if c == '=':
				tokenstring = ':='
				tokentype = 'asgntk'
			else:
				print("lex error: wrong assignment. Unexpected character", c, " expected =")
				exit()
		elif c == '<':
			tokenstring = c
			c = ci_prog.read(1)
			if c == '=' or c == '>':
				tokenstring += c
			else:
				ci_prog.seek(ci_prog.tell() - 1)
			tokentype = 'relOpertk'
		elif c == '>':
			tokenstring = c
			c = ci_prog.read(1)
			if c == '=':
				tokenstring += c
			else:
				ci_prog.seek(ci_prog.tell()-1)
			tokentype = 'relOpertk'
		elif c == '=':
			tokenstring = c
			tokentype = 'relOpertk'

		elif c == '.':
			tokenstring = c
			tokentype = 'endprogtk'
		else:
			print("lex error: character", c, " uknown character in line ",lineNo)
			exit()

		token = Token(tokentype, tokenstring, lineNo)
		return token
	

def program():
	global token
	global prog_name
	global checkReturn
	token = lex()
	if token.tokenType=='programtk':
		token = lex()
		if token.tokenType=='idtk':
			addScope() #s
			prog_name = token.tokenString #added for int code
			token=lex()
			checkReturn.append([0,0]) #s
			block(prog_name) #added for int code
			if token.tokenType != 'endprogtk':
				print('Error in program function')
				print("Syntax error: Expected '.' at the end of the program at line:",lineNo,token.tokenType )
				exit()
		else:
			print('Error in program function')
			print('Syntax error: Program name expected in line: ',lineNo,token.tokenType )
			exit()	
	else:
		print('Error in program function')
		print("Syntax error: Expected program in the beggining in line:", lineNo,token.tokenType )	
		exit()


def block(block_name): #added for int code
	global prog_name
	global token
	global checkReturn
	global symbolTable
	global symTableFile
	if token.tokenString=='{':
		token = lex()
		declarations()
		subprograms()
		genquad('BEGIN_BLOCK',block_name,'_','_') #added for int code
		if(len(symbolTable[len(symbolTable)-2]["entities"][-1]) != 0 and block_name!= prog_name): #s
			if(symbolTable[len(symbolTable)-2]["entities"][-1]["entity_type"]) == "subprogram": #s
				symbolTable[len(symbolTable)-2]["entities"][-1]["StartingQuad"] = nextquad() #s
		blockstatements()
		if block_name == prog_name: #added for int code
			genquad('HALT','_','_','_') #added for int code
		if (len(checkReturn)>0):	
			if (checkReturn[len(checkReturn)-1][0]==1) and (checkReturn[len(checkReturn)-1][1]==0): #s
				print('Error in block function') #s
				print('Semantic error: Expected return in', block_name,'in line',lineNo) #s
				exit() #s
			elif (checkReturn[len(checkReturn)-1][0]==0) and (checkReturn[len(checkReturn)-1][1]==1): #s
				print('Error in block function') #s
				print('Semantic error: Unexpected return in', block_name,'in line',lineNo) #s
				exit() #s
			checkReturn.pop() #s		
		genquad('END_BLOCK',block_name,'_','_')	#added for int code	
		addOffset() #s
		if token.tokenString=='}':
			token = lex()
		else:
			print('Error in statements function')
			print('Syntax error: expected "}" in line:', lineNo, token.tokenType)
			exit()
		symTableFile.write("Scope: "+ str(len(symbolTable)-1)) #s
		for entities in symbolTable[len(symbolTable)-1]["entities"]: #s
			symTableFile.write("\n")	#s
			symTableFile.write(str(entities)) #s
		symTableFile.write("\n") #s
		symTableFile.write("\n") #s
		createAssembly(block_name) #create assebly code for each scope
		removeScope() #s	
	else:
			print('Error in statements function')
			print('Syntax error: expected "{" in line:', lineNo, token.tokenType)
			exit()


def declarations():
	global token
	while (token.tokenType=='declaretk'):
		token=lex()
		varlist()
		if token.tokenString==';':
			token = lex()
		else:
			print('Error in declaration function')
			print('Syntax error: expected \';\' in line',lineNo,token.tokenType)
			exit()	
	return

def varlist():	
	global token
	if token.tokenType=='idtk':
		checkEntityExists(token.tokenString) #s
		addEntity(token.tokenString, "variable", None) #s
		vars.append(token.tokenString)
		token = lex()
		while token.tokenString==',':
			token = lex()
			if token.tokenType=='idtk':	
				vars.append(token.tokenString)
				checkEntityExists(token.tokenString) #s
				addEntity(token.tokenString, "variable", None) #s	
				token = lex()
			else:
				print('Error in varlist function')
				print('Syntax error: expected variable name in line:',lineNo,token.tokenType)
				exit()
				
def subprograms():
	global token
	global cfile
	while token.tokenType=='functiontk' or token.tokenType=='proceduretk':
		cfile=0
		subprogram()

def subprogram():
	global prog_name
	global token
	global checkReturn #s
	if token.tokenType=='functiontk':
		checkReturn.append([1,0]) #s
		token = lex()
		if token.tokenType=='idtk':
			checkEntityExists(token.tokenString) #s
			addEntity(token.tokenString, 'subprogram', 'function') #s
			addScope() #s
			block_name = token.tokenString #added for int code
			token = lex()
			if token.tokenString=='(':
				token = lex()
				formalparlist() #do i need to read next lex?
				if token.tokenString==')': 
					token = lex()
					if block_name == prog_name:
						print('Semantic error in line:',lineNo,'You cannot use program name as function name',token.tokenType)
						exit()	
					block(block_name) #added for int code
				else:
					print('Error in subprogram function')
					print('Syntax error: expected \')\' in line',lineNo,token.tokenType)
					exit()
			else:
				print('Error in subprogram function')
				print('Syntax error: expected \'(\' in line',lineNo,token.tokenType)
				exit()	
		else:
			print('Error in subprogram function')
			print('Syntax error: expected funtion name in line',lineNo,token.tokenType)
			exit()
	else:
		token=lex()
		if token.tokenType=='idtk':
			checkEntityExists(token.tokenString) #s
			addEntity(token.tokenString, 'subprogram', 'procedure') #s
			addScope() #s
			block_name = token.tokenString #added for int code
			token = lex()
			if token.tokenString=='(':
				token = lex()
				formalparlist() #do i need to read next lex?
				if token.tokenString==')': 
					token = lex()
					if block_name == prog_name:
						print('Semantic error in line:',lineNo,'You cannot use program name as procedure name',token.tokenType)
						exit()	
					block(block_name) #added for int code
				else:
					print('Error in subprogram function')
					print('Syntax error: expected \')\' in line',lineNo,token.tokenType)
					exit()
			else:
				print('Error in subprogram function')
				print('Syntax error: expected \'(\' in line',lineNo,token.tokenType)	
				exit()
		else:
			print('Error in subprogram function')
			print('Syntax error: expected funtion name in line',lineNo,token.tokenType)
			exit()

def formalparlist():
	global token
	formalparitem()
	while token.tokenString==',':
		token = lex()
		formalparitem()

def formalparitem():
	global token
	addArgument(token.tokenString) #s
	if token.tokenType=='intk' or token.tokenType=='inouttk':
		if token.tokenType=='intk':
			mode = 'In'
		else:
			mode = 'Inout'	
		token = lex()
		if token.tokenType=='idtk':
			checkEntityExists(token.tokenString) #s
			addEntity(token.tokenString, "parameter", mode) #s
			token = lex()
		else:
			print('Error in formalparitem function')
			print('Syntax error: expected parameter name in line:',lineNo,token.tokenType)
			exit()

def statements():
	global token
	if token.tokenString == '{':
		token = lex()
		statement()
		while token.tokenString == ';':
			token = lex()
			statement()
		if token.tokenString == '}':
			token = lex()	
		else:
			print('Error in statements function')
			print('Syntax error: expected \'}\' in line:',lineNo,token.tokenType)
			exit()	
	else:
		statement()
		if token.tokenString == ';':
			token = lex()
		else:
			print('Error in statements function')
			print('Syntax error: expected \';\' in line:',lineNo,token.tokenType)
			exit()	

def blockstatements():
	global token			
	statement()
	while token.tokenString == ';':
		token = lex()
		statement()	

def statement():
	global token
	if token.tokenType == 'idtk':
		assignStat()
	elif token.tokenType == 'iftk':
		ifStat()
	elif token.tokenType == 'whiletk':
		whileStat()
	elif token.tokenType == 'switchcasetk':
		switchcaseStat()
	elif token.tokenType == 'forcasetk':
		forcaseStat()
	elif token.tokenType == 'incasetk':
		incaseStat()
	elif token.tokenType == 'calltk':
		callStat()
	elif token.tokenType == 'returntk':
		returnStat()
	elif token.tokenType == 'inputtk':
		inputStat()
	elif token.tokenType == 'printtk':
		printStat()

def assignStat():
	global token
	if token.tokenType=='idtk':
		var_name = token.tokenString #added for int code
		token=lex()
		if token.tokenType=='asgntk':
			token=lex()
			ex_var = expression() #added for int code
			genquad(':=',ex_var,'_',var_name) #added for int code
		else:
			print('Error in assignStat function')
			print('Syntax error: Expected ":=". Wrong assignment in line:',lineNo,token.tokenType)
			exit()
	else:
		print('Error in assignStat function')
		print('Syntax error: Expected variable in line: ', lineNo,token.tokenType)
		exit()						

def ifStat():
	global token
	if token.tokenType == 'iftk':
		token = lex()
		if token.tokenString == '(':
			token = lex()
			if_var = condition() #added for int code
			if_true = if_var[0] #added for int code
			if_false = if_var[1] #added for int code
			if token.tokenString==')':
				token=lex()
				backpatch(if_true,nextquad()) #added for int code
				statements()
				elsepart(if_false) #added for int code
			else:
				print('Error in ifStat function')
				print('Syntax error: Expected \')\' in line',lineNo,token.tokenType)
				exit()
		else:
			print('Error in ifStat function')
			print('Syntax error: Expected \'(\' in line',lineNo,token.tokenType)
			exit()
	else:
		print('Error in ifStat function')
		print('Syntax error: Expected \'if\' in line',lineNo,token.tokenType)
		exit()	

def elsepart(cond_false): #added for int code
	global token
	if token.tokenType=='elsetk':
		if_list = makelist(nextquad()) #added for int code
		genquad('JUMP','_','_','_') #added for int code
		backpatch(cond_false,nextquad()) #added for int code
		token=lex()
		statements()
		backpatch(if_list,nextquad()) #added for int code
	else:
		backpatch(cond_false,nextquad()) #added for int code

def whileStat():
	global token
	if token.tokenType=='whiletk':
		token=lex()
		if token.tokenString=='(':
			token=lex()
			while_quad = nextquad() #added for int code
			while_cond = condition() #added for int code
			while_true = while_cond[0] #added for int code
			while_false = while_cond[1] #added for int code
			backpatch(while_true,nextquad()) #added for int code
			if token.tokenString==')':
				token=lex()
				statements()
				genquad('JUMP','_','_',while_quad) #added for int code
				backpatch(while_false,nextquad()) #added for int code
			else:
				print('Error in whileStat function')
				print('Syntax error: Expected ")" in line',lineNo,token.tokenType)
				exit()
		else:
			print('Error in whileStat function')
			print('Syntax error: Expected "(" in line',lineNo,token.tokenType)
			exit()
	else:
		print('Error in whileStat function')
		print('Syntax error: Expected "while" in line',lineNo,token.tokenType)
		exit()						

def switchcaseStat():
	global token
	if token.tokenType=='switchcasetk':
		token=lex()
		jlist=emptylist()
		while token.tokenString=='case':
			token=lex()
			if token.tokenString=='(':
				token=lex()
				cond=condition() #added for int code
				cond_true=cond[0] #added for int code
				cond_false=cond[1] #added for int code
				if token.tokenString==')':
					token=lex()
					backpatch(cond_true,nextquad()) #added for int code
					statements()
					temp_list=makelist(nextquad()) #added for int code
					genquad('JUMP','_','_','_') #added for int code
					jlist=merge(jlist,temp_list)
					backpatch(cond_false,nextquad()) #added for int code

				else:
					print('Error in switchcaseStat function')
					print('Syntax error: Expected ")" in line',lineNo,token.tokenType)
					exit()
			else:
				print('Error in switchcaseStat function')
				print('Syntax error: Expected "(" in line',lineNo,token.tokenType)
				exit()
		if token.tokenType=='defaulttk':
			token=lex()
			statements()
		else:
			print('Error in switchcaseStat function')
			print('Syntax error: Expected "default" in line',lineNo,token.tokenType)
			exit()
		backpatch(jlist,nextquad())	 #added for int code			
	else:
		print('Error in switchcaseStat function')
		print('Syntax error: Expected "switchcase" in line',lineNo,token.tokenType)
		exit()

def forcaseStat():
	global token
	if token.tokenType=='forcasetk':
		token=lex()
		quad1=nextquad() #added for int code
		while token.tokenType=='casetk':
			token=lex()
			if token.tokenString=='(':
				token=lex()
				cond=condition() #added for int code
				cond_true=cond[0] #added for int code
				cond_false=cond[1] #added for int code
				if token.tokenString==')':
					token=lex()
					backpatch(cond_true,nextquad()) #added for int code
					statements()
					genquad('JUMP','_','_',quad1) #added for int code
					backpatch(cond_false,nextquad()) #added for int code
				else:
					print('Error in forcaseStat function')
					print('Syntax error: Expected ")" in line',lineNo,token.tokenType)
					exit()
			else:
				print('Error in forcaseStat function')
				print('Syntax error: Expected "(" in line',lineNo,token.tokenType)
				exit()
		if token.tokenType=='defaulttk':
			token=lex()
			statements()
		else:
			print('Error in forcaseStat function')
			print('Syntax error: Expected "deafault" in line',lineNo,token.tokenType)
			exit()			
	else:
		print('Error in forcaseStat function')
		print('Syntax error: Expected "forcase" in line',lineNo,token.tokenType)
		exit()

def incaseStat():
	global token
	if token.tokenType=='incasetk':
		token=lex()
		flag=newtemp() #added for int code
		quad1=nextquad() #added for int code
		genquad(':=',1,'_',flag) #added for int code
		while token.tokenType=='casetk':
			token=lex()
			if token.tokenString=='(':
				token=lex()
				cond=condition() #added for int code
				cond_true=cond[0] #added for int code
				cond_false=cond[1] #added for int code
				if token.tokenString==')':
					token=lex()
					backpatch(cond_true,nextquad()) #added for int code
					genquad(':=','0','_',flag) #added for int code
					statements()
					backpatch(cond_false,nextquad()) #added for int code
				else:
					print('Error in incaseStat function')
					print('Syntax error: Expected ")" in line',lineNo,token.tokenType)
					exit()
			else:
				print('Error in incaseStat function')
				print('Syntax error: Expected "(" in line',lineNo,token.tokenType)
				exit()
		genquad("=",flag,'0',quad1) #added for int code 		
	else:
		print('Error in incaseStat function')
		print('Syntax error: Expected "incase" in line',lineNo,token.tokenType)
		exit()

def returnStat():
	global token
	global cfile
	global checkReturn
	if token.tokenType=='returntk':
		checkReturn[len(checkReturn)-1][1]=1 #s
		cfile=0
		token=lex()
		if token.tokenString=='(':
			token=lex()
			ex_var = expression() #added for int code
			genquad('RET',ex_var,'_','_') #added for int code
			if token.tokenString==')':
				token=lex()
			else:
				print('Error in returnStat function')
				print('Syntax error: Expected ")" in line2',lineNo,token.tokenType)
				exit()
		else:
			print('Error in returnStat function')
			print('Syntax error: Expected "(" in line',lineNo,token.tokenType)
			exit()				
		return ex_var #added for int code			

def callStat():
	global token
	global cfile
	if token.tokenType=='calltk':
		cfile=0
		token=lex()
		if token.tokenType=='idtk':
			called_name = token.tokenString #added for int code
			token=lex()
			if token.tokenString=='(':
				token=lex()
				actualparlist(called_name) 
				genquad('CALL','_','_',called_name) #added for int code
				if token.tokenString==')':
					token=lex()
				else:
					print('Error in callStat function')
					print('Syntax error: Expected ")" in line',lineNo,token.tokenType)
					exit()
			else:
				print('Error in callStat function')
				print('Syntax error: Expected "(" in line',lineNo,token.tokenType)
				exit()			
		else:
			print('Error in callStat function')
			print('Syntax error: Expected name in line:',lineNo,token.tokenType)
			exit()
	else:
		print('Error in callStat function')	
		print('Syntax error: Expected "call" in line',lineNo,token.tokenType)
		exit()					

def printStat():
	global token
	if token.tokenType=='printtk':
		token=lex()
		if token.tokenString=='(':
			token=lex()
			ex_var = expression() #added for int code
			genquad('PRINT',ex_var,'_','_') #added for int code
			if token.tokenString==')':
				token=lex()
			else:
				print('Error in printStat function')
				print('Syntax error: Expected ")" in line',lineNo,token.tokenType)
				exit()
		else:
			print('Error in printStat function')
			print('Syntax error: Expected "(" in line',lineNo,token.tokenType)
			exit()					
	else:
		print('Error in printStat function')	
		print('Syntax error: Expected "print" in line',lineNo,token.tokenType)
		exit()		

def inputStat():
	global token
	if token.tokenType=='inputtk':
		token=lex()
		if token.tokenString=='(':
			token=lex()
			if token.tokenType=='idtk':
				id_name = token.tokenString #added for int code
				searchEntity(id_name, "VAR")  #s
				genquad('INPUT',id_name,'_','_') #added for int code
				token=lex()
				if token.tokenString==')':
					token=lex()
				else:
					print('Error in inputStat function')
					print('Syntax error: Expected ")" in line',lineNo,token.tokenType)
					exit()
			else:
				print('Error in inputStat function')
				print('Syntax error: Expected variable name in line',lineNo,token.tokenType)
				exit()
		else:
			print('Error in inputStat function')
			print('Syntax error: Expected "(" in line',lineNo,token.tokenType)
			exit()			
	else:
		print('Error in inputStat function')
		print('Syntax error: Expected "input" in line',lineNo,token.tokenType)
		exit()

def actualparlist(name): #added for int code
	global token
	if token.tokenType=='intk' or token.tokenType=='inouttk':
		parsList=[]
		modeList=[] #s
		tempItem=actualparitem() #s
		modeList.append(tempItem[1].lower()) #s
		parsList.append(tempItem) #s
		while token.tokenString==',':
			token=lex() 
			tempItem=actualparitem() #s
			modeList.append(tempItem[1].lower()) #s
			parsList.append(tempItem) #s
		checkArguments(name, modeList) #s
		for items in parsList:
			genquad('PAR',items[0],items[1],'_') #added for int code
	else:
		print('Error in actualparlist function')			
		print('Syntax error: Expected in or inout command in line',lineNo,token.tokenType)
		exit()		

def actualparitem():
	global token
	if token.tokenType=='intk':
		token=lex()
		var=expression() #added for int code
		return [var,'IN'] #added for int code
	elif token.tokenType=='inouttk':
		token=lex()
		if token.tokenType!='idtk':
			print('Error in actualparitem function')
			print('Syntax error: Expected variable name in line',lineNo,token.tokenType)
			exit()
		else:
			var = token.tokenString #added for int code
			searchEntity(var, "VAR")  #s
			token = lex()
			return [var,'INOUT'] #added for int code
	else:
		print('Error in actualparitem function')			
		print('Syntax error: Expected in or inout command in line',lineNo,token.tokenType)
		exit()

def condition():
	global token
	bool1 = boolterm() #added for int code
	term_true = bool1[0] #added for int code
	term_false = bool1[1] #added for int code
	while token.tokenType=='ortk':
		token=lex()
		backpatch(term_false,nextquad()) #added for int code
		bool2 = boolterm() #added for int code
		term_true = merge(term_true, bool2[0]) #added for int code
		term_false = bool2[1] #added for int code
	return [term_true,term_false] #added for int code

def boolterm():
	global token		
	bool1 = boolfactor() #added for int code
	factor_true = bool1[0] #added for int code
	factor_false = bool1[1] #added for int code
	while token.tokenType=='andtk':
		token=lex()
		backpatch(factor_true, nextquad()) #added for int code
		bool2 = boolfactor() #added for int code
		factor_false = merge(factor_false, bool2[1]) #added for int code
		factor_true = bool2[0] #added for int code
	return [factor_true, factor_false] #added for int code

def boolfactor():
	global token
	if token.tokenType=='nottk':
		token=lex()
		if token.tokenString=='[':
			token=lex()
			cond =condition() #added for int code
			cond_true= cond[0] #added for int code
			cond_false= cond[1] #added for int code
			if token.tokenString==']':
				token=lex()
			else:
				print('Error in boolfactor function')
				print('Syntax error: Expected "]" in line',lineNo,token.tokenType)
				exit()
			return [cond_true,cond_false] #added for int code	
		else:
			print('Error in boolfactor function')
			print('Syntax error: Expected "[" in line',lineNo,token.tokenType)
			exit()
	elif token.tokenString=='[':
		token=lex()
		cond= condition() #added for int code
		cond_true= cond[0] #added for int code
		cond_false =cond[1] #added for int code
		if token.tokenString==']':
			token=lex()
		else:
			print('Error in boolfactor function')
			print('Syntax error: Expected "]" in line',lineNo,token.tokenType)
			exit()
		return [cond_true,cond_false] #added for int code		
	else:
		exp1 = expression()
		if token.tokenType=='relOpertk':
			relop= token.tokenString #added for int code
			token=lex()
		else:
			print('Error in boolfactor function')
			print('Syntax error: Expected relational operator in line',lineNo,token.tokenType)
			exit()
		exp2= expression() #added for int code
		exp_true=makelist(nextquad()) #added for int code
		genquad(relop,exp1,exp2,'_') #added for int code
		exp_false=makelist(nextquad()) #added for int code
		genquad('JUMP','_','_','_') #added for int code
		return [exp_true,exp_false] #added for int code

def expression():
	global token
	sign=optionalSign() #added for int code
	t_var1=sign+term() #added for int code
	while token.tokenType=='addtk':
		sign=token.tokenString #added for int code
		token=lex() 
		t_var2=term() #added for int code
		temp=newtemp() #added for int code
		genquad(sign,t_var1,t_var2,temp) #added for int code
		t_var1=temp #added for int code
	return t_var1 #added for int code

def term():
	global token
	f_var1=factor() #added for int code
	while token.tokenType=='multk':
		muloper=token.tokenString #added for int code
		token=lex() 
		f_var2=factor() #added for int code
		temp=newtemp() #added for int code
		genquad(muloper,f_var1,f_var2,temp) #added for int code
		f_var1=temp #added for int code
	return f_var1 #added for int code

def factor():
	global token
	
	if token.tokenType=='numtk':
		factor_var=token.tokenString #added for int code
		token=lex()
	elif token.tokenString=='(':
		token=lex()
		factor_var=expression() #added for int code
		if token.tokenString==')':
			token=lex()	
		else:
			print('Error in factor function')
			print('Syntax error: Expected ")" in line',lineNo,token.tokenType)
			exit()
	else:
		if token.tokenType=='idtk':
			var_name=token.tokenString #added for int code
			token=lex()
			tail_var=idtail(var_name) #added for int code
			if tail_var=='VAR': #added for int code
				searchEntity(var_name, "VAR") #s
				factor_var=var_name
			else: #added for int code
				searchEntity(var_name, "FUNC")  #s
				factor_var=tail_var #added for int code	
		else:
			print('Error in factor function')
			print('Syntax error: Expected variable name in line',lineNo,token.tokenType)
			exit()
	return factor_var #added for int code

def idtail(var_name): #added for int code
	global token
	global cfile
	func_flag=0 #added for int code
	if token.tokenString=='(':
		token=lex()
		if token.tokenString!=')': #added for int code
			actualparlist(var_name) #added for int code
			func_flag=1 #added for int code
		if token.tokenString==')':
			token=lex()	
		else:
			print('Error in idtail function')
			print('Syntax error: Expected ")" in line idtail',lineNo,token.tokenType,token.tokenString)
			exit()
		if func_flag==1:
			cfile=0
			ret=newtemp() #added for int code
			genquad('PAR',ret,'RET','_') #added for int code
			genquad('CALL','_','_',var_name) #added for int code
			func_flag=0 #added for int code
			return ret #added for int code
	else:
		return 'VAR' #added for int code											

def optionalSign():
	global token
	sign='' #added for int code
	if token.tokenType=='addtk':
		if token.tokenString=='-': #added for int code
			sign='-'
		token=lex()
	return sign #added for int code

def createIntCode(): #int code creator
	int_name=sys.argv[1][:-3]
	f = open(int_name + '.int', 'w') 
	for i in range(len(quadsList)): 
		f.write(quadsList[i][0] +':'+str(quadsList[i][1][0])+','+str(quadsList[i][1][1])+','+str(quadsList[i][1][2])+','+str(quadsList[i][1][3])+'\n')
	f.close() 

#intermidiate code out files start

def createCCode(): #C code creator
	global vars
	varstr = '' 
	main = [] 
	line_c = 1 
	int_name=sys.argv[1][:-3]
	f = open(int_name+'.int', 'r') 

	#making main 

	for line in f: 
		line = line.replace(':',' ',1) 
		line = line.replace(',',' ')
		line = line.replace('\n','') 
		text = line.split(' ') 
		if text[1] == ':=':
			main.append('\tL_' + str(line_c) + ': ' + str(text[4]) + '=' + str(text[2]) + ';\n')
		elif text[1] == '=':
			main.append('\tL_' + str(line_c) + ': ' + 'if (' + str(text[2]) + '==' + str(text[3]) + ') goto L_' + str(int(text[4])) + ';\n')	
		elif text[1] == '<=':
			main.append('\tL_' + str(line_c) + ': ' + 'if (' + str(text[2]) + '<=' + str(text[3]) + ') goto L_' + str(int(text[4])) + ';\n')
		elif text[1] == '>=':
			main.append('\tL_' + str(line_c) + ': ' + 'if (' + str(text[2]) + '>=' + str(text[3]) + ') goto L_' + str(int(text[4])) + ';\n')
		elif text[1] == '>':
			main.append('\tL_' + str(line_c) + ': ' + 'if (' + str(text[2]) + '>' + str(text[3]) + ') goto L_' + str(int(text[4])) + ';\n')
		elif text[1] == '<':
			main.append('\tL_' + str(line_c) + ': ' + 'if (' + str(text[2]) + '<' + str(text[3]) + ') goto L_' + str(int(text[4])) + ';\n')	
		elif text[1] == '<>':
			main.append('\tL_' + str(line_c) + ': ' + 'if (' + str(text[2]) + '!=' + str(text[3]) + ') goto L_' + str(int(text[4])) + ';\n')
		elif text[1] == '+':
			main.append('\tL_' + str(line_c) + ': ' + str(text[4]) + '=' + str(text[2]) + '+' + str(text[3]) + ';\n')
		elif text[1] == '-':
			main.append('\tL_' + str(line_c) + ': ' + str(text[4]) + '=' + str(text[2]) + '-' + str(text[3]) + ';\n')
		elif text[1] == '*':
			main.append('\tL_' + str(line_c) + ': ' + str(text[4]) + '=' + str(text[2]) + '*' + str(text[3]) + ';\n')
		elif text[1] == '/':
			main.append('\tL_' + str(line_c) + ': ' + str(text[4]) + '=' + str(text[2]) + '/' + str(text[3]) + ';\n')	
		elif text[1] == 'PRINT':
			main.append('\tL_' + str(line_c) + ': ' + 'printf(\"%d\\n\", ' + text[2] + ');\n')
		elif text[1] == 'JUMP':
			main.append('\tL_' + str(line_c) + ': ' + 'goto L_' + str(int(text[4])) + ';\n')		
		elif text[1] == 'INPUT':
			main.append('\tL_' + str(line_c) + ': ' + 'scanf(\"%d\", &' + text[2] + ');\n')
		elif text[1] == 'HALT':
			main.append('\tL_' + str(line_c) + ': {}\n')
			main.append('}')
		else:
			line_c -= 1 
		line_c += 1

	#make C output file

	f.close() 
	if vars != []:
		varstr= vars[0]
		for i in range(1,len(vars)): 
			varstr += ','
			varstr += vars[i]
		varstr += ';'
	c_name = sys.argv[1][:-3]
	c_out = open(c_name+'.c', 'w') 
	c_out.write('#include <stdio.h>\n')
	c_out.write('\n')
	c_out.write('int main()\n')
	c_out.write('{\n')
	if vars != []:
		c_out.write('\tint ' +varstr+'\n') 
	c_out.write('\tL_0: \n')
	for l in main: 
		c_out.write(l)
	c_out.close() 

#intermidiate code out files finish	
#symbol table

def addScope(): #create new Scope
	global symbolTable
	scope = {}
	scope["entities"] = []
	scope["offset"] = 12
	symbolTable.append(scope)

def addOffset(): #add 4 to offset of each entity if not subprogram
	global symbolTable
	offset = 12
	for entity in symbolTable[len(symbolTable)-1]["entities"]:
		if entity["entity_type"] != "subprogram":
			offset += 4
	if len(symbolTable) > 1:
		entitiesLength = len(symbolTable[len(symbolTable)-2]["entities"])
		symbolTable[len(symbolTable)-2]["entities"][entitiesLength-1]["offset"] = offset


def removeScope(): 
	global symbolTable 
	symbolTable.pop()


def addEntity(entity_name, entity_type, subprog): #append new entity to symbol table
	global symbolTable

	entity = {}
	entity["entity_name"] = entity_name
	entity["entity_type"] = entity_type

	if entity_type == "variable":
		entity["offset"] = symbolTable[len(symbolTable)-1]["offset"]
		symbolTable[len(symbolTable)-1]["offset"] += 4
	elif entity_type == "subprogram":
		entity["function_type"] = subprog
		entity["arguments"] = []
		entity["offset"] = 0
		entity["StartingQuad"] = 0
	elif entity_type == "parameter":
		entity["parMode"] = subprog
		entity["offset"] = symbolTable[len(symbolTable)-1]["offset"]
		symbolTable[len(symbolTable)-1]["offset"] += 4
	elif entity_type == "tempvar":
		entity["offset"] = symbolTable[len(symbolTable)-1]["offset"]
		symbolTable[len(symbolTable)-1]["offset"] += 4

	symbolTable[len(symbolTable)-1]["entities"].append(entity)	

def addArgument(parMode): # add the arguments of a subprogram
	global symbolTable

	argument = {}
	argument["parMode"] = parMode
	entitiesLength = len(symbolTable[len(symbolTable)-2]["entities"])
	if entitiesLength > 0:
		symbolTable[len(symbolTable)-2]["entities"][entitiesLength-1]["arguments"].append(argument)

def searchEntity(name, TYPE): # search if an entity the program needs exist
	global symbolTable 	

	for scope in symbolTable:
		for entity in scope["entities"]:
			if name == entity["entity_name"]:
				if TYPE == "VAR":
					if entity["entity_type"] in ["variable", "parameter", "tempvar"]:
						return entity
				elif TYPE == "PROC": 
					if entity["entity_type"] == "subprogram" and entity["function_type"] == "procedure":
						return entity
				elif TYPE == "FUNC": 
					if entity["entity_type"] == "subprogram" and entity["function_type"] == "function":
						return entity
				elif TYPE == "subprogram":
					return entity
	print("Semantic Error: Line", lineNo, " Entity type:", TYPE, "", name, " not found!")
	exit()

def checkEntityExists(name): # check if a variable already exists 
	global symbolTable 
	
	for entity in symbolTable[len(symbolTable)-1]["entities"]:
		if name == entity["entity_name"]:
			print("Semantic Error: Line", lineNo, "-> Entity ", name, " already exists!")
			exit()

def checkArguments(id_name, pars): #check if the arguments are correct when you call a subprogram
	
	entity = searchEntity(id_name, "subprogram")

	if len(entity["arguments"]) != len(pars):
		print("Semantic Error: Line", lineNo, "-> In ", entity["entity_type"], " ", entity["entity_name"], " wrong number of arguments!")
		exit()
	i = 0
	for parameter in pars:
		if entity["arguments"][i]["parMode"] != parameter:
			print("Semantic Error: Line", lineNo, "-> In ", entity["entity_type"], " ", entity["entity_name"], " wrong type of arguments!")
			exit()
		i += 1
#end of symbol table

#final code
def varInfo(name): # find the entity in the symbol table and return info and scope
	global symbolTable
	level = 0 
	for scope in reversed(symbolTable):
		for entity in scope["entities"]:
			if name == entity["entity_name"]:
				return [entity, len(symbolTable)-1-level]
		level += 1

def gnlvcode(name):
	global symbolTable
	entity = varInfo(name)
	produce('   	lw t0,-8(sp)')
	for scopes in symbolTable:
		produce('   	lw t0,-8(t0)')
	produce('   	addi t0, t0, -' + str(entity[0]['offset']))

def loadvr(v, reg):
	global symbolTable
	if(v.lstrip('-').isdigit()):							
		produce('   	li t'+str(reg)+', '+str(v)) 
	else:
		varinfo = varInfo(v)
		if varinfo[1] == 0 and len(symbolTable)!=1:
			produce('   	lw t'+str(reg)+', -'+str(varinfo[0]['offset'])+'(gp)')
		elif varinfo[1] == len(symbolTable)-1:
			if varinfo[0]['entity_type'] == 'variable' or varinfo[0]['entity_type'] == 'tempvar' or (varinfo[0]['entity_type'] == 'parameter' and varinfo[0]['parMode'] == 'In'):
				produce('   	lw t'+str(reg)+', -'+str(varinfo[0]['offset'])+'(sp)')
			elif varinfo[0]['entity_type'] == 'parameter' and varinfo[0]['parMode'] == 'Inout':
				produce('   	lw t0, -'+str(varinfo[0]['offset'])+'(sp)')
				produce('   	lw t'+str(reg)+', (t0)')
		else:
			if varinfo[0]['entity_type'] == 'variable' or (varinfo[0]['entity_type'] == 'parameter' and varinfo[0]['parMode'] == 'In'):	
				gnlvcode(v)
				produce('   	lw t'+str(reg)+', (t0)')
			elif varinfo[0]['entity_type'] == 'parameter' and varinfo[0]['parMode'] == 'Inout':
				gnlvcode(v)
				produce('   	lw t0, (t0)')
				produce('   	lw t'+str(reg)+', (t0)')	

def storerv(reg, v):
	global symbolTable
	varinfo = varInfo(v)
	if varinfo[1] == 0 and len(symbolTable)!=1:
		produce('   	sw t'+str(reg)+', -'+str(varinfo[0]['offset'])+'(gp)')
	elif varinfo[1] == len(symbolTable)-1:
		if varinfo[0]['entity_type'] == 'variable' or varinfo[0]['entity_type'] == 'tempvar' or (varinfo[0]['entity_type'] == 'parameter' and varinfo[0]['parMode'] == 'In'):
			produce('   	sw t'+str(reg)+', -'+str(varinfo[0]['offset'])+'(sp)')
		elif varinfo[0]['entity_type'] == 'parameter' and varinfo[0]['parMode'] == 'Inout':
			produce('   	lw t0, -'+str(varinfo[0]['offset'])+'(sp)')
			produce('   	sw t'+str(reg)+', (t0)')
	else:
		if varinfo[0]['entity_type'] == 'variable' or (varinfo[0]['entity_type'] == 'parameter' and varinfo[0]['parMode'] == 'In'):	
			gnlvcode(v)
			produce('   	sw t'+str(reg)+', (t0)')
		elif varinfo[0]['entity_type'] == 'parameter' and varinfo[0]['parMode'] == 'Inout':
			gnlvcode(v)
			produce('   	lw t0, (t0)')
			produce('   	sw t'+str(reg)+', (t0)')		

def createAssembly(block_name):
	global prog_name
	global quadsList
	global labelNumbers
	global symbolTable
	global lock 
	for scope in symbolTable:
		framelength = 12
		for entity in reversed(scope["entities"]):
			if entity['entity_type'] != subprogram:
				framelength = entity['offset']
				break
	if labelNumbers == 0:
		produce('.data') 
		produce('   	str_nl: .asciz "\\n"')
		produce('.text')
		produce('   	b Lmain')
	if block_name == prog_name:
		produce('Lmain:')	
	else:
		produce(quadsList[labelNumbers][1][1]+':')	
	for quad in range(labelNumbers, len(quadsList)):
		produce('L'+quadsList[quad][0]+':')
		if quadsList[quad][1][0]=='JUMP':
			produce('   	b L'+quadsList[quad][1][3])
		elif(quadsList[quad][1][0] in ['=','<>', '>', '<', '<=', '>=']):
			loadvr(quadsList[quad][1][1], 1)
			loadvr(quadsList[quad][1][2], 2)
			if quadsList[quad][1][0] == '=':
				produce('   	beq, t1, t2, L'+quadsList[quad][1][3])
			elif quadsList[quad][1][0] == '<>':
				produce('   	bne, t1, t2, L'+quadsList[quad][1][3])
			elif quadsList[quad][1][0] == '<':
				produce('   	blt, t1, t2, L'+quadsList[quad][1][3])
			elif quadsList[quad][1][0] == '>':
				produce('   	bgt, t1, t2, L'+quadsList[quad][1][3])
			elif quadsList[quad][1][0] == '<=':
				produce('   	ble, t1, t2, L'+quadsList[quad][1][3])
			elif quadsList[quad][1][0] == '>=':
				produce('   	bge, t1, t2, L'+ quadsList[quad][1][3])
		elif quadsList[quad][1][0]== ':=':
			loadvr(quadsList[quad][1][1], 1)
			storerv(1, quadsList[quad][1][3])
		elif(quadsList[quad][1][0] in ['+','-','/','*']):
			loadvr(quadsList[quad][1][1], 1)
			loadvr(quadsList[quad][1][2], 2)
			if quadsList[quad][1][0] == '+':
				produce('   	add t1, t1, t2')
			elif quadsList[quad][1][0] == '-':
				produce('   	sub t1, t1, t2')
			elif quadsList[quad][1][0] == '/':
				produce('   	div t1, t1, t2')
			else:		
				produce('   	mul t1, t1, t2')
			storerv(1, quadsList[quad][1][3])
		elif quadsList[quad][1][0]== 'RET':
			loadvr(quadsList[quad][1][1], 1)
			produce('   	lw t0, -8(sp)')
			produce('   	sw t1, (t0)')
		elif quadsList[quad][1][0] == 'INPUT':
			produce('   	li a7, 5')
			produce('   	ecall')
			produce('   	move t1, a0')
			storerv(1,quadsList[quad][1][1])
		elif quadsList[quad][1][0] == 'PRINT':
			loadvr(quadsList[quad][1][1],1)	
			produce('   	move a0, t1')
			produce('   	li a7, 1')
			produce('   	ecall')
			produce('   	la a0, str_nl')
			produce('   	li a7, 4')
			produce('   	ecall')
		elif quadsList[quad][1][0] == 'BEGIN_BLOCK':
			if  prog_name == block_name:
				produce('   	addi sp, sp, '+ str(framelength+4))
				produce('   	move gp, sp')
			else:
				produce('   	sw ra, -0(sp)')
		elif quadsList[quad][1][0] == 'END_BLOCK':
			if  prog_name == block_name:
				produce('   	li a0, 0')
				produce('   	li a7, 93')
				produce('   	ecall')	
			else:
				produce('   	lw ra, -0(sp)')
				produce('   	jr ra')
		elif quadsList[quad][1][0] == 'PAR' or quadsList[quad][1][0] == 'CALL':	
			if lock == 0:
				for parquads in range(quad,len(quadsList)):
					if quadsList[parquads][1][0] == 'CALL':	
						funcinfo = varInfo(quadsList[parquads][1][3])
						break
				produce('   	addi fp, sp, '+ str(funcinfo[0]['offset']))
				lock = 1
			if 	quadsList[quad][1][2] == 'IN':
				loadvr(quadsList[quad][1][1], 1)
				entity = varInfo(quadsList[quad][1][1])
				produce('   	sw t1, -'+ str(entity[0]['offset'])+'(fp)')
			elif quadsList[quad][1][2] == 'INOUT':
				entity = varInfo(quadsList[quad][1][1])
				#print(entity)
				if funcinfo[1] == entity[1]:
					if entity[0]['entity_type'] == 'variable' or (entity[0]['entity_type'] == 'parameter' and entity[0]['parMode'] == 'IN'):
						produce('   	addi t0, sp, -'+str(entity[0]['offset']))
						produce('   	sw t0, -'+ str(entity[0]['offset'])+'(fp)')
					else:
						produce('   	lw t0, -'+str(entity[0]['offset'])+'(sp)')
						produce('   	sw t0, -'+str(entity[0]['offset'])+'(fp)')
				else:
					if entity[0]['entity_type'] == 'variable' or (entity[0]['entity_type'] == 'parameter' and entity[0]['parMode'] == 'IN'):
						gnlvcode(entity[0]["entity_name"])
						produce('   	lw t0, -'+str(entity[0]['offset'])+'(fp)')	
					else:
						gnlvcode(entity[0]["entity_name"])
						produce('   	lw t0, (t0)')
						produce('   	sw t0, -'+str(entity[0]['offset'])+'(fp)')
			elif quadsList[quad][1][2] == 'RET':
				entity = varInfo(quadsList[quad][1][1])
				produce('   	addi t0, sp ,-' + str(entity[0]['offset']))
				produce('   	sw t0, -8(fp)')
			elif quadsList[quad][1][0] == 'CALL':
				lock = 0
				if len(symbolTable) == funcinfo[1]:
					produce('   	lw t0, -4(sp)')
					produce('   	sw t0, -4(fp)')
				else:
					produce('   	sw sp, -4(fp)')	
				produce('   	addi sp, sp, '+ str(funcinfo[0]['offset']))
				produce('   	jal '+ quadsList[parquads][1][3])
				produce('   	addi sp, sp, -'+ str(funcinfo[0]['offset']))
	labelNumbers = len(quadsList)

def produce(code):
	global finalFile
	finalFile.write(code + '\n')
#end of final code

#globals for first phase (sytax,lex)
vars = []
cfile = 1
quadsList = []
temp_count = 0
prog_name=''
lineNo = 1
token = Token('','',lineNo)

#globals for second phase(intermidiate, symbol table)
checkReturn = []
symbolTable = []

#globals for final phase (final code)
labelNumbers = 0
lock = 0

ci_file = sys.argv[1]
try:
	ci_prog = open(ci_file)
except IOError:
	print("Error: Could not find the file", ci_file)
	exit()
ci_name = sys.argv[1][:-3]	
symTableFile = open(ci_name+".symb.txt","w")	
finalFile = open(ci_name+".asm","w")
program()
createIntCode()
if cfile == 1:
	createCCode()
ci_prog.close
symTableFile.close

