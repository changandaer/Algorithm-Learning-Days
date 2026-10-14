"""DAY28：验证四类评估链、属性可修改及参数变化的损失；不新增训练器，具体要求见课程。"""

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

    def forward(self,predicition,target):
        return ((predicition - target)**2)/2
    
    def mean(self,predicitions,targets):
        total = 0
        for i in range(len(predicitions)):
            total += self.forward(predicitions[i],targets[i])
        return total/len(predicitions)

class LossEvaluator:

    def __init__(self,data,loss):
        self.data = data
        self.loss = loss
    
    def evaluate(self,model):
        predicitions = []
        for i in range(self.data.size()):
            xs,ys = self.data.get_item(i)
            predicitions.append(model.forward(xs))
        
        loss = self.loss.mean(predicitions,self.data.ys)

        return loss

loss = SquaredLoss()
neuron_A = LinearNeuron(0,1)
neuron_B = LinearNeuron(2,1)
dataset_A = RegressionDataset([-2,1,3],[-3,3,7]) #16+4+36=56 /2 =28
dataset_B = RegressionDataset([0,2],[1,5])
assert dataset_A.size() == 3
assert dataset_B.size() == 2
assert dataset_A.get_item(0) == (-2,-3)


evaluator_A = LossEvaluator(dataset_A,loss)
result__AA = evaluator_A.evaluate(neuron_A)
print(result__AA)

result__AB = evaluator_A.evaluate(neuron_B)
print(result__AB)

evaluator_B = LossEvaluator(dataset_B,loss)
result__BA = evaluator_B.evaluate(neuron_A)
print(result__BA)


neuron_A = LinearNeuron(2,1)

evaluator_A = LossEvaluator(dataset_A,loss)
result__AA = evaluator_A.evaluate(neuron_A)
print(result__AA)

evaluator_B = LossEvaluator(dataset_B,loss)
result__BA = evaluator_B.evaluate(neuron_A)
print(result__BA)

# 实例属性能否改变？
# 实力属性就类似于一台咖啡机的各种零件，开始的时候需要初始化咖啡机各个零件的型号
# 模型训练就相当于放入各种各样的咖啡豆，根据咖啡机生成的咖啡的味道去调节咖啡机各个零件的型号，以便生成味道最好的咖啡