#!/usr/bin/python

import random
import math
import string

import stack as StackMachine


def spawn(minLength,maxLength,maxValue,parents=None,mutationRate=.001):
	# Produce a new organism provided the number of genes and optional parents.
	# An organism is a list of integers, where each integer is a stack instruction.
	
	# If a list of parents is provided:	
	baby = []
	length = random.randint(minLength,maxLength)
	if parents:
		for i in xrange(length):
			parent = random.choice(parents)
			try:
				baby.append(parent[i])
			except IndexError:
				return mutate(baby,maxValue,mutationRate)
		return mutate(baby,maxValue,mutationRate)

	# If no parents are provided, randomly generate a list of integers.
	for index in range(length):
		baby.append(random.randint(0,maxValue))
	return baby


def mutate(organism,maxValue,mutationRate):
	# Introduce random variation into the genome
	i = 0
	while i < len(organism) :
		option = random.randint(1,4)

		if roll_dice(mutationRate):
			if option == 1:
				# Replace
				organism[i] = random.randint(0,maxValue)
			if option == 2:
				# Remove
				organism.pop(i)
			if option == 3:
				# Insert
				organism.insert(i,random.randint(0,maxValue))
			if option == 4:
				# Swap)
				first = random.randint(0,len(organism)-1)
				second = random.randint(0,len(organism)-1)
				organism[first],organism[second] = organism[second],organism[first]
			
		i += 1
	return organism


def build_population(popSize,minLength,maxLength,maxValue,mutationRate,prevPopulation=None):
	# Build a new population, optionally taking in existing organisms to be bred
	# Args: population size, length of the genome, highest possible value for gene, population

	newPopulation = []
	if prevPopulation:
		for organism in prevPopulation:
			mom = random.choice(prevPopulation)
			dad = random.choice(prevPopulation)
			newPopulation.append(spawn(minLength,maxLength,maxValue,[mom,dad],mutationRate))
		while len(newPopulation) < popSize:
			newBaby = spawn(minLength,maxLength,maxValue)
			newPopulation.append(newBaby)
		return newPopulation
	else:
		for index in range(popSize):
			newBaby = spawn(minLength,maxLength,maxValue)
			newPopulation.append(newBaby)
	return newPopulation


def get_fitness(organism,stack):
	# Determine the fitness of a single organism

	score = 0
	timePenalty = 10000
	attempted = 0
	right = 0
	timings = []
	for i in xrange(100):
		test = generate_test()
		stack.append(test[0])	
		result = stack.evaluate(organism)
		attempted += 1
		
		if result is test[1]:
			right += 1
		
		elif result is None:
			stack.clear()
			return None
		else:
			stack.clear()
			continue
		timings.append(stack.execTime)	
		stack.clear()
	
	stack.clear()
	if len(timings):
		meanTiming = sum(timings)/float(len(timings))
		score = (right/float(attempted)) - timePenalty*meanTiming
	else:
		score = (right/float(attempted))
	return score

def decode(organism):
	# Takes the genes and returns their human-readable representation.

	return StackMachine.decode(organism)		


def roll_dice(prob):
	choice = random.randint(1,100)
	if choice in xrange(1,int(prob*100)):
		return True
	return False


def normalize(key_score_pair):
	# Return a list of 2-tuples containing a key and a score, normalized to 1

	scores = []
	newPair = []
	for pair in key_score_pair:
		scores.append(pair[1])
	try:
		maxScore = max(scores)
	except ValueError:
		return None
	for pair in key_score_pair:
		if pair[1] == 0:
			newPair.append((pair[0],pair[1])) 
		else:
			newPair.append((pair[0],pair[1]/float(maxScore)))
	
	return newPair

def breed(scoreTable,popSize,minLength,maxLength,maxValue,mutationRate,elitistSelection=False,normalizeScores=True):
	# Selectively breed the population, with their probability of breeding being proportional to their scores

	if scoreTable:
		if normalizeScores:
			normalScores = normalize(scoreTable)
		else:
			normalScores = scoreTable
		winners = []

		while normalScores:
			pair = normalScores.pop()
			if roll_dice(pair[1]):
				winners.append(pair[0])
		newPopulation = build_population(popSize,minLength,maxLength,maxValue,mutationRate,winners) 

		if elitistSelection:
			elites = []
			for pair in normalScores:
				if pair[1] > .95:
					elites.append(pair[0])
			for each in elites:
				# TODO: Use something other than pop
				newPopulation.pop()
				newPopulation.append(each)
	else:
		newPopulation = build_population(popSize,minLength,maxLength,maxValue,mutationRate)

	return newPopulation
		

def generate_test():
	# This enerates the test values for determining fitness.
	number = random.randint(0,1000)
	even = True if number % 2 == 0 else False
	return (number,even)
	
	
def save_results(survivors):
	# Decode each organism's genome into a human-readable format and save them all
	# to a text file.

	fileHandle = open('output.txt','w')
	formatted = ''
	for survivor in survivors:
		formatted = formatted + decode(survivor[0]) + ' : ' + str(survivor[1]) + '\n'
	fileHandle.write(formatted)
	fileHandle.close()

def __main__():
	# Uncomment this next line to interactively test the stack.
	# StackMachine.stack_test()
	
	# Initialize the stack
	stack = StackMachine.Stack()

	# Defining some parameters
	maxGenerations = None		# Maximum number of generations to evaluate
	maxLength = 7			# Maximum number of genes for each organism
	minLength = 3			# Minimum number of genes for each organism
	maxValue = stack.instructionSetLength+9	# Highest possible value for each gene
	initPopSize = 100		# Desired population size for first generation
	popSize = 500			# Desired population size for each generation
	mutationRate = 	.1		# Probability of any single gene mutating.
	elitistSelection = True		# Enabling this sends the best individuals to next gen	
	normalizeScores = False		# Enabling this will normalize scores between 0 and 1

	
	# Generate the initial population.
	population = build_population(initPopSize,minLength,maxLength,maxValue,mutationRate)
	generations = 1

	# Keep evaluating, breeding, and spawning until (and if) maxGenerations is reached 
	while True:

		print "Generation " + str(generations) + " of " + str(maxGenerations) 
		survivors = [] # list of tuples of form: (organism,score)
		
		# Evaluate each organism in the current population for fitness
		for organism in population:
			score = get_fitness(organism,stack)
			if (score is not None) and (score > 0):
				if score > .80:
					print(decode(organism))
				survivors.append((organism,score))

		# Breed any surviving organisms to generate a new population.
		population = breed(survivors,popSize,minLength,maxLength,maxValue,mutationRate,elitistSelection,normalizeScores)

		# Break out of the loop if we've evaluated the maximum number of generations
		generations += 1
		if maxGenerations:
			if generations == maxGenerations+1:
				break	
	
	# Once out of the loop, save the last generation to a text file
	save_results(survivors)
		
	return None
	

__main__()
	
