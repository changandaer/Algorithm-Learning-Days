# DAY35：复用正确模型部件，按验证集选候选，最后评价独立测试集；要求见同目录课程。

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

def batch_gradient(data,model):
    g_w,g_b = 0,0
    for i in range(data.size()):
        single_xs,single_ys = data.get_item(i)
        error = model.forward(single_xs) - single_ys
        g_w += error * single_xs
        g_b += error * 1

    mean_g_w = g_w/data.size()
    mean_g_b = g_b/data.size()
    return mean_g_w,mean_g_b

class Trainer:
    def __init__(self,model,data,loss,optimizer):
        self.model = model
        self.data = data
        self.loss = loss
        self.optimizer = optimizer
        self.evaluator = LossEvaluator(self.data,self.loss)

    def train(self):
        old_loss = self.evaluator.evaluate(self.model)
        
        g_w,g_b = batch_gradient(self.data,self.model)
        self.optimizer.step(self.model,g_w,g_b)

        new_loss = self.evaluator.evaluate(self.model)

        return new_loss
    
    def fit(self,epochs):
        loss_list = []
        loss_list.append(self.evaluator.evaluate(self.model))
        for i in range(epochs):
            loss_list.append(self.train())
        return loss_list


loss = SquaredLoss()

data_train = RegressionDataset([-1,0,1,2],[-1,1,3,5])
data_val = RegressionDataset([-2,3],[-3,7])
data_test = RegressionDataset([4,5],[9,11])

models = {
    0 : LinearNeuron(0,0),
    0.1 : LinearNeuron(0,0)
}

optimizers = {
    0 : GradientDescent(0),
    0.1 : GradientDescent(0.1)
}

val_evaluator = LossEvaluator(data_val,loss)
val_losses = {}

for learning_rate,model in models.items():
    trainer = Trainer(model,data_train,loss,optimizers[learning_rate])
    loss_list = trainer.fit(100)
    print(f"学习率为{learning_rate}时初始损失为：{loss_list[0]}，训练100轮后的损失为：{loss_list[-1]}")

    w_before,b_before = model.weight,model.bias

    val_loss = val_evaluator.evaluate(model) 
    val_losses[learning_rate] = val_loss

    w_aftre,b_after = model.weight,model.bias
    assert w_aftre == w_before and b_after == b_before
    print(f"学习率为{learning_rate}的验证集损失为：{val_loss}")

best_rate = min(val_losses, key=val_losses.get)
best_model = models[best_rate]
print(f"\n选出的最佳学习率是: {best_rate} (验证损失最小)")

# 4. 最后只报告选中模型的测试损失与两项预测（输入 4 和 5）
test_evaluator = LossEvaluator(data_test, loss)
test_loss = test_evaluator.evaluate(best_model)

pred_4 = best_model.forward(4)
pred_5 = best_model.forward(5)

print("\n--- 最终独立测试结果 ---")
print(f"测试集损失: {test_loss}")
print(f"输入 4 的预测值: {pred_4} (目标接近 9)")
print(f"输入 5 的预测值: {pred_5} (目标接近 11)")



