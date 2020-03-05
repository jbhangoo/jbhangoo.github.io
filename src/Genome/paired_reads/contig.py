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

class Sequence():
    def __init__(self, kmers):
        self.rows = kmers

    def debruijn(self):
        '''
        Process the list of kmers saved by the Constructor into a dictionary adj
        index is the kmer prefix
        value is a list of every suffix associated with the prefix
        This is a DeBruijn network
        '''
        adj = {}
        for kmer in self.rows:
            skey = kmer[:-1]
            sval = kmer[1:]

            if skey in adj:
                adj[skey].append(sval)
            else:
                adj[skey] = [sval]
        return adj

    def eulerPath(self, adj):
        euler = EulerPath(adj)
        return euler.eulerPath()

    def assemble(self, circuit):
        '''
        Turn the Euler path through the DeBruijn network into a sequence
        by merging the overlapping edges
        '''
        seq = circuit[0]
        for elt in circuit[1:]:
            seq = seq + elt[-1]
        return seq

class Contig():

    def __init__(self, kmers):
        self.sequencer = Sequence(kmers)

    def getNode(self, graph, name):
        if name in graph:
            node = graph[name]
        else:
            node = Node(name)
            graph[name] = node
        return node

    def readKmers(self):
        return self.sequencer.debruijn()

    def readAdj(self):
        graph = {}
        for adjs in self.sequencer.rows:
            nodes = adjs.split('->')
            src = nodes[0].strip()
            srcnode = self.getNode(graph, src)

            for deststr in nodes[1].split(','):
                dest = deststr.strip()
                destnode = self.getNode(graph, dest)
                srcnode.outs.append(destnode)
                destnode.ins.append(srcnode)
        return graph

    def getBranches(self, graph):
        '''
        Paths ← empty list
        for each node v in Graph
            if v is not a 1-in-1-out node
                if out(v) > 0
                    for each outgoing edge (v, w) from v
                        Path ← the path consisting of single edge (v, w)
                        while w is a 1-in-1-out node
                            extend NonBranchingPath by the edge (w, u) 
                            w ← u
                        add NonBranchingPath to the set Paths
        for each isolated cycle Cycle in Graph
            add Cycle to Paths
        return Paths
        '''

        paths = []
        visited = set()
        for _,curnode in graph.items():
            if (len(curnode.outs) != 1) or (len(curnode.ins) != 1):
                for v in curnode.outs:
                    curpath = [curnode, v]
                    visited.add(curnode.name)
                    visited.add(v.name)
                    while (len(v.outs) == 1) and (len(v.ins) == 1):
                        v = v.outs[0]
                        visited.add(v.name)
                        curpath.append(v)
                    paths.append(curpath)

        for _,curnode in graph.items():
            if curnode.name not in visited:
                curpath = [curnode]
                v = curnode
                while (len(v.outs) == 1) and (v.name not in visited):
                    visited.add(v.name)
                    v = v.outs[0]
                    curpath.append(v)
                paths.append(curpath)
        
        return paths

    def assemble(self, paths):
        seqs = []
        for path in paths:
            names = [v.name for v in path]
            seq = self.sequencer.assemble(names)
            seqs.append(seq)
        return seqs

kmers = [row.rstrip() for row in sys.stdin.readlines()]
contig = Contig(kmers)
adj = contig.readKmers()

euler = EulerPath(adj)
paths = contig.getBranches(euler.graph)
seqs = contig.assemble(paths)
print(' '.join(seqs))
