# DAY36：实现双特征模型前向，并将已知档位的查表向量接入模型。
class LinearNeuron2D:
    def __init__(self, weight1, weight2, bias):
        self.weight1 = weight1
        self.weight2 = weight2
        self.bias = bias
    
    def forward(self,features):
        return self.weight1 * features[0] + self.weight2 * features[1] + bias
