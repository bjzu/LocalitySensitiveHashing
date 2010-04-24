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
		"""Reduces a vector v to coordinate %s""" % n
		return v[n]
	coordinate_hash.__dict__['coord'] = n
	return coordinate_hash

##############################################################################
################### Functions For Building Signatures ########################
##############################################################################

class LSH_tools(object):
	def __init__(self):
		pass
	
	def make_lsh_ensemble(hash_creator, functions=5, d=None):
		"""Creates an ensemble of hash functions using 
		a hash_creator.  You must specify the dimension 
		of the data you're expecting, d, as well as the number_of_functions."""
		return [hash_creator(d) for i in range(functions)]

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

def lsh_nn(vector, signature_hash, original_data, distance, hash_ensemble):
	vec_sig = write_signature(vector, hash_ensemble)
	
	candidates = signature_hash.get(vec_sig, None)
	if not candidates:
		raise Error, "There are no points in this hash. %s." % vec_sig
	winning_distance, winning_prototype = -1, -1
	for c in candidates:
		d = distance(vector, original_data[c,:])
		if winning_distance == -1 or d < winning_distance:
			winning_distance = d
			winning_prototype = c
	return c

class LSH(LSH_tools):
	def __init__(self, hash_fcn = this_hash_fcn):
		self.hash_function = this_hash_fcn
		LSH_tools.__init__(self)
		self.last_ensemble = None
		self.last_indices = None
		self.last_bins = None
		self.last_data_id = None
	
	def bin_data(self, data, bands = 20, per_band = 5, flush = False):
		"""Takes data and bins them using the LSH algorithm.
		This is akin to the preprocessing step in LSH papers.
		"""
		sigsize = bands * per_bands
		n, p = data.shape
		# create the hash ensemble.
		self.last_ensemble = self.make_lsh_ensemble(self.hash_function, 
		                                           functions = sigsize, d = p)
		
		sig_matrix = self.matrix_signature(data, self.last_ensemble)
		self.last_bins = self.bin_matrix_signature(sig_matrix)
		self.last_data_id = id(data)
	
	def return_near_neighbors(self, new_data):
		"""Returns a list of lists, where the upper level indices
		mirror the new_data indices, and the lower level elements
		are indices of the near neighbors"""
		return self.lsh_nn(new_data)
	
	def is_binned(self):
		return self.last_bins != None
	
	def flush_bins(self):
		self.last_bins = None
		self.last_data_id = None
		self.last_indices = None

##############################################################################
################ Tests in need of migration to tests.py ######################
##############################################################################

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


if __name__ == "__main__":
	import numpy as np
	from time import time
	#dense_test()
	sparse_test()