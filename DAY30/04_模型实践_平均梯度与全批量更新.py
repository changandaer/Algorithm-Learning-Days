# DAY30：复用已正确的模型部件，自写平均梯度与批量一步更新；要求见同目录课程。

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
        return ((prediction - target)**2)/2
    def mean(self,predictions,targets):
        total = 0
        for i in range(len(predictions)):
            total += self.forward(predictions[i],targets[i])
        return total/len(predictions)

class LossEvaluator:
    def __init__(self,dataset,loss):
        self.dataset = dataset
        self.loss = loss
    def evaluate(self,model):
        predictions = []
        for index in range(self.dataset.size()):
            xs,ys = self.dataset.get_item(index)
            prediction = model.forward(xs)
            predictions.append(prediction)
        mse = self.loss.mean(predictions,self.dataset.ys)

        return mse

class GradientDescent:
    def __init__(self,learning_rate):
        self.learning_rate = learning_rate
    def step(self,model,g_w,g_b):
        w = model.weight - self.learning_rate * g_w
        b = model.bias - self.learning_rate * g_b
        return w,b

def batch_gradients(model, data):
    g_w,g_b = 0,0
    for i in range(data.size()):
        xs,ys = data.get_item(i)
        g_w += (model.forward(xs) - ys) * xs
        g_b += model.forward(xs) - ys
    
    return g_w/data.size(),g_b/data.size()

neuron = LinearNeuron(0,0)
dataset = RegressionDataset([-1,0,1,2],[-1,1,3,5])
loss = SquaredLoss()
gradient_desent = GradientDescent(0.1)
evaluator = LossEvaluator(dataset,loss)
g_w,g_b = batch_gradients(neuron,dataset) 

# 评估旧损失；调用平均梯度函数；确认此时参数仍为0、0
print(evaluator.evaluate(neuron),neuron.weight,neuron.bias)

# 调用旧step一次；再评估。输出两梯度、新参数、前后损失，对照上表
w_new,b_new = gradient_desent.step(neuron,g_w,g_b)
neuron_new = LinearNeuron(w_new,b_new)
print(w_new,b_new,evaluator.evaluate(neuron_new))




