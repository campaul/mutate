#!/usr/bin/python

import random

def spawn(params,parents=None):
	# Produce a new organism provided the number of genes and optional parents.
	# An organism is a list of integers, where each integer is a stack instruction.
	
	# If a list of parents is provided:	
	baby = []
	length = random.randint(params['minLength'],params['maxLength'])
	if parents:
		for i in xrange(length):
			parent = random.choice(parents)
			try:
				baby.append(parent[i])
			except IndexError:
				return mutate(params,baby)
		return mutate(params,baby)

	# If no parents are provided, randomly generate a list of integers.
	for index in range(length):
		baby.append(random.randint(0,params['maxValue']))
	return baby


def mutate(params,organism):
	# Introduce random variation into the genome
	i = 0
	while i < len(organism) :
		option = random.randint(1,4)

		if roll_dice(params['mutationRate']):
			if option == 1:
				# Replace
				organism[i] = random.randint(0,params['maxValue'])
			if option == 2:
				# Remove
				organism.pop(i)
			if option == 3:
				# Insert
				organism.insert(i,random.randint(0,params['maxValue']))
			if option == 4:
				# Swap)
				first = random.randint(0,len(organism)-1)

				second = random.randint(0,len(organism)-1)
				organism[first],organism[second] = organism[second],organism[first]
			
		i += 1
	return organism


def build_population(params,prevPopulation=None):
	# Build a new population, optionally taking in existing organisms to be bred
	# Args: population size, length of the genome, highest possible value for gene, population

	newPopulation = []
	if prevPopulation:
		for organism in prevPopulation:
			mom = random.choice(prevPopulation)
			dad = random.choice(prevPopulation)
			newPopulation.append(spawn(params,[mom,dad]))
		while len(newPopulation) < params['popSize']:
			newBaby = spawn(params)
			newPopulation.append(newBaby)
		return newPopulation
	else:
		for index in range(params['popSize']):
			newBaby = spawn(params)
			newPopulation.append(newBaby)
	return newPopulation



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

def breed(params,scoreTable):
	# Selectively breed the population, with their probability of breeding being proportional to their scores
	if params['maxBreeders'] is None:
		params['maxBreeders'] = params['popSize']
	if scoreTable:
		if params['normalizeScores']:
			normalScores = normalize(scoreTable)
		else:
			normalScores = scoreTable
		winners = []
		if params['elitistSelection']:
			elites = []
			for pair in normalScores:
				if pair[1] > params['elitePercentile']:
					elites.append(pair[0])
					normalScores.remove(pair)
		while len(winners) < params['maxBreeders']:
			#air = normalScores.pop()
			for pair in normalScores:
				if roll_dice(pair[1]):
					winners.append(pair[0])
		newPopulation = build_population(params,winners) 

		if params['elitistSelection']:	
			for each in elites:
				# TODO: Use something other than pop
				newPopulation.pop()
				newPopulation.append(each)
	else:
		newPopulation = build_population(params)

	return newPopulation
		

	
	
def save_results(survivors):
	# Decode each organism's genome into a human-readable format and save them all
	# to a text file.

	fileHandle = open('output.txt','w')
	formatted = ''
	for survivor in survivors:
		formatted = formatted + decode(survivor[0]) + ' : ' + str(survivor[1]) + '\n'
	fileHandle.write(formatted)
	fileHandle.close()

def solve(params,fitnessFunction):

	# Generate the initial population.
	population = build_population(params)
	generations = 1
	
	# Keep evaluating, breeding, and spawning until (and if) params['maxGenerations'] is reached 
	while True:
		print('Generation ' + str(generations))
		survivors = [] # list of tuples of form: (organism,score)
		
		# Evaluate each organism in the current population for fitness
		for organism in population:
			score = fitnessFunction(params,organism)
			if (score is not None) and (score > 0):
				survivors.append((organism,score))
		print(str(len(survivors)) + ' survivors')	
		if params['maxGenerations']:
			if generations == params['maxGenerations']+1:
				return survivors	

		# Breed any surviving organisms to generate a new population.
		population = breed(params,survivors)

		# Break out of the loop if we've evaluated the maximum number of generations
		generations += 1
