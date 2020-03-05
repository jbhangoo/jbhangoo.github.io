from src.Genome.alignment.Fasta import Fasta
from src.Genome.sequence.PairedReads import PairedReads
from src.Genome.sequence.Sequence import Sequence
from src.Genome.assembly.Overlap import Overlap
from src.Genome.sequence.EulerPath import EulerPath
from src.Genome.assembly.OverlappingReads import OverlappingReads

def sequence(filename, filetype):
    ff = Fasta()
    if filetype == 'fasta':
        reads = ff.readFasta(filename)
    elif filetype == 'fastq':
        reads,qual = ff.readFastq(filename)
    else:
        return
    seq = Sequence('', kmers=reads)
    adj = seq.debruijn()
    euler = EulerPath(adj)

    contig = Overlap(sequencer=seq)
    branches = contig.getBranches(euler.graph)

    seqs = contig.assembleContigs(branches)
    return seqs

def pairedSequence(filename, filetype):
    paired = PairedReads(filename)
    adj = paired.debruijn()
    euler = EulerPath(adj)

    contig = Overlap()
    branches = contig.getBranches(euler.graph)

    seq = paired.assemble(branches)
    return seq

#seq = pairedSequence("data/paired_reads.txt", "text")
#seq = sequence("data/ads1_week4_reads.fq", "fastq")

k = 8
#ff = OverlapGraph("data/ERR266411_1.for_asm.fastq", k)
#ff = OverlapGraph("data/practice.fq", k)
ff = OverlappingReads("data/ads1_week4_reads.fq", k)
adj = ff.getOverlaps()
tot = 0
for seq,nexts in adj.items():
    tot += len(nexts)

print ("Edges")
print(tot)
print ("  ")
print (len(adj.keys()))
print (" reads have overlaps out of a total of ")
print (len(ff.reads))
print ("  ")

graph = ff.buildGraph(adj)
print("Graph nodes:")
print(len(graph))
print ("  ")

paths = ff.allPaths(graph)

totlen = 0
for path in paths:
    totlen += len(path)
print ("Avg path len")
print (totlen/len(paths))
print (" out of ")
print (len(paths))
print (" paths")

contig = Overlap()
paths = contig.getBranches(graph)

with open("seq.out","w") as outf:
    outf.write(''.join(seq))
print(seq)