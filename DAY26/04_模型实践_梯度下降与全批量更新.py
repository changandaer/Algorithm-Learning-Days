"""DAY26模型实践：复用已掌握部件，自己实现更新器与平均梯度，验证单样本及全批量的一步更新；要求见课程。"""

class LinearNeuron:

    def __init__(self,weight,bias):
        self.weight = weight
        self.bias = bias
    
    def forward(self,x):
        return self.weight * x + self.bias

class RegressionDataset:

    def __init__(self,xs,ys):
        self.xs = xs
        self.ys = ys
    
    def size(self):
        return len(xs)
    
    def get_item(self,index):
        return self.xs[index],self.ys[index]

class SquaredLoss:

    def prediction(self,model,data):

        mse = ((self.model.forward - self.data.ys) ** 2) / self.data.size
    
    def predictions(self,model,data):


class LossEvaluator:

    def evaluate(self,model):
