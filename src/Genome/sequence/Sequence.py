from sequence.EulerPath import EulerPath

class Sequence():
    def __init__(self, filename, skip=False, kmers=None):
        '''
        Expecting either a file where each row is a kmer or a list of kmers directly.
        Can skip the first row that tells you the 'k' value
        '''
        if kmers is not None:
            self.rows = kmers
        else:
            with open(filename) as infile:
                if skip:
                    next(infile)
                self.rows = [row.rstrip() for row in infile]

    def debruijn(self):
        '''
        Process the list of kmers saved by the Constructor into a dictionary adj
        index is the kmer prefix
        value is a list of every suffix associated with the prefix
        This is a DeBruijn network
        '''
        adj = {}
        for kmer in self.rows:
            skey = kmer[:-1]
            sval = kmer[1:]

            if skey in adj:
                adj[skey].append(sval)
            else:
                adj[skey] = [sval]
        return adj

    def eulerPath(self, adj):
        euler = EulerPath(adj)
        return euler.eulerPath()

    def assemble(self, circuit):
        '''
        Turn the Euler path through the DeBruijn network into a sequence
        by merging the overlapping edges
        '''
        seq = circuit[0]
        for elt in circuit[1:]:
            seq = seq + elt[-1]
        return seq
