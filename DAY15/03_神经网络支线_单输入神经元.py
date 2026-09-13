"""DAY15任务3：手算并实现单输入ReLU神经元，用类保存各自参数；要求见课程，自己写分析、实现和测试。"""

class SingleNeuron:

    def __init__(self,weight,bias):

        self.weight = weight
        self.bias = bias

    def forward(self,x):

        ReLU = self.weight*x + self.bias

        if ReLU > 0:
            return self.weight*x + self.bias
        else:
            return 0

SingleNeuron_1 = SingleNeuron(2,-1)
assert SingleNeuron_1.forward(3) == 5
assert SingleNeuron_1.forward(0) == 0
assert SingleNeuron_1.forward(0.5) == 0

SingleNeuron_2 = SingleNeuron(-1,2)
assert SingleNeuron_2.forward(3) == 0
assert SingleNeuron_2.forward(-1) == 3