import sys

def getKmersStdin():
    rows = sys.stdin.readlines()
    kmers = [row.rstrip() for row in rows]
    return kmers

def getKmers(filename):
    with open(filename) as infile:
        lines = infile.readlines()
        kmers = [row.rstrip() for row in lines[1:]]
    return kmers

def debruijn(kmerfile):
    adj = {}
    kmers = getKmers(kmerfile)
    for kmer in kmers:
        skey = kmer[:-1]
        sval = kmer[1:]

        if skey in adj:
            adj[skey].append(sval)
        else:
            adj[skey] = [sval]
    return adj

adj = debruijn("kmers.txt")
for skey,sval in adj.items():
    slist = ','.join(sval)
    print(skey+" -> "+slist)

