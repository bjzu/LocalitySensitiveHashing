import random
import unittest
import lsh

class TestNewObject(unittest.TestCase):
	
	def setUp(self):
		# set up the data structure we will train on.
		# should have a self.lsh object.
		pass
	
	def test_vanilla_instantiation(self):
		try:
			l = lsh.LSH()
		except:
			self.fail()
		self.assertTrue(True)
	
	def test_too_few_bands(self):
		try:
			lsh.LSH(bands=-10)
		except:
			self.assert_(True)
		self.fail("bands was set to -10, should have failed.")
		
	
	def test_too_few_per_band(self):
		try:
			lsh.LSH(per_band=-10)
		except:
			self.assert_(True)
		self.fail("per_band was set to -10, should have failed.")
	
	def test_noninteger_bands(self):
		try:
			lsh.LSH(bands="foo")
		except:
			self.assert_(True)
		self.fail("tried to set bands to a noninteger value.")
	
	def test_noninteger_per_band(self):
		try:
			lsh.LSH(per_band="foo")
		except:
			self.assert_(True)
		self.fail("tried to set per_band to a noninteger value.")

class TestWithCachedData(unittest.TestCase):
	pass



if __name__ == "__main__":
	unittest.main()