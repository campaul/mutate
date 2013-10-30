import random
import mutate


def get_hamming_distance(string1,string2):
	try:
		assert len(string1) == len(string2)
	
	except AssertionError:
		print(string2)
		print "String is " + str(len(string2)) + " characters long, unequal to the required length. Exiting."
		exit()

	distance = sum(ch1 != ch2 for ch1, ch2 in zip(string1,string2))
	return distance

def get_fitness(params, organism):
	# In this example, the organism's fitness is defined by the Hamming distance from our given string.
	#the_string = "THE FOOL DOTH THINK HE IS WISE BUT THE WISE DOTH KNOW HE IS A FOOL"
	the_string = "GARRETT"
	
	hdistance = get_hamming_distance(the_string,decode(organism))
	
	if hdistance == 0:
		organism.score = 1
		print("Solution found.")
		return
	else:
		
		organism.score = ((params['maxLength']-hdistance)/float(params['maxLength']) * 100)
		if organism.score == 0:
			organism.kill()
			return
		else:
			return
	
					
def decode(organism):
	
	encMap = ['A',
		'B',
		'C',
		'D',
		'D',
		'F',
		'G',
		'H',
		'I',
		'J',
		'K',
		'L',
		'M',
		'N',
		'O',
		'P',
		'Q',
		'R',
		'S',
		'T',
		'U',
		'V',
		'W',
		'X',
		'Y',
		'Z',
		' ']



	decoded = ''
	for i in organism:
		try:
			decoded = decoded + encMap[int(i)]
		except IndexError:
			print str(i) + " is out of the encoder map's range. Exiting."
	return decoded


def __main__():
	params = {
		'maxGenerations':None,
		'maxLength':7, # Change back to 66
		'minLength':7,
		'maxValue':26,
		'initPopSize':250,
		'popSize':250,
		'mutationRate':.5,
		'elitistSelection':False, # NOT READY! Hardcoded instead of done by normalization.
		'normalizeScores':False,
		'maxBreeders':250,
		'execTimePenalty':10000,
		'execIterations':8,
		'elitePercentile':.95
		}
	
	encMap = ['A',
		'B',
		'C',
		'D',
		'D',
		'F',
		'G',
		'H',
		'I',
		'J',
		'K',
		'L',
		'M',
		'N',
		'O',
		'P',
		'Q',
		'R',
		'S',
		'T',
		'U',
		'V',
		'W',
		'X',
		'Y',
		'Z']

	results = mutate.solve(params,get_fitness)
	
	for organism in sorted(results, key = lambda result:result.score):
		if organism.score > 0:
			print(decode(encMap,organism) + ' : ' + str(organism.score))
	
__main__()
