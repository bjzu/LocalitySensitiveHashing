import unittest
from random import seed
from scipy.sparse import dok_matrix, csr_matrix

from lsh_nn import LSH
from lsh_nn import make_sparse_minhash, make_coordinate_hash

from text_tools import txt_to_csr


class TestHashingFunctions(unittest.TestCase):
	def setUp(self):
		pass
	
	
	def testMinhashRandomness(self):
		seed(1)
		a = make_sparse_minhash(3)
		b = make_sparse_minhash(3)
		v = csr_matrix([[1,0,0]])
		a_out = a(v)
		b_out = b(v)
		self.assertTrue(a_out != b_out)

	def testCoordinateRandomness(self):
		seed(1)
		a = make_coordinate_hash(3)
		b = make_coordinate_hash(3)
		v = [4,9,8]
		a_out = a(v)
		b_out = b(v)
		self.assertTrue(a_out != b_out)


class TestDataUtilities(unittest.TestCase):
	def testTextToCSR(self):
		"""Should not return an error"""
		data = txt_to_csr("test.txt")
		self.assertTrue(True)
		

class TestLSHTools(unittest.TestCase):
	pass


class TestCoreFunctionality(unittest.TestCase):
	def testFullCase(self):
		"""LSH should not return an error"""
		seed(1)
		lsh = LSH(hash_function = make_sparse_minhash)
		
		self.assertTrue(True)

	def testMinhashWithLSH(self):
		"""LSH should 'work' with make_sparse_minhash"""
		pass
	
	def testCoordinateWIthLSH(self):
		"""LSH should 'work' with make_coordinate_hash"""
		pass
		
class TestDistanceFunctions(unittest.TestCase):
	def setUp(self):
		from scipy.sparse import csr_matrix
		import numpy as np
		from distance import sparse_jaccard

	def testSparseJaccard(self):
		"""sparse_jaccard between should work with disjoint, 
		identical, and partially overlapping vectors."""
		from scipy.sparse import csr_matrix
		import numpy as np
		from distance import sparse_jaccard
		a = csr_matrix((1,3))
		a[0,2] = 1
		b = csr_matrix((1,3))
		b[0,1] = 1
		b[0,2] = 1
		c = csr_matrix((1,3))
		c[0,0] = 1
		c[0,1] = 1
		d = csr_matrix((1,3))
		d[0,0] = 1
		sp1 = sparse_jaccard(a,d)
		sp2 = sparse_jaccard(b,c)
		sp3 = sparse_jaccard(a,a)
		sp1 = sp1 == 1
		sp2 = round(sp2,2)== .67
		sp3 = sp3 == 0
		
		self.assertTrue(sp1 and sp2 and sp3)


if __name__ == "__main__":
	unittest.main()
