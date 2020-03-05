from alignment.Fasta import Fasta
from alignment.BoyerMoore import BoyerMoore
from alignment.Pigeon import Pigeon

from datetime import datetime

t = 'TGTGGTAAGCCCCGAGCAGCTAGCGTAGGAGCGTTGGCTTATTCGCGTAGGCCTGAGATCGCGTAACA'

p = 'TACCTGCGTAGGATAGCTGCCTGC' # Middle 8 chars are in t
p = 'TATAGCTGCCGGATAGTAGGAGCG' # Last 8 chars are in t
p = 'AGCGTAGGAGCGCTGCGTGAAACT' # First 8 chars are in t
p = 'TAGCGTAGGAGCGTTGGCTTATTC' # This is an exact match
p = 'TAGCGTCGGAGCGTTGGCTTAGTC' # This is a match with 2 errors
k = 8

p = 'GGCGCGGTGGCTCACGCCTGTAATCCCAGCACTTTGGGAGGCCGAGG'
p = 'GGCGCGGTGGCTCACGCCTGTAAT'
ff = Fasta()
#genome = ff.readFastq("alignment/human_ERR.fastq")
genome = ff.readFasta("data/chr1.fasta")
t0 = datetime.now()
m = ff.naive(p, genome)
t1 = datetime.now()
print((t1-t0).total_seconds())
print('Naive', m)
bm = BoyerMoore(p)
m = bm.align(genome)
t2 = datetime.now()
print((t2-t1).total_seconds())
print('Boyer Moore', m)
pp = Pigeon(genome, k)
t3 = datetime.now()
print((t3-t2).total_seconds())
print (pp.kmerMatch(p))