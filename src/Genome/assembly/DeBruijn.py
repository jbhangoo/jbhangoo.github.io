"""
A DeBruijn graph is a directed multi-graph that turns read into k-mers
and stores as an edge from the prefix to the suffix, both of length k-1

Allow for errors. Only create a new node if the segment is not similar to one already seen.
"""
from src.Genome import Levenshtein

class DBNode():
    def __init__(self, name, errors):
        '''
        Save this sequence as a new De Bruijn node. Need to track the input and output nodes
        as well as similar sequences that are within the given Edit Distance of this node's sequence
        :param name:
        :param errors: Similarity is defined as any sequence that is within an Edit Distance of this size
        '''
        self.name = name
        self.members = set()
        self.max_errors = errors
        self.add(name)
        self. ins = set()
        self. outs = set()

    def add(self, name):
        self.members.add(name)

    def isSimilar(self, name):
        '''
        Test if the given name is within the acceptable error by computing the Levenshtein distance to this node's name
        :param name:
        :return:
        '''
        if Levenshtein.distance(name, self.name) <= self.max_errors:
            return True
        return False

class DeBuijn():
    def __init__(self, fastqFile, k, errors):
        '''
        Store all reads from the FASTQ file and extract all k-mers
        Then build a directed multigraph from the left (k-1)-mer to the
        right (k-1)-mer of each k-mer extracted
        '''
        self.k = k
        self.nodes = set()
        self.edges = set()
        with open(fastqFile) as fh:
            self.reads = []
            while True:
                fh.readline()  # skip name line
                read = fh.readline().rstrip()  # read base sequence
                slen = len(read)
                if slen == 0:
                    break
                self.reads.append(read)
                fh.readline()  # skip placeholder line
                fh.readline().rstrip() # skip base quality line

                for i in range(slen-k+1):
                    kmer = read[i:i+k]
                    prefix = kmer[:-1]
                    suffix = kmer[1:]

                    prefixnode = None
                    suffixnode = None
                    for node in self.nodes:
                        if node.isSimilar(prefix):
                            node.add(prefix)
                            prefixnode = node
                        elif node.isSimilar(suffix):
                            node.add(prefix)
                            suffixnode = node
                    if prefixnode is None:
                        prefixnode = DBNode(prefix, errors)
                        self.nodes.add(prefixnode)
                    if suffixnode is None:
                        suffixnode = DBNode(suffix, errors)
                        self.nodes.add(suffixnode)

                    self.edges.add((prefixnode, suffixnode))
                    prefixnode.outs.add(suffixnode)
                    suffixnode.ins.add(prefixnode)

    def findFirstNode(self):
        '''
        An acceptible first node of an Euler path is one whose out-degree is one more than its in-degree.
        Since we do not expect ideal conditions from sequencing reads, allow any node with higher
        out-degree than in-degree. If none, take any node with equal in and out degrees. If none again,
        start from any node
        :return: Start node of an Euler path
        '''
        for curnode in self.nodes:
            if len(curnode.outs) > len(curnode.ins):
                return curnode
        for curnode in self.nodes:
            if len(curnode.outs) == len(curnode.ins):
                return curnode
        return list(self.nodes).pop()

    def visitNode(self, node):
        '''
        While building an Euler path, pass through this node to any output node then continue to build
        the path from there recursively
        :param node:
        '''
        while len(node.outs) > 0:
            nextnode = node.outs.pop()
            self.visitNode(nextnode)
        self.path.append(node.name)

    def eulerPath(self):
        '''
        Try to build an Euler path. This is a destructive process that removes the edges traversed,
        which allows for further assembly of remaining edges
        :return: The path built, in case that is needed for further usage
        '''
        src = self.findFirstNode()
        self.path = []
        self.visitNode(src)
        return self.path[::-1]

    def assembleSequence(self):
        '''
        Assemble the Euler path produced by eulerPath() from a node list into a sequence
        :return: The sequence that corresponds to the Euler path
        '''
        path = self.path[::-1]
        seq = path[0]
        for node in path[1:]:
            seq += node[-1]
        return seq
