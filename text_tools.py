from scipy.sparse import dok_matrix, csr_matrix
import numpy as np

def file_to_matrix(filename, outfile):
	"""Converts raw text file to a matrix, saved in outfile as a COO mat."""
	f = open(filename, "r")
	every_line = []
	# get every line out.
	for line in f:
		line = line.strip().lower()
		every_line.append(line)
	every_line = ''.join(every_line)
	
	# Split into sentences.
	every_line = every_line.split('.')
	
	
	# get number of sentences.
	n = len(every_line)
	dictionary = set()
	wc = {}
	for l in every_line:
		words = l.split()
		dictionary.update(set(words))
		for word in words:
			wc[word] = wc.get(word, 0) + 1
	wc = [(v,k) for k, v in wc.items()]
	wc.sort(reverse=True)
	wc = dict((w,i) for i, (v,w) in enumerate(wc))
	# get number of words.
	d = len(wc)
	
	of = file(outfile, 'w')
	total_spots = 0
	for i, l in enumerate(every_line):
		words = l.split()
		words = set(words)
		for word in words:
			of.write("%s,%s\n" % (i, wc[word]))
			total_spots += 1
	of.close()
	
	print n, d, total_spots, total_spots / float(n*d)

def txt_to_csr(filename):
	f = open(filename, "r")
	every_line = []
	# get every line out.
	for line in f:
		line = line.strip().lower()
		every_line.append(line)
	every_line = ''.join(every_line)
	
	# Split into sentences.
	every_line = every_line.split('.')
	
	# get number of sentences.
	n = len(every_line)
	dictionary = set()
	wc = {}
	for l in every_line:
		words = l.strip().split()
		dictionary.update(set(words))
		for word in words:
			wc[word] = wc.get(word, 0) + 1
	wc = [(v,k) for k, v in wc.items()]
	wc.sort(reverse=True)
	wc = dict((w,i) for i, (v,w) in enumerate(wc))
	# get number of words.
	d = len(wc)
	
	data = dok_matrix((n,d), dtype=np.int32)
	for j, l in enumerate(every_line):
		words = l.split()
		for word in words:
			data[j, wc[word]] = 1
	data = csr_matrix(data)
	return data 
