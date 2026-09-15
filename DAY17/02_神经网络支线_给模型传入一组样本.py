"""DAY17任务2：复用自己的单输入神经元，为多次单值预测写普通函数；接口和测试见课程。"""

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

    def predict_samples(self, samples):

        z_list = []

        for sample in samples:

            z = self.forward(sample)

            z_list.append(z)
        
        return z_list

neuron = SingleNeuron(2,1)
assert neuron.predict_samples([-1,0,2]) == [0,1,5]
assert neuron.predict_samples([]) == []
assert neuron.predict_samples([4]) == [9]

