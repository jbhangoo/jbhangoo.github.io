from alignment.Fasta import Fasta
from alignment.SubseqIndex import GappedIndex

t = 'TGTCCAGTTAGGATCTACTGGACCGAAGTATTGAGGACACACGTATATGTATGGGTGAGAGTAGCCACAGTGACGTAGACAT'
t = 'ABCDEFGHI'
f = Fasta()
t = f.readFasta("data/chr1.fasta")
ind = GappedIndex(t, 10, 4)
p = 'GGCGCGGTGGCTCACGCCTGTAAT'
print(len(p))
print(ind.query(p))