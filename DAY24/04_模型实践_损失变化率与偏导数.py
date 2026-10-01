"""DAY24模型实践：复用已有模型、数据集和损失，自己实现评估器并比较邻近参数的损失变化率；接口与预期见课程。"""
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
    
    def __init__(self, dataset, loss):

        self.dataset = dataset
        self.loss = loss

    def evaluate(self, model):

        predictions = []

        for i in range(self.dataset.size()):

            single_xs,single_ys = self.dataset.get_item(i)
            single_prediction = model.forward(single_xs)
            predictions.append(single_prediction)
            single_loss = self.loss.forward(single_prediction,single_ys)

            
        total = self.loss.mean(predictions,self.dataset.ys)

        return total
    


mse_loss = SquaredLoss()
data = RegressionDataset([-1,0,1,2],[-1,1,3,5])
evaluator = LossEvaluator(data,mse_loss)
assert data.size() == 4
assert data.get_item(0) == (-1,-1)
linear_1_0 = LinearNeuron(1,0)
linear_2_1 = LinearNeuron(2,1)

linear_1_0_loss = evaluator.evaluate(linear_1_0)
print(linear_1_0_loss)
linear_2_1_loss = evaluator.evaluate(linear_2_1)
print(linear_2_1_loss)