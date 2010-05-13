def jaccard(x0, x1):
	"""x0 and x1 are sets."""
	return len(x0 & x1) / float(len(x0 | x1))
