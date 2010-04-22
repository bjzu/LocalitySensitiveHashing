"""
Hash Functions.  
Currently have minhash and coordinate hash implemented.
"""

from random import randint, shuffle
from scipy.sparse import csr_matrix, dok_matrix
import numpy as np
from lsh_nn import make_minhash, make_sparse_minhash, make_coordinate_hash,
                   make_lsh_ensemble, write_signature, write_signature_matrix,
                   bin_signature_matrix


#
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

def sparse_matrix_write_signature():
	pass

if __name__ == "__main__":
	#minhash_test()
	sparse_minhash_test()