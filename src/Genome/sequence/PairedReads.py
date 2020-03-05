from sequence.EulerPath import EulerPath

class PairedReads():
    def __init__(self, filename):
        with open(filename) as infile:
            first = infile.readline().split()
            self.k = int(first[0].strip())
            self.d = int(first[1].strip())
            rows = infile.readlines()
            self.rows = [row.strip() for row in rows]

    def debruijn(self):
        '''
        Process the list of kmers saved by the Constructor into a dictionary adj
        index is the kmer prefix
        value is a list of every suffix associated with the prefix
        This is a DeBruijn network
        '''
        adj = {}
        for pair in self.rows:
            kmers = pair.split('|')
            first = kmers[0].strip()
            second = kmers[1].strip()
            skey = (first[:-1],second[:-1])
            sval = (first[1:],second[1:])

            if skey in adj:
                adj[skey].append(sval)
            else:
                adj[skey] = [sval]
        return adj

    def eulerPath(self, adj):
        euler = EulerPath(adj)
        return euler.eulerPath()

    def assemble(self, patterns):
        firsts = ['' for p in patterns]
        seconds = ['' for p in patterns]
        for i in range(len(patterns)):
            firsts[i] = patterns[i][0]
            seconds[i] = patterns[i][1]
        prefix = self.stringFromKmers(firsts)
        suffix = self.stringFromKmers(seconds)
        k = self.k
        d = self.d
        for i in range(k+d+1, len(prefix)):
            if prefix[i] != suffix[i-k-d]:
                return ''
        return prefix + suffix[-k-d:]

    def stringFromKmers(self, kmers):
        seq = kmers[0]
        for kmer in kmers[1:]:
            seq = seq + kmer[-1]
        return seq
