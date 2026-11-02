# DAY34：复用正确模型部件，比较干净与有误训练数据在同一留出集上的表现；要求见同目录课程。

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
    def __init__(self,data,loss):
        self.data = data
        self.loss = loss
    def evaluate(self,model):
        predictions = []
        for i in range(self.data.size()):
            single_xs,single_ys = self.data.get_item(i)
            prediction = model.forward(single_xs)
            predictions.append(prediction)
        mean_loss = self.loss.mean(predictions,self.data.ys)

        return mean_loss

class GradientDescent:
    def __init__(self,learning_rate):
        self.learning_rate = learning_rate
    def step(self,model,g_w,g_b):
        model.weight -= self.learning_rate * g_w
        model.bias -= self.learning_rate * g_b

def batch_gradient(model,data):
    g_w,g_b = 0,0
    for i in range(data.size()):
        single_xs,single_ys = data.get_item(i)
        g_w += (model.forward(single_xs) - single_ys) * single_xs
        g_b += (model.forward(single_xs) - single_ys) * 1
    return g_w/data.size(),g_b/data.size()

class Trainer:
    def __init__(self,model,data,loss,optimizer):
        self.model = model
        self.data = data
        self.loss = loss
        self.optimizer = optimizer

        self.evaluator = LossEvaluator(self.data,self.loss)
    
    def train(self):
        old_loss = self.evaluator.evaluate(self.model)

        mean_g_w,mean_g_b = batch_gradient(self.model,self.data)
        self.optimizer.step(self.model,mean_g_w,mean_g_b)

        new_loss = self.evaluator.evaluate(self.model)

        return new_loss
    
    def fit(self,epochs):
        loss_list = []
        loss_list.append(self.evaluator.evaluate(self.model))
        for i in range(epochs):
            loss_list.append(self.train())
        return loss_list
            

loss = SquaredLoss()
optimizer = GradientDescent(0.1)
data_test = RegressionDataset([-2,3],[-3,7])

model_clean = LinearNeuron(0,0)
data_clean = RegressionDataset([-1, 0, 1, 2], [-1, 1, 3, 5])
trainer_clean = Trainer(model_clean,data_clean,loss,optimizer)
counts_clean = {}
loss_list_clean = trainer_clean.fit(100)
counts_clean['初始损失'] = loss_list_clean[0]
counts_clean['一步后损失'] = loss_list_clean[1]
counts_clean['最终损失'] = loss_list_clean[-1]
print(f"最终(w,b)值：{model_clean.weight},{model_clean.bias}")
print(f"数据干净时：{counts_clean}")

evaluate_clean = LossEvaluator(data_test,loss).evaluate(model_clean)
print(f"数据干净时的测试集损失为：{evaluate_clean}")

model_dirty = LinearNeuron(0,0)
data_dirty = RegressionDataset([-1, 0, 1, 2], [-1, 1, 3, 11])
trainer_dirty = Trainer(model_dirty,data_dirty,loss,optimizer)
counts_dirty = {}
loss_list_dirty = trainer_dirty.fit(100)
counts_dirty['初始损失'] = loss_list_dirty[0]
counts_dirty['一步后损失'] = loss_list_dirty[1]
counts_dirty['最终损失'] = loss_list_dirty[-1]
print(f"最终(w,b)值：{model_dirty.weight},{model_dirty.bias}")
print(f"数据不干净时：{counts_dirty}")

evaluate_dirty = LossEvaluator(data_test,loss).evaluate(model_dirty)
print(f"数据不干净时的测试集损失为：{evaluate_dirty}")
