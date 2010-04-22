from random import randint, shuffle
from scipy.sparse import dok_matrix, csr_matrix
from distance import sparse_jaccard
from hash_functions import *

##############################################################################
###################### Various Hash Generating Functions #####################
##############################################################################

def make_minhash(d):
	n = range(d)
	shuffle(n)
	def minhash(v):
		for i in n:
			if v[i] !=0: return i
		return 0
	return minhash

def make_sparse_minhash(d):
	"""Returns a function sparse_minhash: sparse matrix -> integer
	which is created somewhat randomly."""
	n = range(d)
	shuffle(n)
	n = tuple(n)
	mh = dict((i,j) for i, j in enumerate(n))
	def sparse_minhash(v):
		"""Returns the minimum index for the permutation.
		Expects v to be a sparse 1xn matrix."""
		return  min(j for j in [mh[i] for i in v.indices])
	
	return sparse_minhash

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

##############################################################################
################### Functions For Building Signatures ########################
##############################################################################

def write_signature(vector, hash_ensemble):
	"""Turns a raw numeric vector into a signature, which is
	simply a vector of hash functions with the original vector
	as the argument."""
	#print [ens(np.array(vector)[0]) for ens in hash_ensemble]
	return np.array([ens(vector) for ens in hash_ensemble])

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

def minhash_test():
	a = make_lsh_ensemble(make_minhash, number_of_functions=5, d=9)
	li = [0,1,0,0,0,0,1,0,0]
	li2 = [1,0,0,1,1,1,1,1,1]
	print [mh(li) for mh in a]
	print [mh(li2) for mh in a]

def sparse_minhash_test():
	smat = dok_matrix((1,100), dtype=np.int32)
	smat[0,4] = 1
	smat[0,6] = 1
	smat[0,8] = 1
	smat[0,85] = 1
	smat[0,63] = 1
	smat = csr_matrix(smat)
	for i in range(10):
		a = make_lsh_ensemble(make_sparse_minhash, number_of_functions=5, d=100)
		sig = write_signature(smat[0,:], a)
		print sig


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
	f = open("otoos11.txt", "r")
	every_line = []
	for line in f:
		line = line.strip().lower()
		every_line.append(line)
	every_line = ''.join(every_line)
	every_line = every_line.split('.')
	n = len(every_line)
	dictionary = set()
	for l in every_line:
		words = l.split()
		dictionary.update(set(words))
	d = len(dictionary)
	dictionary = dict((word, i) for i, word in enumerate(list(dictionary)))
	data = dok_matrix((n,d), dtype=np.int32)
	for j, l in enumerate(every_line):
		words = l.split()
		for word in words:
			data[j, dictionary[word]] = 1
	data = csr_matrix(data)
	
	###################################################################
	# find average Jaccard distance between completely random points. #
	###################################################################
	

if __name__ == "__main__":
	import numpy as np
	from time import time
	#dense_test()
	sparse_test()
	