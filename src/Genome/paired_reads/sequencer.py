import sys

def getrows(filename):
    with open(filename) as infile:
        rows = [x.strip() for x in infile]
    return rows

def pathToSeq(pathfile):
    #rows = sys.stdin.readlines()
    rows = getrows(pathfile)
    return stringFromKmers(rows)

def stringFromKmers(kmers):
    seq = kmers[0]
    for kmer in kmers[1:]:
        seq = seq + kmer[-1]
    return seq

"""
    StringSpelledByGappedPatterns(GappedPatterns, k, d)
        FirstPatterns ← the sequence of initial k-mers from GappedPatterns
        SecondPatterns ← the sequence of terminal k-mers from GappedPatterns
        PrefixString ← StringSpelledByGappedPatterns(FirstPatterns, k)
        SuffixString ← StringSpelledByGappedPatterns(SecondPatterns, k)
        for i = k + d + 1 to |PrefixString|
            if the i-th symbol in PrefixString does not equal the (i - k - d)-th symbol in SuffixString
                return "there is no string spelled by the gapped patterns"
        return PrefixString concatenated with the last k + d symbols of SuffixString
"""
def stringFromGappedReads(patterns, k, d):
    firsts = ['' for p in patterns]
    seconds = ['' for p in patterns]
    for i in range(len(patterns)):
        pieces = patterns[i].split('|')
        firsts[i] = pieces[0].strip()
        seconds[i] = pieces[1].strip()
    prefix = stringFromKmers(firsts)
    suffix = stringFromKmers(seconds)
    for i in range(k+d+1, len(prefix)):
        if prefix[i] != suffix[i-k-d]:
            return ''
    return prefix + suffix[-k-d:]

k = 50
d = 200
preads = getrows("paired_reads/preads.txt")
seq =  (stringFromGappedReads(preads, k, d))
with open("genome.out","w") as outf:
    outf.write(seq)

print (seq)

import sys
sys.exit(0)
seq = pathToSeq("path.txt")

with open("genome.out","w") as outf:
    outf.write(seq)
print (seq)
