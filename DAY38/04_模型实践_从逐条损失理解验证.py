# 复用 DAY35 的六个类、batch_gradient 和实验。
# 在 LossEvaluator 新增 sample_losses，先核对固定模型的逐条损失和平均值。
# 能解释每一步后，接到原有训练候选的验证报告，记录参数与数据保持检查。
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
        loss_mean = self.loss.mean(predictions,self.data.ys)
        return loss_mean
    def sample_losses(self,model):
        sample_losses_list = []
        for i in range(self.data.size()):
            single_xs,single_ys = self.data.get_item(i)
            sample_loss = ((model.forward(single_xs) - single_ys) ** 2)/2
            sample_losses_list.append(sample_loss)
        return sample_losses_list


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

        self.evaluator = LossEvaluator(self.data,self.loss)
        self.optimizer = optimizer

    def train(self):
        old_loss = self.evaluator.evaluate(self.model)
        g_w,g_b = batch_gradient(self.model,self.data)
        self.optimizer.step(self.model,g_w,g_b)
        new_loss = self.evaluator.evaluate(self.model)
        return new_loss

    def fit(self,epochs):
        loss_list = []
        loss_list.append(self.evaluator.evaluate(self.model))
        for i in range(epochs):
            new_loss = self.train()
            loss_list.append(new_loss)
        return loss_list



       
       


