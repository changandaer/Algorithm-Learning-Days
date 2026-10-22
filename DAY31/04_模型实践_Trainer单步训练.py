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
    g_w = 0,g_b = 0
    for i in range(data.size()):
        xs,ys = data.get_item(i)
        g_w += (model.forward(xs) - ys) * xs
        g_b += (model.forward(xs) - ys) * 1
    return g_w/data.size(),g_b/data.size()


