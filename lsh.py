#!/usr/bin -i
from time import time
import multiprocessing
from random import shuffle
import cPickle
import os
from distance import jaccard





class LSH(object):
	def __init__(self, dims, bands = 100, per_band = 5, assignment_name = "lsh_example"):
		self.assignment_name = assignment_name
		#self.func = fcn
		self.bands = bands
		self.per_band = per_band
		self.dims = dims
	
	def __h_ens(self, d):
		n = range(d)
		shuffle(n)
		n = tuple(n)
		mh = dict((i,j) for i, j in enumerate(n))
		return mh
	
	def bin_data_queue(self, data, q, ens, bands, per_band):
		"""Given the nature of the multiprocessing module"""
		which_process = multiprocessing.current_process().name
		sigs = []
		print "Started %s" % (which_process)
		while not q.empty():
			ind = q.get()
			pt = data[ind]
			sig = [min(j for j in [mh[i] for i in pt]) \
					for mh in ens]
			#siglist = []
			for b in range(bands):
				minhash = tuple(sig[(b*per_band):((b+1)*per_band)])
				#siglist.append(minhash)
				#if minhash not in d[b]: d[b][minhash] = mngr.list()
				#d[b][minhash].append(ind)
				sigs.append([b, ind, minhash])
				#d[b].append(mngr.list([ind, minhash]))
		bins = open("temp/%s-bins.pickle" % (which_process), 'w')
		cPickle.dump(sigs, bins)
		bins.close()
		print "Finished %s" % which_process
	
	def bin_data(self, data, verbose = True, new_bins = True):
		"""Trains the LSH object on the available data, storing the
		results in object.bins.  It is not really wise to touch
		object.bins - stick with finding near neighbors with
		object.near_neighbors(query_pt, query_vector) instead.
		"""
		if not os.path.exists("temp/"):
			# need to create temp/
			pass
		
		remap_data = False
		
		for i in range(multiprocessing.cpu_count()):
			if not os.path.exists("temp/%s-worker_%s-bins.pickle" % (self.assignment_name, str(i))):
				remap_data = True
		if not os.path.exists("temp/%s-lsh.pickle" % self.assignment_name):
			remap_data = True
		if remap_data:
			
			if verbose: print "Mapping data from scratch.  This will probably take a few minutes."
			
			bands = self.bands
			per_band = self.per_band
		
			if new_bins:
				self.ensemble = [self.__h_ens(self.dims) \
						for i in range(bands*per_band)]
			
			queue = multiprocessing.Queue()
			for k in data:
				queue.put(k)
			
			pool = multiprocessing.Pool()
			t = time()
			ens = self.ensemble
			
			#results = pool.apply_async(bin_data_queue, (data, queue, self.ensemble, self.bands))
			results = [multiprocessing.Process(target=self.bin_data_queue, \
				args=(data, queue, ens, bands, per_band), \
				name = "%s-worker_%s" % (self.assignment_name, str(i))) \
				for i in range(multiprocessing.cpu_count())]         
			for i in results:
				i.start()
			for i in results:
				i.join()
			print "Done mapping data.  Took %s minutes." % (round((time() - t)/60.0, 2))
			
			misc_values = {}
			misc_values['bands'] = self.bands
			misc_values['per_band'] = self.per_band
			misc_values['ensemble'] = self.ensemble
			
			f = open("temp/%s-lsh.pickle" % self.assignment_name, "w")
			cPickle.dump(misc_values, f)
			
		else:
			if verbose: print "Data already mapped.  Loading saved ensemble."
			f = open("temp/%s-lsh.pickle" % self.assignment_name, "r")
			misc_values = cPickle.loads(f.read())
			self.bands = misc_values['bands']
			self.per_band = misc_values['per_band']
			self.ensemble = misc_values['ensemble']
		
		if verbose: print "Reducing data."
		t = time()
		# open all the available bin dumps, reduce the data.
		bins = []
		for i in range(multiprocessing.cpu_count()):
			#lsh_example-worker_0
			f = open("temp/%s-worker_%s-bins.pickle" % (self.assignment_name, str(i)), "r")
			#f = open("temp/%s-bins-worker_%s.pickle" % (self.assignment_name, str(i)), "r")
			bins.append(cPickle.loads(f.read()))
		
		self.bins = {}
		
		for bin in bins:
			for (b, index, minhash) in bin:
				#print (b, index, minhash)
				if b not in self.bins: self.bins[b] = {}
				if minhash not in self.bins[b]: self.bins[b][minhash] = set()
				self.bins[b][minhash].add(index)
		
		if verbose: print "Finished Reducing the data. Took %s seconds" % (round(time() - t, 2))
	
	
	def near_neighbors(self, ind, query):
		sig = [min(j for j in [mh[i] for i in query]) \
				for mh in self.ensemble]
		nn = set()
		for b in range(self.bands):
			minhash = tuple(sig[(b*self.per_band):((b+1)*self.per_band)])
			if minhash in self.bins[b]:
				nn.update(self.bins[b][minhash])
		nn = nn - set([ind])
		return nn
	

	