class Node():
  def __init__(self, name):
    self.name = name
    self.ins = []
    self.outs = []

class EulerCycle():
    def initFromAdj(self, adj):
        self.graph = {}
        for src,destlist in adj.items():
            srcnode = self.getNode(src)
            for dest in destlist:
                destnode = self.getNode(dest)
                srcnode.outs.append(destnode)
                destnode.ins.append(srcnode)

    def __init__(self, rows):
        self.graph = {}
        for adjs in rows:
            nodes = adjs.split('->')
            src = nodes[0].strip()
            srcnode = self.getNode(src)

            for deststr in nodes[1].split(','):
                dest = deststr.strip()
                destnode = self.getNode(dest)
                srcnode.outs.append(destnode)
                destnode.ins.append(srcnode)

    def findFirstNode(self):
        curnode = next( iter( self.graph.values()) )
        return curnode

    def getNode(self, name):
        if name in self.graph:
            node = self.graph[name]
        else:
            node = Node(name)
            self.graph[name] = node
        return node

    def eulerCycle(self):
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