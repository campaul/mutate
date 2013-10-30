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


		# Define the organism's attributes.
		self.score = 0
		self.alive = True
		self.mutant = False
		self.elite = False # May not need this functionality.
		
		# Let Darwin do his sexy work
		self.mutate(params)
		

		### Testing ###
		"""

		# Ensure that organism is of the right length	
		try:
			assert len(self) <= params['maxLength']
			assert len(self) >= params['minLength']
		except AssertionError:
			print("WARNING: Organism is of an invalid length upon spawn!" + "(" + str(len(self)) + ")")
			
		# Ensure that the organism is not a mutant if mutation rate is set to zero.
		try:
			assert self.mutant == False
		except AssertionError:
			print "Mutation rate is set to zero, but mutation is still occurring. Life apparently found a way."
			exit()
		
		# Ensure that the organism IS a mutant if mutation rate is set to 1.
		# TODO: This test fails.
		try:
			assert self.mutant == True
		except AssertionError:
			print "Mutation rate is 100%, but I haven't mutated."
			exit()
		"""
		return None

	def mutate(self,params):
	# Introduce random variation into the genome
		for gene in self:
			if roll_dice(params['mutationRate']):
				self.mutant = True
				option = random.randint(1,2)

				if option == 1:
					# Replace
					# NOTE : It almost seems like we aren't getting replacements.
					gene = random.randint(0,params['maxValue'])
					return
				# Hamming distance is undefined for strings of unequal length, so we can't do this here.
				"""
				if option == 2:
					# Remove
					self.pop(gene)
				if option == 3:
					# Insert
					self.insert(i,random.randint(0,params['maxValue']))
				"""
				if option == 2:
					# Swap
					#print("Mutation occurred! (swap)")
					first = random.randint(0,len(self)-1)
	
					second = random.randint(0,len(self)-1)
					self[first],self[second] = self[second],self[first]
					return
				else:
					print("We never should have gotten here.")
					exit()
				
	
		

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
		
		### Testing ###
		# Ensure that we are the right size.
		try:
			assert len(self) == params['popSize']
		except AssertionError:
			print "Population size is supposed to be " + str(params['popSize']) + ", but is actually " + str(len(self)) + "."
			exit()

		# Ensure that we have the right number of breeders.
		try:
			bred = 0
			bastards = 0
			for each in self:
				if each.parents:
					bred += 1
				else:
					bastards += 1
			assert bred == params['maxBreeders']
		except AssertionError:
			print "We're supposed to have " + str(params['maxBreeders']) + " organisms with parents, but we have " + str(bred) + "."
			print "Previous population had " + str(len(prevPopulation)) + " organisms."
		
				 
		return

	def get_mean_score(self):
		total_pop_score = 0
		for each in self:
			total_pop_score += each.score
		average = total_pop_score/float(len(self))
		print average
		return average
		
	def select_by_score(self):
		for organism in self:
			
			if roll_dice(organism.score > self.get_mean_score()) and organism.alive:
				
				return organism
				if params['elitistSelection']:
					if organism.score > self.get_mean_score(): # Crappy way of doing this
						self.append(organism)
						organism.elite = True
						i += 1
		return None


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

def solve(params,fitnessFunction):

	# Generate the initial population.
	population = Population(params)
	generations = 1
	
	# Keep evaluating, breeding, and spawning until (and if) params['maxGenerations'] is reached 
	while True:
		#print('Generation ' + str(generations))
		
		# Evaluate each organism in the current population for fitness
		for organism in population:
			fitnessFunction(params,organism)
		
		if params['maxGenerations']:
			if generations == params['maxGenerations']:
				#save_results(population)
				return population
		# Breed any surviving organisms to generate a new population.
		population = Population(params,population)

		# Break out of the loop if we've evaluated the maximum number of generations
		generations += 1
