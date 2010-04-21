
from scipy import weave
from scipy.weave import converters

def sparse_jaccard(x0, x1):
	#return 1 - len(x0 & x1) / float(len(x0 | x1))
	return 1 - len(set(x0.indices) and set(x1.indices)) / float((x0 + x1).getnnz())

def quick_jaccard(x0, x1):
	l = x0.shape[0]
	#weave.inline('printf("%f\\n", *x0);', ['x0'])
	code = """
	double num, denom;
	num = 0.0;
	denom = 0.0;
	for (int i = 0; i < l; ++i) {
		if (x0[i] == x1[i]) {
			num += 1.0;
		}
		printf(x0[i]);
		if (x0[i] > 0.0 || x1[i] > 0.0) {
			denom += 1.0;
		}
		return_val = num / denom;
	}
	"""
	distance = weave.inline(code, 
							['l', 'x0', 'x1'],
							type_converters=converters.blitz,
							compiler = 'gcc')
	return 1 - distance

if __name__ == "__main__":
	from scipy.sparse import csr_matrix
	import numpy as np
	from time import time
	times = []
	for i in range(50000):
		x0 = csr_matrix([0,1,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
		x1 = csr_matrix([0,1,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
		t = time()
		#quick_jaccard(x0, x1)
		sparse_jaccard(x0, x1)
		t1 = time()
		times.append(t1- t)
		
	print sum(times) / float(len(times))
	print sum(times)
	# from scipy.sparse import dok_matrix
	# 	
	# 	a = dok_matrix([[0,0,1,1,0,0],[1,0,0,1,0,0]], dtype=np.int32)
	# 	print a[1,:].toarray()[0]
	# 	print quick_jaccard(a[0,:].toarray()[0], a[1,:].toarray()[0])
	# 	print quick_jaccard(a[0,:].toarray()[0], a[1,:].toarray()[0])