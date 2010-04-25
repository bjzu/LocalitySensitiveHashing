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
		

class TestCoreFunctionality(unittest.TestCase):
	def testFullCase(self):
		"""LSH should not return an error"""
		seed(1)
		lsh = LSH(hash_function = make_sparse_minhash)
		# get data.
		self.assertTrue(True)

	def testMinhashWithLSH(self):
		"""LSH should 'work' with make_sparse_minhash"""
		pass
	
	def testCoordinateWIthLSH(self):
		"""LSH should 'work' with make_coordinate_hash"""
		pass
		

if __name__ == "__main__":
	unittest.main()
