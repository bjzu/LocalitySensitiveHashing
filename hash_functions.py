from random import randint, shuffle

def make_minhash(d):
	n = range(d)
	shuffle(n)
	def minhash(v):
		for i in n:
			if v[i] !=0: return i
		return 0
	return minhash

def make_coordinate_hash(d):
	"""outputs a hash function that returns only one coordinate
	of a vector or list, but selects which coordinate randomly
	in the creation of the function.
	"""
	n = randint(0,d-1)
	def coordinate_hash(v):
		return v[n]
	return coordinate_hash

def make_lsh_ensemble(hash_creator, number_of_functions=5, d=None):
	"""Creates an ensemble of hash functions using 
	a hash_creator.  You must specify the dimension 
	of the data you're expecting, d, as well as the number_of_functions."""
	return [hash_creator(d) for i in range(number_of_functions)]

def minhash_test():
	a = make_lsh_ensemble(make_minhash, number_of_functions=5, d=9)
	li = [0,1,0,0,0,0,1,0,0]
	li2 = [1,0,0,1,1,1,1,1,1]
	print [mh(li) for mh in a]
	print [mh(li2) for mh in a]
	

if __name__ == "__main__":
	minhash_test()