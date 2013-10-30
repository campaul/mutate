import mutate
import random
import stack as StackMachine
import yaml

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
			organism.kill()
		else:
			right -= 1
			stack.clear()
		timings.append(stack.execTime)	
		stack.clear()
	
	stack.clear()
	if timings:
		meanTiming = sum(timings)/float(len(timings))
		score = (right/float(attempted)) - timePenalty*meanTiming
	else:
		score = (right/float(attempted))
	organism.score = score
	return  

					
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
	# This generates the test values for determining fitness.
	number = random.randint(0,1000)
	even = True if number % 2 == 0 else False
	return (number,even)
	
def __main__():
	params = yaml.load(open('config.yaml'))
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
	
	for organism in sorted(results, key = lambda result:result.score):
		if organism.score > 0:
			print(decode(encMap,organism) + ' : ' + str(organism.score))
	
__main__()
