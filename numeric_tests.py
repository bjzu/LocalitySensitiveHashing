import lsh_nn as lsh

from text_tools import txt_to_csr

def sparse_minhash_test():
    nn = lsh.LSH(hash_function = lsh.make_sparse_minhash)
    # grab some data.
    data = txt_to_csr("dd.txt")
    print "Loaded data (%s by %s) ..." % data.shape
    nn.bin_data(data, bands = 20, per_band = 5)
    print "Binned data ..."
    nearest = nn.return_nearest_neighbors(data, 1)
    print nearest

if __name__ == "__main__":
    sparse_minhash_test()
    
