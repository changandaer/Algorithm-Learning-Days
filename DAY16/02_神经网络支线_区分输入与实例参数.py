"""DAY16任务2：独立重写单输入神经元，用换输入和双实例实验区分参数与输入；要求见课程。"""

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

neuron_A = SingleNeuron(3,-2)
z = neuron_A.forward(2)
print(z)
z = neuron_A.forward(0)
print(z)


neuron_B = SingleNeuron(-2,1)
z = neuron_B.forward(2)
print(z)
z = neuron_B.forward(-2)
print(z)

z = neuron_A.forward(2)
print(z)

neuron_A.weight = 1
neuron_A.bias = -2
z = neuron_A.forward(2)
print(z)

z = neuron_B.forward(-2)
print(z)