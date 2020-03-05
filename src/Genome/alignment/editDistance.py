from alignment.Fasta import Fasta
from alignment.EditIndex import EditIndex

seqlen = 16
k = 8

ff = Fasta()
genome = ff.readFasta("data/chr1.fasta")
ed = EditIndex(genome, k)

p = 'GATTTACCAGATTGAG'
m = ed.nearMatch(p, 2)
print(p)
for d in m:
    print(genome[d:d+seqlen])
print('\n')

ed = EditIndex(genome, 4)
p = 'GCTGATCGATCGTACG'
m = ed.nearMatch(p, 3)
print(p+':')
for d in m:
    print(genome[d:d+seqlen])
print('\n')
