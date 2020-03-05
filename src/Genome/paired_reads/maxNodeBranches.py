import sys

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

class Node():
  def __init__(self, name):
    self.name = name
    self.ins = []
    self.outs = []

class Contig():

    def getNode(self, graph, name):
        if name in graph:
            node = graph[name]
        else:
            node = Node(name)
            graph[name] = node
        return node


    def readAdj(self, rows):
        graph = {}
        for adjs in rows:
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

rows = [row.rstrip() for row in sys.stdin.readlines()]

contig = Contig()
adj = contig.readAdj(rows)
branches = contig.getBranches(adj)
             
for path in branches:
    print(" -> ".join([v.name for v in path]))
