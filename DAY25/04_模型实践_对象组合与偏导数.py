"""DAY25模型实践：复用已理解的部件，自己重写平均损失与评估方法，再完成单样本偏导数实验；接口和结果见课程。"""
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
        return len(self.xs)
    def get_item(self,index):
        return self.xs[index],self.ys[index]

class SquaredLoss:
    def forward(self,prediction,target):
        return ((prediction-target)**2)/2
    def mean(self,predictions,targets):
        total = 0
        for i in range(len(predictions)):
            loss = self.forward(predictions[i],targets[i])
            total += loss
        return total/len(predictions)

class LossEvaluator:
    def __init__(self,data,loss):
        self.data = data
        self.loss = loss
    
    def evaluate(self,model):
        predictions = []
        for i in range(self.data.size()):
            single_xs,single_ys = self.data.get_item(i)
            single_prediction = model.forward(single_xs)
            predictions.append(single_prediction)
        mse_loss = self.loss.mean(predictions,self.data.ys)
    
    return mse_loss

