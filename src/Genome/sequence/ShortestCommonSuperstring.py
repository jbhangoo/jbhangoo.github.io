import itertools

class ShortestCommonSuperstring:
    def overlap(self, a, b, min_length=3):
        """ Return length of longest suffix of 'a' matching
            a prefix of 'b' that is at least 'min_length'
            characters long.  If no such overlap exists,
            return 0. """
        start = 0  # start all the way at the left
        while True:
            start = a.find(b[:min_length], start)  # look for b's suffx in a
            if start == -1:  # no more occurrences to right
                return 0
            # found occurrence; check for full suffix/prefix match
            if b.startswith(a[start:]):
                return len(a)-start
            start += 1  # move just past previous match

    def scs(self, ss):
        """ Returns shortest common superstring of given
            strings, which must be the same length """
        shortest_sup = None
        for ssperm in itertools.permutations(ss):
            sup = ssperm[0]  # superstring starts as first string
            for i in range(len(ss)-1):
                # overlap adjacent strings A and B in the permutation
                olen = self.overlap(ssperm[i], ssperm[i+1], min_length=1)
                # add non-overlapping portion of B to superstring
                sup += ssperm[i+1][olen:]
            if shortest_sup is None or len(sup) < len(shortest_sup):
                shortest_sup = sup  # found shorter superstring
        return shortest_sup  # return shortest

    def allscs(self, ss):
        """ Returns shortest common superstring of given
            strings, which must be the same length """
        shortest_sup = None
        sups = set()
        for ssperm in itertools.permutations(ss):
            sup = ssperm[0]  # superstring starts as first string
            for i in range(len(ss)-1):
                # overlap adjacent strings A and B in the permutation
                olen = self.overlap(ssperm[i], ssperm[i+1], min_length=1)
                # add non-overlapping portion of B to superstring
                sup += ssperm[i+1][olen:]
            sups.add(sup)
            if shortest_sup is None or len(sup) < shortest_sup:
                shortest_sup = len(sup)  # found shorter superstring
        return [s for s in sups if len(s)==shortest_sup]  # return shortest

scs = ShortestCommonSuperstring()
print(scs.allscs(["ABC", "BCA", "CAB"]))
got = scs.allscs(['GAT', 'TAG', 'TCG', 'TGC', 'AAT', 'ATA'])
got.sort()
answer = ['AATAGATCGTGC',
 'AATAGATGCTCG',
 'AATAGTCGATGC',
 'AATCGATAGTGC',
 'AATGCTCGATAG',
 'TCGAATAGATGC',
 'TCGATAGAATGC',
 'TCGATGCAATAG',
 'TGCAATAGATCG',
 'TGCAATCGATAG']
print (got)
print (answer)
['AATAGATCGTGC', 'AATAGATGCTCG', 'AATAGTCGATGC', 'AATCGATAGTGC', 'AATGCTCGATAG', 'TCGAATAGATGC', 'TCGATAGAATGC', 'TCGATGCAATAG', 'TGCAATAGATCG', 'TGCAATCGATAG']
['AATAGATCGTGC', 'AATAGATGCTCG', 'AATAGTCGATGC', 'AATCGATAGTGC', 'AATGCTCGATAG', 'TCGAATAGATGC', 'TCGATAGAATGC', 'TCGATGCAATAG', 'TGCAATAGATCG', 'TGCAATCGATAG']

reads = ["CCT", "CTT", "TGC", "TGG", "GAT", "ATT"]
superstr = scs.allscs(reads)
print(superstr)