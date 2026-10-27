# DAY32：复用正确的Trainer，自己新增fit并完成100步及连续训练检查；要求见同目录课程。

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
        self.prediction = prediction
        self.target = target
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
        mse = self.loss.mean(predictions,self.data.ys)
        return mse

class GradientDescent:
    def __init__(self,learning_rate):
        self.learning_rate = learning_rate
    def step(self,model,g_w,g_b):
        model.weight -= g_w * self.learning_rate
        model.bias -= g_b * self.learning_rate
        

def batch_gradients(model,data):
    g_w,g_b=0,0
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

        mean_g_w,mean_g_b = batch_gradients(self.model,self.data)

        self.optimizer.step(self.model,mean_g_w,mean_g_b)

        new_loss = self.evaluator.evaluate(self.model)

        return new_loss

    def fit(self,steps):
        loss_list = []
        loss_list.append(self.evaluator.evaluate(self.model))
        for i in range(steps):
            loss = self.train()
            loss_list.append(loss)
        return loss_list

model = LinearNeuron(0,0)
loss = SquaredLoss()
data = RegressionDataset([-1,0,1,2],[-1,1,3,5])
optimizer = GradientDescent(0.1)
trainer = Trainer(model, data, loss, optimizer)
loss_list = trainer.fit(0)
print(loss_list)
loss_list = trainer.fit(1)
print(loss_list)
loss_list = trainer.fit(2)
print(loss_list)
loss_list = trainer.fit(10)
print(loss_list)
loss_list = trainer.fit(50)
print(loss_list)
loss_list = trainer.fit(100)
print(loss_list)
