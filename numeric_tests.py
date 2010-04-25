import lsh_nn as lsh

from text_tools import txt_to_csr

def sparse_minhash_test():
	nn = lsh.LSH(hash_function = lsh.make_sparse_minhash)
	# grab some data.
	data = txt_to_csr("otoos11.txt")
	print "Loaded data (%s by %s) ..." % data.shape
	nn.bin_data(data, bands = 60, per_band = 5)
	print "Binned data ..."
	from pprint import PrettyPrinter
	p = PrettyPrinter(indent=4)
	p.pprint(nn.last_bins)

if __name__ == "__main__":
    sparse_minhash_test()
    
