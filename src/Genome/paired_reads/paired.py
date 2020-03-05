# put your python code here
import sys

class Node():
  def __init__(self, name):
    self.name = name
    self.ins = []
    self.outs = []

class EulerPath():
    def __init__(self, adj):
        self.graph = {}
        for src,destlist in adj.items():
            srcnode = self.getNode(src)
            for dest in destlist:
                destnode = self.getNode(dest)
                srcnode.outs.append(destnode)
                destnode.ins.append(srcnode)

    def findFirstNode(self):
        for _,curnode in self.graph.items():
            if len(curnode.outs) > len(curnode.ins):
                return curnode
        return curnode

    def getNode(self, name):
        if name in self.graph:
            node = self.graph[name]
        else:
            node = Node(name)
            self.graph[name] = node
        return node

    def eulerPath(self):
        activenodes = []
        circuit = []
        curnode = self.findFirstNode()
        while True:
            while len(curnode.outs) > 0:
                activenodes.append(curnode)
                curnode = curnode.outs.pop()

            circuit.append(curnode.name)
            if len(activenodes) == 1:
                circuit.append(activenodes.pop().name)
                break
            elif len(activenodes) == 0:
                break
            curnode = activenodes.pop()
        return circuit[::-1]

class PairedReads():
    def __init__(self, lines):
        first = lines[0].split()
        self.k = int(first[0].strip())
        self.d = int(first[1].strip())
        rows = lines[1:]
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

rows = [row.rstrip() for row in sys.stdin.readlines()]
paired = PairedReads(rows)
adj = paired.debruijn()
epath = paired.eulerPath(adj)
seq = paired.assemble(epath)

print(seq)
