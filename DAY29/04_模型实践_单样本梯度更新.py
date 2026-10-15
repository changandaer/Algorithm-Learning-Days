# DAY29：复用自己已正确的四个类，独立新增单样本梯度更新与验证；要求见同目录课程。

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
        for i in range(self.dataset.size()):
            xs,ys = self.dataset.get_item(i)
            prediction = model.forward(xs)
            predictions.append(prediction)
        
        loss = self.loss.mean(predictions,self.dataset.ys)
        
        return loss

class GradientDescent:
    def __init__(self,learning_rate):
        self.learning_rate = learning_rate

    def step(self, model, grad_w, grad_b):
        model.weight -= self.learning_rate * grad_w
        model.bias -= self.learning_rate * grad_b
        return model.weight,model.bias


dataset = RegressionDataset([2],[5])
loss = SquaredLoss()
neuron = LinearNeuron(0,1)
another_name = neuron
print(another_name is neuron)

evaluator = LossEvaluator(dataset,loss)
old_loss = evaluator.evaluate(neuron)
print(old_loss)

grad_w = (neuron.forward(dataset.xs[0]) - dataset.ys[0]) * dataset.xs[0]
grad_b = (neuron.forward(dataset.xs[0]) - dataset.ys[0])
print(grad_w,grad_b)

gradient = GradientDescent(0.1)
neuron.weight,neuron.bias = gradient.step(neuron,grad_w,grad_b)
print(neuron.weight,neuron.bias)

new_prediction = neuron.forward(dataset.xs[0])
print(new_prediction)
new_loss = evaluator.evaluate(neuron)
print(new_loss)