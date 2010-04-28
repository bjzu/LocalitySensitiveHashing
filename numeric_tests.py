import lsh_nn as lsh
import numpy as np
from scipy.sparse import csr_matrix

from text_tools import txt_to_csr
from mysql_connection import table_to_csr

def sparse_minhash_test():
	nn = lsh.LSH(hash_function = lsh.make_sparse_minhash)
	# grab some data.
	data, sentence_dict = txt_to_csr("otoos11.txt")
	#data, kid_index, link_index = table_to_csr()
	print "Loaded data (%s by %s) ..." % data.shape
	nn.bin_data(data, bands = 20, per_band = 5, verbose = True)
	print "Binned data ..."
	
	print nn.single_bins_frequency()
	
	from pprint import PrettyPrinter
	p = PrettyPrinter(indent=4)
	#len(b for b in nn.last_bins.keys() if nn.last_bins[b])
	#p.pprint(nn.last_bins)
	#p.pprint(nn.check_for_duplicates())
	#check_sentences(nn, sentence_dict)
	#check_points(nn, data)

def check_sentences(lsh, sd):
	for sig in lsh.last_bins:
		values = lsh.last_bins[sig]
		if len(values) > 2:
			for i in values:
				print sd[i]
			print "*"*80, "\n"

def check_points(lsh, orig_data):
	for sig in lsh.last_bins:
		values = lsh.last_bins[sig]
		if len(values) > 2:
			for i in values:
				print orig_data[i,:].indices
			print "/"*80, "\n"

if __name__ == "__main__":
    sparse_minhash_test()
    
