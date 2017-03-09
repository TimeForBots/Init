class bind :
	bind = None
	command = None

	def __init__(self, bindstr, commandstr) :
		self.bind = bindstr
		self.command = commandstr

	def toCFGEntry() :
		return '"' + bind + command + '"'

def isBinded(bindlist, bindstr) :
	for bindobj in bindlist :
		if bindobj.bind == bindstr :
			return True

	return False

def getBindFromList(bindlist, bindstr) :
	for bindobj in bindlist :
		if bindobj.bind == bindstr :
			return bindobj

	return None
