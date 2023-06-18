import heapq

def str_to_list(s:str, delim=' ')->str:

    """
    Split a string into a list by a given separator.
    """

    j=0
    seqs=[]
    for i in range(len(s)):
        if s[i]==delim or s[i]=='\n':
            seqs+=[s[j:i]]
            j=i+1
    
    if j!=len(s):
        seqs+=[s[j:]]
    
    return seqs


class ProteinNet(object):

    def __init__(self, filename):
        self.graph=dict()

        with open(filename) as ofl:
            useless=ofl.readline()
            self.info=list()
            self.name_node=dict()
            self.node_name=dict()
            i=1
            for line in ofl:
                info_all=str_to_list(line,delim="\t")
                info=list()
                if info_all[0] not in self.name_node:
                    self.name_node[info_all[0]]=i
                    self.node_name[i]=info_all[0]
                    i+=1
                if info_all[1] not in self.name_node:
                    self.name_node[info_all[1]]=i
                    self.node_name[i]=info_all[1]
                    i+=1    
                info.append(self.name_node[info_all[0]])
                info.append(self.name_node[info_all[1]])
                info.append(float(info_all[12]))
                self.info.append(info)

        for i in range(len(self.info)):
            self.graph.setdefault(self.info[i][0], {})[self.info[i][1]]=self.info[i][2]
            self.graph.setdefault(self.info[i][1], {})[self.info[i][0]]=self.info[i][2]
        
    def dijkstra(self, start, end):

        start=self.name_node[start]
        end=self.name_node[end]

        # 创建节点距离字典
        distances={node: float('inf') for node in self.graph}
        distances[start] = 0

        # 创建前驱节点字典
        predecessors={node: None for node in self.graph}

        # 创建堆
        pq=[(0, start)]

        while pq:
            # 取出堆顶
            current_distance, current_node=heapq.heappop(pq)
            # 判断是否到达终点，如果到达则直接返回
            if current_node==end:
                path=[]
                while current_node is not None:
                    path.append(self.node_name[current_node])
                    current_node = predecessors[current_node]
                path.reverse()
                return path
            # 遍历邻接节点
            for neighbor, weight in self.graph[current_node].items():
                distance=current_distance + weight
                # 更新距离和前驱节点
                if distance<distances[neighbor]:
                    distances[neighbor]=distance
                    predecessors[neighbor]=current_node
                    heapq.heappush(pq,(distance, neighbor))
        # 如果无法到达终点，则返回空路径
        return None

# 测试
# net_test=ProteinNet('string_interactions.tsv')
# print("The shortest path between {} and {} is: {}".format('wecG','rfbB',net_test.dijkstra('wecG','rfbB')))

filename=input('Please enter the name of the file: ')
net=ProteinNet(filename)
a=input('Please enter the name of the first protein: ')
b=input('Please enter the name of the second protein: ')
if a not in net.name_node:
    with open('Out.txt','w') as ofl:
        ofl.write('{} is not included in the network'.format(a))
    raise ValueError('{} is not included in the network'.format(a))
if b not in net.name_node:
    with open('Out.txt','w') as ofl:
        ofl.write('{} is not included in the network'.format(b))
    raise ValueError('{} is not included in the network'.format(b))
with open('Out.txt','w') as ofl:
    ofl.write("The shortest path between {} and {} is: {}".format(a,b,net.dijkstra(a,b)))