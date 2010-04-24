from random import randint, shuffle
from scipy.sparse import csr_matrix, dok_matrix
import numpy as np
from lsh_nn import make_minhash, make_sparse_minhash, make_coordinate_hash,\
                   make_lsh_ensemble, write_signature, write_matrix_signature,\
                   bin_signature_matrix

def minhash_test():
	a = make_lsh_ensemble(make_minhash, number_of_functions=5, d=9)
	li = [0,1,0,0,0,0,1,0,0]
	li2 = [1,0,0,1,1,1,1,1,1]
	print [mh(li) for mh in a]
	print [mh(li2) for mh in a]

def sparse_minhash_test():
	from scipy.sparse import dok_matrix, csr_matrix
	smat = dok_matrix((1,100), dtype=np.int32)
	smat[0,4] = 1
	smat[0,6] = 1
	smat[0,8] = 1
	smat[0,85] = 1
	smat[0,63] = 1
	smat = csr_matrix(smat)
	for i in range(10):
		a = make_lsh_ensemble(make_sparse_minhash, functions = 5, d=100)
		sig = write_signature(smat[0,:], a)
		print sig

def sparse_signature_test():
	pass

def sparse_matrix_write_signature_test():
	pass

def sparse_jaccard_test():
	import text_tools as tt
	data = tt.text_to_csr("otoos11.txt")
	n, p = data.shape
	# make a signature matrix.
	
	ensemble = make_lsh_ensemble(make_sparse_minhash, functions = 100, d = p)
	sig_matrix = write_matrix_signature(data, ensemble)
	
	

if __name__ == "__main__":
	#minhash_test()
	#sparse_minhash_test()
	sparse_jaccard_test()