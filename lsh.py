#!/usr/bin
from time import time
import multiprocessing
from random import shuffle
import cPickle
import os
from distance import jaccard
import datetime

class LSH(object):
	def __init__(self, bands = 100, per_band = 5, assignment_name = "lsh_example"):
		if type(bands) != int:
			raise TypeError, "bands must be an integer."
		if type(per_band) != int:
			raise TypeError, "per_band must be an integer."
		if bands < 1:
			raise ValueError, "bands must be greater than 0."
		if per_band < 1:
			raise ValueError, "per_band must be greater than 0."
		self.assignment_name = assignment_name
		self.bands = bands
		self.per_band = per_band
		self.dims = None
		self.__trained = False
		self.__loaded_files = set()
		self.bins = {}
		self.verbose = False
	
	def __nice_time(self, t):
		print "Done.  Took %s seconds." % (round(time() - t, 2)) 
	
	def __h_ens(self, d):
		n = range(d)
		shuffle(n)
		n = tuple(n)
		mh = dict((i,j) for i, j in enumerate(n))
		return mh
	
	def __bin_data_queue(self, data, q):
		"""The workers created in self.bin_data() get this function as
		an argument.  It pops indices off of the shared queue and
		processes them, one by one, then saves batches of signatures
		in a flat file under a temp/ folder.  The original self.bin_data()
		function takes care to combine these afterward."""
		which_process = "%s-%s" % (multiprocessing.current_process().name,\
				datetime.datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
				)
		sigs = []
		if self.verbose: print "Started %s" % (which_process)
		while not q.empty():
			ind = q.get()
			pt = data[ind]
			sig = [min(j for j in [mh[i] for i in pt]) \
					for mh in self.ensemble]
			for b in range(self.bands):
				minhash = tuple(sig[(b*self.per_band):((b+1)*self.per_band)])
				sigs.append([b, ind, minhash])
		bins = open("temp/%s-bins.pickle" % (which_process), 'w')
		cPickle.dump(sigs, bins)
		bins.close()
		if self.verbose: print "Finished %s" % which_process
	
	def load_cached_data(self):
		"""Loads cached data associated with assignment_name, 
		if any exists.
		
		"""
		t = time()
		if self.verbose:
			print "Loading cached data."
		self.__load_object_specific_data()
		self.__combine_bins()
		self.__trained = True
		if self.verbose:
			self.__nice_time(t)
	
	def trained_files(self):
		"""Returns a set of trained file paths."""
		return self.__loaded_files
	
	def is_cached(self):
		"""Returns True if there is a cache for this assignment_name,
		and False otherwise."""
		lsh_info = os.path.abspath("temp/%s-lsh.pickle" \
						% self.assignment_name)
		return os.path.exists(lsh_info)
	
	def is_trained(self):
		"""Returns True if the current object has been trained."""
		return self.__trained
	
	def load_cached_or_train(self, data):
		t = time()
		if self.is_cached():
			self.load_cached_data()
		else:
			self.bin_data(data)
	
	def delete_all_data(self):
		pass
	
	def bin_data(self, data, dims = None):
		"""Trains the LSH object on the available data, storing the
		results in bins.
		
		It is not really wise to touch object.bins - stick to finding 
		near neighbors with object.near_neighbors(query_index, query_vector)
		instead.
		"""
		
		# the directory temp/ is for storing the serialized processed data.
		# I hope it is not too intrusive - if you have a better solution,
		# drop me a line.
		
		temp_path = os.path.abspath("temp/")
		
		if not os.path.exists(temp_path):
			os.mkdir(temp_path)
		
		if self.verbose:
			print "Mapping new data.  Might take a few minutes."
		
		bands = self.bands
		per_band = self.per_band
		
		############################################################
		# Create a new ensemble if the cached data was not loaded. #
		############################################################
		
		if not self.__trained:
			if dims == None:
				raise ValueError, \
					"you must specify the dims on this untrained model."
			self.dims = dims
			self.ensemble = [self.__h_ens(self.dims) \
					for i in range(bands*per_band)]
		
		#################################
		# Set up a multiprocessing job. #
		#################################
		
		queue = multiprocessing.Queue()
		for k in data:
			queue.put(k)
		
		pool = multiprocessing.Pool()
		t = time()
		ens = self.ensemble
		
		results = [multiprocessing.Process(target=self.__bin_data_queue, \
			args=(data, queue), \
			name = "%s-worker_%s" % (self.assignment_name, str(i))) \
			for i in range(multiprocessing.cpu_count())]         
		for i in results:
			i.start()
		for i in results:
			i.join()
		if self.verbose: 
			print "Done mapping data.  Took %s minutes." \
						% (round((time() - t)/60.0, 2))
		
		self.__save_object_specific_data()
		
		##############################################
		# Combine the new results with the old ones. #
		##############################################
		
		if self.verbose: print "Reducing data."
		t = time()
		
		self.__combine_bins()
		
		if self.verbose: print "Finished Reducing the data. Took %s seconds"\
												% (round(time() - t, 2))
		self.__trained = True
	
	def __save_object_specific_data(self):
		"""Used to cache parameters and the ensemble
		after we've finished binning data."""
		misc_values = {}
		misc_values['assignment_name'] = self.assignment_name
		misc_values['bands'] = self.bands
		misc_values['per_band'] = self.per_band
		misc_values['ensemble'] = self.ensemble
		misc_values['dims'] = self.dims
		
		f = open("temp/%s-lsh.pickle" % self.assignment_name, "w")
		cPickle.dump(misc_values, f)
	
	def __load_object_specific_data(self):
		"""Used if we've already cached an lsh machine.  This function
		reloads some serialized parameters."""
		f = open("temp/%s-lsh.pickle" % self.assignment_name, "r")
		misc_values = cPickle.loads(f.read())
		self.assignment_name = misc_values['assignment_name']
		self.bands = misc_values['bands']
		self.per_band = misc_values['per_band']
		self.ensemble = misc_values['ensemble']
		self.dims = misc_values['dims']

	def __combine_bins(self):
		"""Combines all the bins from the multiple processes."""
		bins = []
		
		######################################################
		# Check to see which data bins we haven't added yet. #
		######################################################
		os.chdir(os.path.abspath("temp/"))
		files = os.listdir(".")
		eligible_bins = [f for f in files \
			if self.assignment_name in f and "bins" in f]
		for bin_file in eligible_bins:
			if bin_file not in self.__loaded_files:
				f = open(bin_file, "r")
				bins.append(cPickle.loads(f.read()))
				self.__loaded_files.add(bin_file)
		
		##########################
		# Combine the new data here. #
		##########################
		for bin in bins:
			for (b, index, minhash) in bin:
				#print (b, index, minhash)
				if b not in self.bins: self.bins[b] = {}
				if minhash not in self.bins[b]: self.bins[b][minhash] = set()
				self.bins[b][minhash].add(index)
		
		os.chdir(os.path.abspath("../"))
	
	def near_neighbors(self, ind, query):
		"""Returns a set of near neighbors associated with ind, 
		whose data is a set of integers representing item_ids,
		called query."""
		if self.__trained:
			sig = [min(j for j in [mh[i] for i in query]) \
					for mh in self.ensemble]
			nn = set()
			for b in range(self.bands):
				minhash = tuple(sig[(b*self.per_band):((b+1)*self.per_band)])
				if minhash in self.bins[b]:
					nn.update(self.bins[b][minhash])
			nn = nn - set([ind])
			return nn
		else:
			raise Exception, "Object not trained yet."