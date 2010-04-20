def jaccard(x0, x1):
	#return 1 - len(x0 & x1) / float(len(x0 | x1))
	return 1 - sum(x0 * x1) / float(sum(x0 | x1))