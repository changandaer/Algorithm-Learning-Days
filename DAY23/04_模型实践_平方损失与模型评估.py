"""DAY23模型实践：复用旧数据集与神经元，自己实现SquaredLoss并比较三组模型预测的平均损失；接口和测试见课程。"""

class LinearNeuron:

    def __init__(self,weight,bias):
        self.weight = weight
        self.bias = bias
    
    def forward(self,x):
        return self.weight * x + self.bias

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

class RegressionDataset:

    def __init__(self,xs,ys):
        
        self.xs = xs
        self.ys = ys
    
    def size(self):

        return len(self.xs)
    
    def get_item(self,index):

        return (xs[index],ys[index])

class SquaredLoss:
    
    def forward(self, prediction, target):

        return ((prediction - target)**2)/2
    
    def mean(self, predictions, targets):

        total = 0

        for i in range(len(predictions)):

            loss = self.forward(predictions[i],targets[i])
            total += loss
            i += 1

        return total/len(predictions)

 
loss = SquaredLoss()
assert loss.forward(3, 1) == 2
assert loss.forward(-1, -1) == 0
assert loss.forward(-2, 1) == 4.5
assert loss.mean([0, 2], [1, 1]) == 0.5
assert loss.mean([3], [1]) == 2

data = RegressionDataset([-1,0,1,2],[-1,1,3,5])
linear_1_0 = LinearNeuron(1,0)
linear_2_1 = LinearNeuron(2,1)
relu_2_1 = SingleNeuron(2,1)

linear_1_0_predictions = []
for i in range(data.size()):
    prediction = linear_1_0.forward(data.xs[i])
    linear_1_0_predictions.append(prediction)
linear_1_0_loss = loss.mean(linear_1_0_predictions,data.ys)
print(linear_1_0_loss)

linear_2_1_predictions = []
for i in range(data.size()):
    prediction = linear_2_1.forward(data.xs[i])
    linear_2_1_predictions.append(prediction)
linear_2_1_loss = loss.mean(linear_2_1_predictions,data.ys)
print(linear_2_1_loss)

relu_2_1_predictions = []
for i in range(data.size()):
    prediction = relu_2_1.forward(data.xs[i])
    relu_2_1_predictions.append(prediction)
relu_2_1_loss = loss.mean(relu_2_1_predictions,data.ys)
print(relu_2_1_loss)