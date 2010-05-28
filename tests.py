import random
import unittest
import lsh
import os
import cPickle
import glob

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
		else:
			self.fail("bands was set to -10, should have failed.")
	
	def test_too_few_per_band(self):
		try:
			lsh.LSH(per_band=-10)
		except:
			self.assert_(True)
		else:
			self.fail("per_band was set to -10, should have failed.")
	
	def test_noninteger_bands(self):
		try:
			lsh.LSH(bands="foo")
		except:
			self.assert_(True)
		else:
			self.fail("tried to set bands to a noninteger value.")
	
	def test_noninteger_per_band(self):
		try:
			lsh.LSH(per_band="foo")
		except:
			self.assert_(True)
		else:
			self.fail("tried to set per_band to a noninteger value.")

class TestWithCachedData(unittest.TestCase):
	"""
	This set of tests is meant to test the functionality of the 
	various cache-related functions.  Need to test:
	
	- If there is actually a usable cache available
	- If there is not actually a usable cache available
	- List all the trained files.
	- Check to see if the model is trained.
	- Delete cached data.
	
	"""
	
	def retrieve_test_data(self, filename):
		f = open("test_data/%s.data" % filename, "r")
		data = cPickle.loads(f.read())
		f.close()
		return data
	
	def dump_data(self, assignment_name):
		if os.path.exists("temp/"):
			files = glob.glob("temp/%s*" % assignment_name)
			for f in files:
				os.remove(f)
	
	def create_trained_model(self, assignment_name, dims):
		l = lsh.LSH(assignment_name=assignment_name)
		data = self.retrieve_test_data(assignment_name)
		l.bin_data(data, dims=21)
		return l
	
	def test_data_is_not_there(self):
		l = lsh.LSH(assignment_name="data_not_there")
		self.assertFalse(l.is_cached(), \
			"LSH tells us there's data here, but there shouldn't be.")
	
	def test_data_is_there(self):
		# first, remove existing data for this, retrain,
		# and then check to see if the data is cached.
		self.dump_data("small_correct")
		l = self.create_trained_model("small_correct", 21)
		
		is_cached = os.path.exists("temp/small_correct-lsh.pickle")
		
		self.assertTrue(l.is_cached() == is_cached, \
		 			"Data is supposed to be cached, but isn't.")
	
	def test_cache_is_usable(self):
		self.dump_data("small_correct")
		l = self.create_trained_model("small_correct", 21)
		l2 = lsh.LSH(assignment_name="small_correct")
		try:
			l2.load_cached_data()
			self.assertTrue(True)
		except:
			self.assertFalse(False)
	
	def test_cache_is_not_usable(self):
		# Need to find a better Exception to raise.
		l = lsh.LSH(assignment_name="broken_cache")
		self.assertRaises(KeyError, l.load_cached_data)
	
	def test_model_is_trained(self):
		self.dump_data("small_correct")
		l = self.create_trained_model("small_correct", 21)
		self.assertTrue(l.is_trained(), \
			"model declared it wasn't trained even though it was.")

class TestWithoutCachedData(unittest.TestCase):
	pass


if __name__ == "__main__":
	unittest.main()