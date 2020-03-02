"""
A DeBruijn graph is a directed multi-graph that turns read into k-mers
and stores as an edge from the prefix to the suffix, both of length k-1

Allow for errors
"""
from src.Genome import Levenshtein

class DNode():
    def __init__(self, name, errors):
        self.names = set()
        self.errors = errors
        self.addName(name)

    def add(self, name):
        self.names.add(name)

    def isSimilar(self, name):
        for curname in self.names:
            if Levenshtein.distance(name, curname) < self.errors:
                return True
        return False

    def isSuffix(self, name):
        '''
        Does the given sequence qualify as a suffix of the current node
        The overlapping parts must be within the pre-defined edit distance
        :param name:
        :return:
        '''
        prefix = name[:-1]
        for curname in self.names:
            if Levenshtein.distance(prefix, curname[1:]) < self.errors:
                return True
        return False

class DeBuijn():
    def __init__(self, fastqFile, k):
        '''
        Store all reads from the FASTQ file
        Then build an index from each kmer of each read back to the full original read
        '''
        self.k = k
        self.edges = {}
        with open(fastqFile) as fh:
            self.reads = []
            while True:
                fh.readline()  # skip name line
                read = fh.readline().rstrip()  # read base sequence
                slen = len(read)
                if slen == 0:
                    break
                self.reads.append(read)
                fh.readline()  # skip placeholder line
                fh.readline().rstrip() # skip base quality line

                for i in range(slen-k+1):
                    kmer = read[i:i+k]
                    prefix = kmer[:-1]
                    suffix = kmer[1:]

                    if prefix in self.edges:
                        self.edges[prefix].append(suffix)
                    else:
                        self.edges[prefix] = [suffix]
