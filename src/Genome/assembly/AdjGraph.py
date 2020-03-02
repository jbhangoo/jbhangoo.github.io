class AdjNode():
    def __init__(self, name):
        '''
        Directed adjacency graph node. It holds a label, a list of input nodes and a list of output nodes
        :param name: What to label this node
        '''
        self.name = name
        self.ins = []
        self.outs = []

class AdjGraph():
    def __init__(self, overlaps):
        '''
        Create a graph where each sequence is a node
        :param overlaps: adjasency dictionayy of overlaps
        :return: Adjacency graph
        '''
        self.graph = {}
        for src,destlist in overlaps.items():
            srcnode = self.getNode(src)
            for dest in destlist:
                destnode = self.getNode(dest[0])
                srcnode.outs.append((destnode, dest[1]))
                destnode.ins.append((srcnode, dest[1]))

    def getNode(self, name):
        '''
        Return the adjasency graph node with the given label, creating a new one if needed
        :param name:
        :return:        Node with the given label
        '''
        if name in self.graph:
            node = self.graph[name]
        else:
            node = AdjNode(name)
            self.graph[name] = node
        return node

    '''
    Get all Maximal non-Branching paths algorithm

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

    def getAllBranches(self):
        '''
        Separate the graph into disjoint branches that do not share any edges
        :param graph:   adjasency graph
        :return:        list of the paths that represent all graph branches
        '''
        paths = []
        visited = set()
        for _, curnode in self.graph.items():
            if (len(curnode.outs) != 1) or (len(curnode.ins) != 1):
                for vpair in curnode.outs:
                    v = vpair[0]
                    curpath = [(curnode, 0), vpair]
                    visited.add(curnode.name)
                    visited.add(v.name)
                    while (len(v.outs) == 1) and (len(v.ins) == 1):
                        vpair = v.outs[0]        # We know there is exactly one node in the outs list
                        v = vpair[0]
                        visited.add(v.name)
                        curpath.append(vpair)
                    paths.append(curpath)

        for _, curnode in self.graph.items():
            if curnode.name not in visited:
                curpath = [(curnode, 0)]
                v = curnode
                while (len(v.outs) == 1) and (v.name not in visited):
                    visited.add(v.name)
                    vpair = v.outs[0]  # We know there is exactly one node in the outs list
                    v = vpair[0]
                    curpath.append(vpair)
                paths.append(curpath)

        return paths

    def assembleContigs(self, paths):
        '''
        Convert each path in the set into a single sequence by merging overlaps
        :param paths:   Set of paths through a graph
        :return:        Set of contigs
        '''
        seqs = []
        for path in paths:
            seq = path[0][0].name
            for i in range(1, len(path)):
                node = path[i][0]
                startpos = path[i][1]
                seq += node.name[startpos:]
            seqs.append(seq)
        return seqs