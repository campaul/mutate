#!/usr/bin/python

import random

class Organism(list):
	def __init__(self,params,parents=None):

		# Construct the organism's gene sequence.
		length = random.randint(params['minLength'],params['maxLength'])
		self.parents = parents
		
		if parents is None or (parents[0] is None or parents[1] is None):
			# Randomly generate a list of integers
			for i in xrange(length):
				self.append(random.randint(0,params['maxValue']))
		else:
			# Select genes from both parents, randomly alternating from which
			parentGenes = zip(parents[0],parents[1])
			for each in parentGenes:
				i = random.randint(0,1)
				self.append(each[i])

		# TODO: mutation

		# Define the organism's attributes.
		self.score = 0
		self.alive = True
		return None

	def mutate(self,params):
	# Introduce random variation into the genome
	
		for gene in self:
			option = random.randint(1,4)

			if roll_dice(params['mutationRate']):
				if option == 1:
					# Replace
					gene = random.randint(0,params['maxValue'])
				if option == 2:
					# Remove
					self.pop(gene)
				if option == 3:
					# Insert
					self.insert(i,random.randint(0,params['maxValue']))
				if option == 4:
					# Swap)
					first = random.randint(0,len(self)-1)

					second = random.randint(0,len(self)-1)
					self[first],self[second] = self[second],self[first]
				
	
		

	def kill(self):	
		self.alive = False
		
class Population(list):
	def __init__(self,params,prevPopulation=[]):
		
		if len(prevPopulation) > 2:
			# TODO : Implement elitist selection.
				
			i = 0
			while i < params['maxBreeders']:
				# TODO : Is there a more Pythonic way to do this?
				mom = prevPopulation.select_by_score()
				dad = prevPopulation.select_by_score()
				self.append(Organism(params,[mom,dad]))
				i += 1
		while len(self) < params['popSize']:
			self.append(Organism(params))
				 
		return 
		
	def select_by_score(self):
		for organism in self:
			if roll_dice(organism.score) and organism.alive:
				return organism
		return None

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
'''
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
	
def save_results(population):
	# Decode each organism's genome into a human-readable format and save them all
	# to a text file.

	fileHandle = open('output.txt','w')
	formatted = ''
	for organism in population:
		formatted = formatted + decode(organism[0]) + ' : ' + str(organism[1]) + '\n'
	fileHandle.write(formatted)
	fileHandle.close()
'''
def solve(params,fitnessFunction):

	# Generate the initial population.
	population = Population(params)
	generations = 1
	
	# Keep evaluating, breeding, and spawning until (and if) params['maxGenerations'] is reached 
	while True:
		print('Generation ' + str(generations))
		
		# Evaluate each organism in the current population for fitness
		for organism in population:
			fitnessFunction(params,organism)
		if generations == params['maxGenerations']:
			#save_results(population)
			return population
		# Breed any surviving organisms to generate a new population.
		population = Population(params,population)

		# Break out of the loop if we've evaluated the maximum number of generations
		generations += 1
