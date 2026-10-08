"""DAY27：分段验证神经元、数据集、损失及评估器，重点理解属性、参数、调用和返回，不实现新的训练器。"""

class LinearNeuron:
    def __init__(self,init_weight,init_bias):
        self.weight = init_weight
        self.bias = init_bias
    
    def forward(self,x):
        return self.weight * x + self.bias

class RegressionDataset:
    def __init__(self,init_xs,init_ys):
        self.xs = init_xs
        self.ys = init_ys
    
    def size(self):
        return len(self.xs)
    
    def get_item(self,index):
        return self.xs[index],self.ys[index]

class SquaredLoss:
    def forward(self,prediction,target):
        return ((prediction-target)**2)/2
    def mean(self,predictions,targets):
        total = 0
        for i in range(len(predictions)):
            total += self.forward(predictions[i],targets[i])
        return total/len(predictions)

class LossEvaluator:
    def __init__(self,init_data,init_loss):
        self.data = init_data
        self.loss = init_loss
    def evaluate(self,model):
        predictions = []
        targets = []
        for i in range(self.data.size()):
            xs,ys = self.data.get_item(i)
            predictions.append(model.forward(xs))
            targets.append(ys)
        mse = self.loss.mean(predictions,targets)
    
        return mse
            

