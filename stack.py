import inspect
import time
import numbers
class Stack(list):
	def __init__(self):
		self.geneMap = [
                  (lambda a,b: a+b), # Add
                  (lambda a,b: a-b), # Subtract
                  (lambda a,b: a/b), # Divide
                  (lambda a,b: a*b), # Multiply
                  self.drop, # Drop
                  self.swap, # Swap
                  self.duplicate, # Duplicate
                  self.store, # Store
		  self.recall, # Recall
                  (lambda a,b: True if a < b else False), # Is less than
                  (lambda a,b: True if a > b else False), # Is greater than
                  (lambda a,b: True if a == b else False), # Is equal to
                  (lambda a,b: True if a or b else False), # OR
                  (lambda a,b: True if (a and b) else False), # AND
                  (lambda a,b: a % b), # Modulo
                  (lambda arg1,do1,do2: do1 if arg1 else do2), #a,b,c: If a then b else c
                  (lambda: True), # True
                  (lambda: False) # False
                  ]
		self.memory = {}
		self.instructionSetLength = len(self.geneMap)
		self.execTime = 0

	def setInitialValue(self,value):
		self.clear()
		self.append(value)		
			
	def clear(self):
		### Reset the stack's state.
		self.memory = {}
		self.execTime = 0
		# TODO: Do something more elegant than:
		while len(self) > 0:
			self.pop()
	def drop(self):
		### Remove the last item from the stack.
		self.pop()
		return None

	def swap(self):
		### Switch the last two items on the stack.
		self.append(self.pop(-2))

	def duplicate(self):
		### Copy the last item on the stack and append it
		self.append(self[-1])
		
	def evaluate(self,organism,stackTest=False):
		#print "Evaluating organism: " + str(decode(organism))
		startTime = time.clock()
		for gene in organism:
			if gene >= len(self.geneMap):
				self.append(gene-len(self.geneMap))
			else:
				nArgs = getNumArgs((self.geneMap[gene],gene))
				popped = []
				try:
					for i in range(nArgs):
						popped.append(self.pop())
				except IndexError:
					return None
				popped.reverse()
				args = popped
				if stackTest:
					print(args)
				try:
					result = self.geneMap[gene](*args)
				except IndexError:
					return None
				except ZeroDivisionError:
					return None
				except KeyError:
					return None
				if result or result == 0:
					self.append(result)
		stopTime = time.clock()
		self.execTime = stopTime - startTime
		if stackTest:
			return None
		else:
			
			try:
				return self.pop()
			except IndexError:
				return None

	def store(self):
		index = self.pop()
		value = self.pop()
		self.memory[index] = value
		return None

	def recall(self):
		return self.memory[self.pop()]
		
		
def stackTest():
	### Provides an environment for interactively testing the stack.
	stack = Stack()
	while True:
		print "Raw stack contents: " + str(stack)
		lineNo = len(stack)
		i = 0
		for line in stack:
			print str(lineNo-i)+ ' : ' + str(line)
		i = 0
		userInput = raw_input('> ')
		parsedInput = encode(userInput)
		stack.evaluate(parsedInput,stackTest=True)

def getNumArgs(function):
	### Returns the number of arguments for a function.
	executable = function[0]
	name = function[1]
	#print "Getting arguments for " + decode([name])
	arguments = inspect.getargspec(executable)[0]
	if "self" in arguments:
		return len(arguments)-1
	else:
		return len(arguments)

def decode(instructions):
	### Convert "machine" language to human-readable language.
	encMap = ['+','-','/','*','DROP','SWAP','DUP','STO','RCL','<','>','==','OR','AND','MOD','IFTE','TRUE','FALSE']
	decoded = ''
	for i in instructions:
		try:
			decoded = decoded + encMap[int(i)] + ' '
		except IndexError:
			decoded = decoded + str(i-len(encMap)) + ' '
	return decoded

def encode(rawString):
	### Convert human-readable language to "machine" language.
	encMap = ['+','-','/','*','DROP','SWAP','DUP','STO','RCL','<','>','==','OR','AND','MOD','IFTE','TRUE','FALSE']
	organism = []
	tokens = rawString.split(' ')
	for token in tokens:
		try:
			organism.append(int(token.strip())+len(encMap))
			print "Pushing " + str(int(token)+len(encMap)) + " onto the stack."
		except ValueError:	
			try:
				print "You entered " + str(decode([encMap.index(token)]))
				organism.append(encMap.index(token))
			except IndexError:
				print("Invalid.")
	print("Evaluating instruction array: " + str(organism))
	return organism

