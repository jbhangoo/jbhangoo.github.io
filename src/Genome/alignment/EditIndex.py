"""
Use pigeonhole principle to match pattern p to text t
1. Find k based on average number of errors to expect
2. Index k-mers of t to speed up pattern searches
3. Divide p into k-sized pieces
4. Find all exact matches of one of the pieces. k is chosen to make this possible
5. Validate entire p at the positions where the exact piece matches were found

"""
import math
from alignment.KmerIndex import KmerIndex
from alignment.Levenshtein import Levenshtein

class EditIndex():
    def __init__(self, t, k):
        '''
        Establishes the text and kmer size
        '''
        self.k = k
        self.t = t
        self.ki = KmerIndex(t, k)

    def nearMatch(self, p, errs=2):
        '''
        Search text for each k-mer in p, allowing edits (errors)
        Return all positions of all p's kmers that match t
        '''
        ed = Levenshtein()
        k = self.k
        numPieces = int(math.ceil(len(p)/k))
        offsets = set()
        for i in range(numPieces):
            piece = p[k*i:k*(i+1)]
            matches = self.ki.query(piece)
            for m in matches:
                # Validate entire p against candidate substring of t
                start = m - k * i
                if ed.distance(p, self.t[start:start+len(p)]) <= errs:
                    offsets.add(start)
        return offsets
