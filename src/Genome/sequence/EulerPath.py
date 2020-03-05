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
