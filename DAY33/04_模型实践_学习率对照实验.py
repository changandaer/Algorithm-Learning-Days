# DAY33：复用正确fit，从相同独立初值对比三种学习率；自己组织实验，要求见同目录课程。
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
        error = prediction - target
        return (error**2)/2
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
        mse = self.loss.mean(predictions,self.data.ys)
        return mse

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
        error = model.forward(single_xs) - single_ys
        g_w += error * single_xs
        g_b += error * 1
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
data = RegressionDataset([-1, 0, 1, 2], [-1, 1, 3, 5])

model_0 = LinearNeuron(0,0)
optimizer_0 = GradientDescent(0)
trainer_0 = Trainer(model_0,data,loss,optimizer_0)
counts_0 = {}
loss_list_0 = trainer_0.fit(20)
counts_0['初始损失'] = loss_list_0[0]
counts_0['一步后损失'] = loss_list_0[1]
counts_0['最终损失'] = loss_list_0[-1]
print(f"学习率为0时：{counts_0}")

model_0_1 = LinearNeuron(0,0)
optimizer_0_1 = GradientDescent(0.1)
trainer_0_1 = Trainer(model_0_1,data,loss,optimizer_0_1)
counts_0_1 = {}
loss_list_0_1 = trainer_0_1.fit(20)
counts_0_1['初始损失'] = loss_list_0_1[0]
counts_0_1['一步后损失'] = loss_list_0_1[1]
counts_0_1['最终损失'] = loss_list_0_1[-1]
print(f"学习率为0.1时：{counts_0_1}")

model_2 = LinearNeuron(0,0)
optimizer_2 = GradientDescent(2)
trainer_2 = Trainer(model_2,data,loss,optimizer_2)
counts_2 = {}
loss_list_2 = trainer_2.fit(20)
counts_2['初始损失'] = loss_list_2[0]
counts_2['一步后损失'] = loss_list_2[1]
counts_2['最终损失'] = loss_list_2[-1]
print(f"学习率为2时：{counts_2}")

# 说明损失不降至少可能是哪两类原因。
# 损失不降可能是学习率数值这个超参数选择的不正确，另一个原因是什么？