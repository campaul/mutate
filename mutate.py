#from __future__ import division
# TODO: Make a new module for statistical analysis?
import random
import stack as StackMachine
import math
import string
def spawn(minLength,maxLength,maxValue,parents=None,mutationRate=.001):
	### Produce a new organism provided the number of genes and optional parents.
	### An organism is a list of integers, where each integer is a stack instruction.
	
	### If a list of parents is provided:	
	baby = []
	length = random.randint(minLength,maxLength)
	if parents:
		for i in xrange(length):
			parent=random.choice(parents)
			try:
				baby.append(parent[i])
			except IndexError:
				return mutate(baby,maxValue,mutationRate)
		return mutate(baby,maxValue,mutationRate)

	### If no parents are provided, randomly generate a list of integers.
	for index in range(length):
		baby.append(random.randint(0,maxValue))
	return baby


def mutate(organism,maxValue,mutationRate):
	### Introduce random variation into the genome
	i = 0
	while i < len(organism) :
		## TODO: Make a better function for determining whether mutation happens
		option = random.randint(1,4)
		if roll_dice(mutationRate):
			option = random.choice((1,3))
			if option == 1:
				organism[i] = random.choice((0,maxValue)) # Replace
			if option == 2:
				organism.remove(i) # Remove
			if option == 3:
				organism.insert(i,random.choice((0,maxValue))) # Insert
			if option == 4:
				random.shuffle(organism)
				
		i += 1
	return organism

def buildPopulation(popSize,minLength,maxLength,maxValue,mutationRate,prevPopulation=None):
	### Build a new population, optionally taking in existing organisms to be bred
	### Args: population size, length of the genome, highest possible value for gene, population
	newPopulation = []
	if prevPopulation:
		for index in range(popSize):
			mom = random.choice(prevPopulation)
			dad = random.choice(prevPopulation)
			newPopulation.append(spawn(minLength,maxLength,maxValue,[mom,dad],mutationRate))
		return newPopulation
	else: 
		for index in range(popSize):
			newPopulation.append(spawn(minLength,maxLength,maxValue))
	return newPopulation



def getFitness(organism,qaTable,stack):
	### Determine the fitness of a single organism
	score = 0
	timePenalty = 0
	lengthPenalty = 0
	#print "Evaluating fitness of individual " + StackMachine.decode(organism)
	for i in xrange(50):
		test = generateTestValues()
		stack.append(test[0])
		result = stack.evaluate(organism)
		if test[1]:
			correct = 'TRUE'
		else:
			correct = 'FALSE'
		
		
		if result == test[1]:
			score += 1
			
		elif result == None:
			stack.clear()
			return None
		else:
			score -= 2
		stack.clear()
	
	stack.clear()
	score = score #- lengthPenalty*len(organism)
	return score

def decode(organism):
	### Takes a list of integers and returns a word
	word = ''
	for letter in organism:
		word = word + string.uppercase[letter]
	return word

def encode(word):
	### Takes a string and returns a list of indices
	organism = []
	for i in word:
		organism.append(string.uppercase.index(i))
	return organism
		
def getParamFitness(organism,params,setTest=None):
	### Determines fitness of organism based on paramaters
	
	score = 0
	penalty = 0
	## Set test: Whether the organism is in a given set
	try:
		if setTest:
			decoded = decode(organism)
			if decoded.lower() in setTest:
				score += 50
			else:
				score -= 5
	except IndexError:
		return None 

	## Length scoring 
	length = len(organism)
	penalty += abs(length-params[0])
	
	## Individual gene set testing
	i = 0
	geneScore = 0
	while i < length and i < params[0]:
		letter = decode([organism[i]])
		if letter in params[i+1]:
			if letter == params[i+1][0]:
				geneScore += 2
			else:
				geneScore += 1
			'''
			if i > 1 and i < params[0]-1: # Letter in previous or next position
				if letter in params[i] or letter in params[i+2]:
					geneScore += 1
			'''
		i += 1	
	finalScore = score + geneScore - penalty

	return finalScore	
'''
def topNPercent(scoreTable,n):
	### Returns a list of individuals who score in the top n percent
	### Takes a list of form (organism,score)
	scoreTable.sort(key = lambda scoreTable: scoreTable[1])
	i = (n/100)*len(scoreTable)
	scoreTable = scoreTable[i:]
	topIndividuals = []
	for pair in scoreTable:
		#print(decode(pair[0]))
		topIndividuals.append(pair[0])
	return topIndividuals	
'''	
def roll_dice(prob):
	choice = random.randint(1,100)
	if choice in xrange(1,int(prob*100)):
		return True
	return False

def normalize(key_score_pair):
	### Return a list of 2-tuples containing a key and a score, normalized to 1
	scores = []
	newPair = []
	for pair in key_score_pair:
		scores.append(pair[1])
	maxScore = max(scores)
	for pair in key_score_pair:
		if pair[1] == 0:
			newPair.append((pair[0],pair[1])) 
		else:
			newPair.append((pair[0],pair[1]/float(maxScore)))
	
	return newPair

def breed(scoreTable,popSize,minLength,maxLength,maxValue,mutationRate,elitistSelection=False):
	if scoreTable:
		normalScores = normalize(scoreTable)
		winners = []
		while len(winners) < popSize:
			for pair in normalScores:
				if roll_dice(pair[1]):
					print(StackMachine.decode(pair[0]))
					winners.append(pair[0])	
					
		newPopulation = buildPopulation(popSize,minLength,maxLength,maxValue,mutationRate,winners) 
	else:
		newPopulation = buildPopulation(popSize,minLength,maxLength,maxValue,mutationRate)

	return newPopulation
		
'''
def breed(scoreTable,popSize,minLength,maxLength,maxValue,mutationRate,elitistSelection=False):
	### Takes a list of (organism,score) and breeds individuals based upon score.
	### Enabling eliteSelection will pass on the most succesful to the next gen.
	#print(len(scoreTable))
	## TODO: dictionaries can take an array of tuples as input
	## TODO: Make probability of breeding proportional to score
	scores = {}
	for pair in scoreTable:
		if pair[1] not in scores.keys():
			scores[pair[1]] = []
		scores[pair[1]].append(pair[0])
	scoreList = scores.keys()[::]
	scoreList.sort()

	
	newPopulation = []	
	if len(scoreList) > 0:
		winners = topNPercent(scoreTable,2)
		#for each in winners:
			#print decode(each)
		if len(winners) > 0:
	
			#print str(len(winners)) + ' individuals get to breed'
			#print 'Maximum score: ' + str(max(scoreList))
			
			print 'Champions of this generation:'
			for each in scores[max(scoreList)]:
				decoded = StackMachine.decode(each)
				#decoded = decode(each)
				print decoded 
				#print decode(each)
			
			popSize = popSize - len(winners)	
			newPopulation = buildPopulation(popSize,minLength,maxLength,maxValue,mutationRate,winners)
			#print('length: ' + str(len(newPopulation)))
			if elitistSelection:
				for individual in winners:
					if individual not in newPopulation:
						newPopulation.append(mutate(winners.pop(),maxValue,mutationRate))
						#newPopulation.append(individual)
	else:
		print "No viable organisms. Slaughtering the old population and generating a new one."
		newPopulation = buildPopulation(popSize,minLength,maxLength,maxValue,mutationRate)

	return newPopulation
'''
def generateTestValues():
	number = random.randint(0,1000)
	even = True if number % 2 == 0 else False
	return (number,even)
	
	
def __main__(stackMode=False):
	## Uncomment this next line to interactively test the stack.
	#StackMachine.stackTest()
	if stackMode:		
		stack = StackMachine.Stack()

	## Defining some parameters
	maxGenerations = 5		# Maximum number of generations to evaluate
	maxLength = 4			# Maximum number of genes for each organism
	minLength = 4			# Minimum number of genes for each organism
	if stackMode:
		maxValue = stack.instructionSetLength-1+10	# Highest possible value for each gene
	else:
		maxValue = 25
	initPopSize = 100		# Desired population size for first generation
	popSize = 1000			# Desired population size for each generation
	mutationRate = 1		# Probability of any single gene mutating.
	# TODO: Adjust the mutation rate as the population starts to stagnate
	elitistSelection = True		# Enabling this sends the best individuals to next gen
	
	qaTable = [			# Array of 2-tuples containing desired initial and end values
		(2,5),
		(3,6),
		(4,7),
		(5,8),
		(6,9),
		(7,10),
		(8,11)]

	## Parameters
	params = [6, # Length of the word
		['D'], # Likely first letter
		['L','I'], # Likely second letter
		['S','R','Z'], # Likely third letter
		['Q','P','A'], 
		['U','C','L','A'], # Likely fourth letter
		['T','S','L','A']	# Likely fifth letter
		]
	if not stackMode:		
		dictionary = []
		newFile = open('words.txt','r')
		for line in newFile:
			#print(line)
			if len(line) >= minLength and len(line) <= maxLength:
				dictionary.append(line.strip().lower())
		newFile.close()	
		

	### Generate the initial population.
	print "Generating the inital population..."
	population = buildPopulation(initPopSize,minLength,maxLength,maxValue,mutationRate)
	generations = 0
	while True:
		### Evaluate the population for fitness.
		print "Generation " + str(generations) + " of " + str(maxGenerations) 
		survivors = [] # list of tuples of form: (organism,score)
		for organism in population:
			if stackMode:
				score = getFitness(organism,qaTable,stack)
			#print "Organism: " + str(StackMachine.decode(organism)) + ' ' + str(score)
			else:
				score = getParamFitness(organism,params,dictionary)
			if (score is not None) and (score > 0):
				#print(StackMachine.decode(organism))
				survivors.append((organism,score))
	
		### Breed any surviving organisms to generate a new population.
		population = breed(survivors,popSize,minLength,maxLength,maxValue,mutationRate,elitistSelection)
		generations += 1
		if maxGenerations:
			if generations == maxGenerations:
				break
	return None
	

__main__(stackMode=True)	 		
