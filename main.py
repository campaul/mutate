import random

import stack as StackMachine
import mutate

stack = StackMachine.Stack()

def get_fitness(params,organism):
	# Determine the fitness of a single organism	
	score = 0
	timePenalty = params['execTimePenalty']
	attempted = 0
	right = 0
	timings = []
	#print('Evaluating ' + StackMachine.decode(organism))
	for i in xrange(params['execIterations']):
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
		timings.append(stack.execTime)	
		stack.clear()
	
	stack.clear()
	if timings:
		meanTiming = sum(timings)/float(len(timings))
		score = (right/float(attempted)) - timePenalty*meanTiming
	else:
		score = (right/float(attempted))
	return score 

def decode(encMap,organism):
	# Converts an organism's genes to their human-readable representation

	decoded = ''
	for i in organism:
		try:
			decoded = decoded + encMap[int(i)] + ' '
		except IndexError:
			decoded = decoded + str(i-len(encMap)) + ' '
	return decoded


def generate_test():
	# This enerates the test values for determining fitness.
	number = random.randint(0,1000)
	even = True if number % 2 == 0 else False
	return (number,even)
	
def __main__():
	params = {
		'maxGenerations':50,
		'maxLength':4,
		'minLength':4,
		'maxValue':27,
		'initPopSize':100,
		'popSize':250,
		'mutationRate':.015,
		'elitistSelection':False,
		'normalizeScores':False,
		'maxBreeders':50,
		'execTimePenalty':10000,
		'execIterations':20,
		'elitePercentile':.95
		}
	
	encMap = ['+',
		'-',
		'/',
		'*',
		'DROP',
		'SWAP',
		'DUP',
		'STO',
		'RCL',
		'<',
		'>',
		'==',
		'OR',
		'AND',
		'MOD',
		'IFTE',
		'TRUE',
		'FALSE']

	results = mutate.solve(params,get_fitness)

	for each in sorted(results, key = lambda result: result[1]):
		print(decode(encMap,each[0]) + ' : ' + str(each[1]))
	
__main__()
