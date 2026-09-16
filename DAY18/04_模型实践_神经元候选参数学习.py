"""DAY18 模型实践：复用自己的神经元，从候选权重中学习参数；新方法、三步分析与测试由自己完成。"""

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
    
    def fit(self, xs, ys, candidate_weights):

        for candidate_weight in candidate_weights:

            ys_hat = [] 

            for x_s in xs:

                ys_hat.append(x_s * candidate_weight + self.bias)
            
            if ys_hat == ys:

                self.weight = candidate_weight

                return candidate_weight

neuron_A = SingleNeuron(0,1)
candidate_weight = neuron_A.fit([0,1,2],[1,3,5],[1,2,3])
print(candidate_weight)
z = neuron_A.forward(3)
print(z)              

neuron_B = SingleNeuron(0,0)
candidate_weight = neuron_B.fit([1,2],[3,6],[1,2,3])
print(candidate_weight)
z = neuron_B.forward(3)
print(z) 

neuron_A = SingleNeuron(0,1)
candidate_weight = neuron_A.fit([0,1,2],[1,2,3],[1,2,3])
print(candidate_weight)
z = neuron_A.forward(3)
print(z)  

