# DAY31：复用正确部件并接好原实例更新，自己实现Trainer与连续两次验证；要求见同目录课程。

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
        loss = ((prediction - target)**2)/2
        return loss
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
        for i in range(self.dataset.size()):
            xs,ys = self.dataset.get_item(i)
            prediction = model.forward(xs)
            predictions.append(prediction)
        mse = self.loss.mean(predictions,self.dataset.ys)
        return mse

class GradientDescent:
    def __init__(self,learning_rate):
        self.learning_rate = learning_rate
    def step(self,model,g_w,g_b):
        model.weight -= self.learning_rate * g_w
        model.bias -= self.learning_rate * g_b

# batch_gradients 这个函数计算平均梯度为什么不写成类呢，为什么只需要写成普通函数就可以了呢？
def batch_gradients(model, data):
    g_w ,g_b = 0,0
    for i in range(data.size()):
        xs,ys = data.get_item(i)
        g_w += (model.forward(xs) - ys) * xs
        g_b += (model.forward(xs) - ys) * 1
    return g_w/data.size(),g_b/data.size()

class Trainer:
    def __init__(self,model,data,loss,optimizer):
        self.model = model
        self.data = data
        self.loss = loss
        self.optimizer = optimizer

        # 建立对应的评估器
        self.evaluator = LossEvaluator(self.data,self.loss)
    def train_step(self):
        #1.用旧参数计算损失
        old_loss = self.evaluator.evaluate(self.model)

        #2.计算平均梯度
        mean_g_w,mean_g_b = batch_gradients(self.model,self.data)

        #3.计算新参数并更新模型参数
        self.optimizer.step(self.model,mean_g_w,mean_g_b)

        #4.用更新参数后的模型重新计算新损失
        new_loss = self.evaluator.evaluate(self.model)

        return old_loss,new_loss



model = LinearNeuron(0, 0)
alias = model
data = RegressionDataset([-1, 0, 1, 2], [-1, 1, 3, 5])
loss = SquaredLoss()
evaluator = LossEvaluator(data, loss)
optimizer = GradientDescent(0.1)

print(batch_gradients(model,data))
trainer = Trainer(model,data,loss,optimizer)
old_loss,new_loss = trainer.train_step()
print(old_loss,new_loss)
print(model.weight,model.bias)
print(batch_gradients(model,data))

trainer = Trainer(model,data,loss,optimizer)
old_loss,new_loss = trainer.train_step()
print(old_loss,new_loss)
print(model.weight,model.bias)
print(batch_gradients(model,data))

assert model is alias
