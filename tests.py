"""
Hash Functions.  
Currently have minhash and coordinate hash implemented.
"""

from random import randint, shuffle
from scipy.sparse import csr_matrix, dok_matrix
import numpy as np



if __name__ == "__main__":
	#minhash_test()
	sparse_minhash_test()