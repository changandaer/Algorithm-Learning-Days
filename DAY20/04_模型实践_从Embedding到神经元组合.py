"""DAY20模型实践：复用Embedding和神经元，独立完成TinyNetwork与一维表示的连接；三步、新实现及测试自己写。"""
class SingleNeuron:

    def __init__(self,weight,bias):

        self.weight = weight
        self.bias = bias
    
    def forward(self,x):

        z = self.weight * x + self.bias

        if z > 0:
            return z
        else:
            return 0

class TinyNetwork:

    def __init__(self,w1,b1,w2,b2):

        self.first = SingleNeuron(w1,b1)
        self.second = SingleNeuron(w2,b2)
    
    def forward(self,x):

        h = self.first.forward(x)
        z = self.second.forward(h)

        return h,z

net_A = TinyNetwork(2,1,-1,4)
h,z = net_A.forward(-2)
print(h)
print(z)
net_B = TinyNetwork(1,0,2,1)
h,z = net_B.forward(-1)
print(h)
print(z)