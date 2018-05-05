from  collections import deque
import re

def del_space(val):
    s = ''
    for i in val:
        s += i if i != ' ' else ''
    return s
 
 
class graph:
    def __init__(self):
        self.graph = {}
 
    def addVert(self, name):
        self.graph.update({name: set()})
 
    def addEdge(self, a, b, predic):
        if a not in self.graph:
            self.addVert(a)
        if b not in self.graph:
            self.addVert(b)
        self.graph[a].add((b, predic))
 
    def addDoubleEdge(self, a, b, predic):
        self.addEdge(a, b, predic)
        self.addEdge(b, a, predic)
 
    def printEdge(self):
        for vert in self.graph.keys():
            for to in self.graph[vert]:
                print ("from {0} to {1} predic {2}".format(vert, to[0], to[1]))
 
    def checkConnect(self, a, b, predic):
        q = deque()
        d = {key: 0 for key in self.graph.keys()}
        q.append(a)
        d[a] = 1
        while len(q) > 0:
            v = q.popleft()
            for to in self.graph[v]:
                if to[1] == predic and d[to[0]] == 0:
                    d[to[0]] = d[v] + 1
                    q.append(to[0])
        return d[b] > 0
 
    def checkEdge(self, v):
        return v in self.graph.keys()
 
gr = graph()
var_types = {}
 
def add_predicts(val1, cond, k1, k2=None):
    predic = re.split("\(.*\)", val1)[0]
    val = re.findall("\(.*\)", val1)[0]
    val = val[1:-1]
    val = re.split(',', val)
 
    if len(cond) == 2:
        if val[1] in cond and val[0] in var_types and k2 == None and k1 != val[0]:
            gr.addEdge(val[0], k1, predic)
        elif val[0] in cond and val[1] in var_types and k2 == None and k1 != val[1]:
            gr.addEdge(k1, val[1], predic)
        elif val[0] == cond[0] and val[1] == cond[1]:
            gr.addEdge(k1, k2, predic)
        elif val[1] == cond[0] and val[0] == cond[1]:
            gr.addEdge(k2, k1, predic)
    else:
        if val[0] in var_types or val[1] in var_types:
            if val[0] == cond[0] and k1 != val[1]:
                gr.addEdge(k1, val[1], predic)
            elif val[1] == cond[0] and k1 != val[0]:
                gr.addEdge(val[0], k1, predic)
        else:
            for k_1 in var_types.keys():
                if k_1 == k1:
                    continue
                if val[0] == cond[0]:
                    gr.addEdge(k1, k_1, predic)
                elif val[1] == cond[0]:
                    gr.addEdge(k_1, k1, predic)
 
def make_predicats(val1, val2):
    predic = re.split("\(.*\)", val1)[0]
    val = re.findall("\(.*\)", val1)[0]
    val = val[1:-1]
    val = re.split(',', val)
    val[0] = del_space(val[0])
    if len(val) == 1:
        for k in var_types.keys():
            if var_types[k] == predic:
                add_predicts(val2, val, k)
    else:
        for k_1 in var_types.keys():
            if val[1] in var_types or val[0] in var_types:
                if ((val[0] in var_types and k_1 != val[0] and gr.checkConnect(val[0], k_1, predic)) or (val[1] in var_types and k_1 != val[1] and gr.checkConnect(k_1, val[1], predic))):
                    add_predicts(val2, val, k_1)
            else:
                for k_2 in var_types.keys():
                    if k_1 != k_2 and gr.checkConnect(k_1, k_2, predic):
                        add_predicts(val2, val, k_1, k_2)
 
def do_base(predic, val, ask=False):
    val = val[1:-1]
    val = re.split(',', val)
    val[0] = del_space(val[0])
    if len(val) == 1:
        if ask:
            print("wrong" if var_types.get(val[0], []) != predic else "right")
        else:
            gr.addVert(val[0])
            var_types[val[0]] = predic
    else:
        val[1] = del_space(val[1])
        if ask:
            print("right" if gr.checkConnect(val[0], val[1], predic) else "wrong")
        else:
            gr.addEdge(val[0], val[1], predic)
 
 
while True:
    ln = input()
    if ln == "q":
        break
 
    if "exist" in ln:
        x = re.split("exist", ln)
        val1 = del_space(x[0])
        val2 = del_space(x[1])
        try:
            make_predicats(val1, val2)
        except:
            print("wrong")
            continue
        continue
 
    ask = False
    try:
        predic = re.split("\(.*\)", ln)[0]
        val = re.findall("\(.*\)", ln)[0]
        if (predic[0:2] == "? "):
            ask = True
            predic = predic[2:]
        do_base(predic, val, ask)
    except:
        print("wrong")
        continue