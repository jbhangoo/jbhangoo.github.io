"""
Use pigeonhole principle to find matches of a pattern p in text t, allowing for errors
This works only if there is less than 1 error per k positions, overall

Given k, index every k-mer in t
Split p into k-sized pieces (final piece may be less than k in size)
Pigeonhole principle states that one of the pieces must match t exactly.

"""
import math
from alignment.KmerIndex import KmerIndex

class Pigeon():
    def __init__(self, t, k):
        '''
        Establishes the text and kmer size
        '''
        self.k = k
        self.t = t
        self.ki = KmerIndex(t, k)

    def hamming(self, pat, genome):
        bad = 0
        for j in range(len(pat)):  # loop over characters
            if genome[j] != pat[j]:  # compare characters
                bad += 1
        return bad

    def pieceMatch(self, p, errs=3):
        '''
        Return positions of kmers of p that match text
        '''
        k = self.k
        numPieces = int(math.ceil(len(p)/k))
        offsets = set()
        for i in range(numPieces):
            piece = p[k*i:k*(i+1)]
            matches = self.ki.query(piece)
            for m in matches:
                # Validate entire p against candidate substring of t
                start = m - k * i
                if self.hamming(p, self.t[start:start+len(p)]) < errs:
                    offsets.add(start)
        return offsets
