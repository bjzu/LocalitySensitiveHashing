from random import randint
from scipy.sparse import dok_matrix, csr_matrix

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

def write_signature(vector, hash_ensemble):
	"""Turns a raw numeric vector into a signature, which is
	simply a vector of hash functions with the original vector
	as the argument."""
	#print [ens(np.array(vector)[0]) for ens in hash_ensemble]
	return np.array([ens(np.array(vector)[0]) for ens in hash_ensemble])

def write_matrix_signature(matrix, hash_ensemble):
	return np.matrix([write_signature(v, hash_ensemble) for v in matrix])

def bin_signature_matrix(matrix):
	signature_hash = {}
	for i, v in enumerate(matrix):
		v = tuple(np.array(v)[0])
		if v not in signature_hash:
			signature_hash[v] = []
		signature_hash[v].append(i)
	return signature_hash

def lsh_nn(vector, signature_hash, original_data, distance, hash_ensemble):
	vec_sig = write_signature(vector, hash_ensemble)
	
	candidates = signature_hash.get(vec_sig, None)
	if not candidates:
		raise Error, "Sadness.  There are no points in this hash. %s." % vec_sig
	winning_distance, winning_prototype = -1, -1
	for c in candidates:
		d = distance(vector, original_data[c,:])
		if winning_distance == -1 or d < winning_distance:
			winning_distance = d
			winning_prototype = c
	return c

def dense_test():
	dimensions = 1000
	coord_ensemble = make_lsh_ensemble(make_coordinate_hash, 
						number_of_functions=10, d=dimensions)
	
	# Generate some random data.
	d = np.matrix(np.random.randint(0,2, (100000, dimensions)))
	
	# Build a matrix of signatures.
	print "Let's build a matrix of signatures."
	t = time()
	s = write_matrix_signature(d, coord_ensemble)
	print "%s for a %s matrix" % ((time() - t), s.shape)
	t = time()
	print "Making the signature hash."
	a = bin_signature_matrix(s)
	print "%s seconds for a hash of size %s" % (time() - t, len(a))
	
	bins = {}
	for i in a:
		l = len(a[i])
		if l not in bins: bins[l] = 0
		bins[l] += 1
	bins = [(v,k) for k,v in bins.items()]
	bins.sort(reverse=True)
	for v, k in bins:
		print "%-5s %s" % (v,k)

def sparse_test():
	dimensions = 100000
	data_points = 100000
	a = dok_matrix((dimensions, data_points))
	print a.shape
	

if __name__ == "__main__":
	import numpy as np
	from time import time
	#dense_test()
	sparse_test()
	