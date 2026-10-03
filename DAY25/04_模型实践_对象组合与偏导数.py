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

dataset_1 = RegressionDataset([0,2],[1,5])
loss = SquaredLoss()
neuron_1_0 = LinearNeuron(1,0)
neuron_2_1 = LinearNeuron(2,1)
loss_evaluate_1 = LossEvaluator(dataset_1,loss)
loss_1_0 = loss_evaluate_1.evaluate(neuron_1_0)
print(loss_1_0)
loss_2_1 = loss_evaluate_1.evaluate(neuron_2_1)
print(loss_2_1)
loss_1_0 = loss_evaluate_1.evaluate(neuron_1_0)
print(loss_1_0)

loss_mean = loss.mean([0,0],[1,3])
print(loss_mean)

dataset_2 = RegressionDataset([2],[5])
loss_evaluate_2 = LossEvaluator(dataset_2,loss)

data = RegressionDataset([-1, 0, 1, 2], [-1, 1, 3, 5])
evaluator = LossEvaluator(data, loss)
base = LinearNeuron(1, 0)
base_loss = evaluator.evaluate(base)
assert base_loss == 1.75
assert evaluator.evaluate(base) == 1.75
print("基准平均损失：", base_loss)

for h in [0.1, 0.01]:
    weight_trial = LinearNeuron(base.weight + h, base.bias)
    weight_loss = evaluator.evaluate(weight_trial)
    weight_rate = (weight_loss - base_loss) / h

    bias_trial = LinearNeuron(base.weight, base.bias + h)
    bias_loss = evaluator.evaluate(bias_trial)
    bias_rate = (bias_loss - base_loss) / h

    assert abs(weight_loss - (1.75 - 2 * h + 0.75 * h * h)) < 0.000001
    assert abs(bias_loss - (1.75 - 1.5 * h + 0.5 * h * h)) < 0.000001
    assert abs(weight_rate - (-2 + 0.75 * h)) < 0.000001
    assert abs(bias_rate - (-1.5 + 0.5 * h)) < 0.000001

    print("只改变w：", h, weight_loss, weight_rate)
    print("只改变b：", h, bias_loss, bias_rate)

assert base.weight == 1
assert base.bias == 0
assert data.xs == [-1, 0, 1, 2]
assert data.ys == [-1, 1, 3, 5]