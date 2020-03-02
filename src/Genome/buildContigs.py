from src.Genome.assembly.Overlap import Overlap
from src.Genome.assembly.AdjGraph import AdjGraph

overlaps = Overlap("data/practice.fq", k=2)
overlap_list = overlaps.getOverlaps(errors=0)
graph = AdjGraph(overlap_list)
paths = graph.getAllBranches()
contigs = graph.assembleContigs(paths)
for contig in contigs:
    print(contig)