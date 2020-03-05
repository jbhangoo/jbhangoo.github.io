from src.Genome.assembly.DeBruijn import DeBuijn

dbn = DeBuijn("data/ads1_week4_reads.fq", 16, 2)

dbn.eulerPath()
seq = dbn.assembleSequence()
print(seq)
