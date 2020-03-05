class Node():
  def __init__(self, name):
    self.name = name
    self.ins = []
    self.outs = []

class EulerPath():
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

#rows = [row.rstrip() for row in sys.stdin.readlines()]
"""
"""
rows = [
'0 -> 2',
'1 -> 3',
'2 -> 1',
'3 -> 0,4',
'6 -> 3,7',
'7 -> 8',
'8 -> 9',
'9 -> 6'
]
#adj = readAdj(rows)
euler = EulerPath(rows)
circuit = euler.eulerPath()
outlist = "->".join(circuit)
#outlist += "->"+circuit[-1]
with open("dataset.out","w") as outf:
    outf.write(outlist)
print(outlist)