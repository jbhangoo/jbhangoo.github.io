from sequence.Contig import Contig
from sequence.EulerPath import EulerPath

def branchesFromAdj():
    contig = Contig("data/contig.txt")
    adj = contig.readAdj()
    branches = contig.getAllBranches(adj)

    with open("bra.out","w") as bf:                
        for path in branches:
            bf.write(" -> ".join([v.name for v in path]))
            bf.write('\n')

def branchesFromKmers():
    contig = Contig("data/contig.txt")
    adj = contig.readKmers()
    euler = EulerPath(adj)
    branches = contig.getAllBranches(euler.graph)
    seqs = contig.assembleContigs(branches)

    with open("branch.out","w") as bf:
        for seq in seqs:
            bf.writelines(seq+' ')


branchesFromKmers()