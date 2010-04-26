import numpy as np

from random import randint, shuffle
from scipy.sparse import dok_matrix, csr_matrix
from distance import sparse_jaccard

##############################################################################
###################### Various Hash Generating Functions #####################
##############################################################################

def make_minhash(d):
	n = range(d)
	shuffle(n)
	def minhash(v):
		for i in n:
			if v[i] != 0: return i
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
		if v.getnnz() == 0:
			return -1
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
	
	def make_lsh_ensemble(self, functions=5, d=None):
		"""Creates an ensemble of hash functions using 
		a hash_creator.  You must specify the dimension 
		of the data you're expecting, d, as well as the number_of_functions."""
		return [self._hash_function(d) for i in range(functions)]

	def write_signature(self, vector, i):
		"""Turns a raw numeric vector into a signature, which is
		simply a vector of hash functions with the original vector
		as the argument."""
		#print [ens(np.array(vector)[0]) for ens in hash_ensemble]
		return np.array([ens(vector) for ens in self.last_ensemble[i]])

	def write_signature_matrix(self, matrix, i):
		return np.matrix([self.write_signature(v, i) for v in matrix])

	def bin_signature_matrix(self, matrix):
		signature_hash = {}
		for i, v in enumerate(matrix):
			v = tuple(np.array(v)[0])
			if v not in signature_hash:
				signature_hash[v] = []
			signature_hash[v].append(i)
		return signature_hash 
	
	def near_neighbors(self, vector):
		vec_sig = self.write_signature(vector)
		
		candidates = self.last_bins.get(vec_sig, None)
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
	def __init__(self, hash_function = make_sparse_minhash, distance = None):
		self._hash_function = hash_function
		LSH_tools.__init__(self)
		self.last_ensemble = None
		self.last_indices = None
		self.last_bins = None
		self.last_data_id = None
		self.distance = None
	
	def change_hash_function(self, new_hash_function):
		self._hash_function = new_hash_function
	
	def bin_data(self, data, bands = 20, per_band = 5, 
	             flush = False, verbose = False):
		"""Takes data and bins them using the LSH algorithm.
		This is akin to the preprocessing step in LSH papers.
		"""
		sigsize = bands * per_band
		n, p = data.shape
		
		if flush:
			self.last_ensemble = None
			self.last_data_id = None
			self.last_data = None
		if self.last_ensemble == None:
			self.last_ensemble = []
		
		for i in range(bands):
			ens = self.make_lsh_ensemble(functions = per_band, d = p)
			self.last_ensemble.append(ens)
			if verbose: print "Finished creating band No. %s" % i
		
		self.last_bins = {}
		for i, ens in enumerate(self.last_ensemble):
			sig_matrix = self.write_signature_matrix(data, i)
			binset = self.bin_signature_matrix(sig_matrix)
			for k in binset:
				if k not in self.last_bins:
					v = binset[k]
					self.last_bins[k] = []
				self.last_bins[k].extend(v)
			if verbose: print "finished binning band no. %s" % i
		
		self.last_data_id = id(data)
		self.last_data = data
	
	def _query(self, new_data, query_fcn, parameter):
		"""basis for near(est) neighbors query."""
		indices = []
		for i, v in enumerate(new_data):
			query_i = query_fcn(v, parameter)
			indices.append(query_i)
		return indices
	
	def return_near_neighbors(self, new_data, r):
		"""performs near neighbors search on new_data, with similarity
		threshold r."""
		return self._query(new_data, self.near_neighbors, r)
	
	def return_nearest_neighbors(self, new_data, k):
		"""Performs nearest neighbors search on new_data, looking for the
		k nearest points to each row of new_data."""
		return self._query(new_data, self.nearest_neighbors, k)
	
	def near_neighbors(self, vector, r):
		vec_sig = self.write_signature(vector)
		candidates = self.last_bin.get(vec_sig, None)
		if not candidates:
			raise Error, "There are no points in this hash. %s." % vec_sig
		near_neighbors = []
		for c in candidates:
			d = distance(vector, self.last_data[c,:])
			if d < r:
				near_neighbors.append[d]
		return near_neighbors
	
	def nearest_neighbors(self, vector, k):
		"""Unfinished."""
		vec_sig = self.write_signature(vector)
		candidates = signature_hash.get(vec_sig, None)
		if not candidates:
			raise Error, "There are no points in this hash. %s." % vec_sig
		dists = {}
		for c in candidates:
			d = distance(vector, self.last_data[c,:])
			dists[c] = d
		dists = [(v,k) for k,v in dists.items()]
		dists.sort()
		dists = [k for v,k in dists][0:k]
		return dists
	
	##########################################################################
	#################### misc. lsh utility functions. ########################
	##########################################################################
	
	def is_binned(self):
		return self.last_bins != None
	
	def flush_bins(self):
		self.last_bins = None
		self.last_data_id = None
		self.last_indices = None
	
	def single_bins_frequency(self):
		singles = 0
		total = 0
		for bin in self.last_bins:
			if len(self.last_bins[bin]) == 1:
				singles += 1
			total += 1
		return singles / float(total)
	
	def check_for_duplicates(self):
		dup_dict = {}
		for bin in self.last_bins:
			vs = self.last_bins[bin]
			for v in vs:
				if v not in dup_dict: dup_dict[v] = []
			dup_dict[v].append(bin)
		return dup_dict



if __name__ == "__main__":
	#dense_test()
	sparse_test()
