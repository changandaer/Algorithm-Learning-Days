"""DAY22模型实践：复用修正后的数据集和ReLU神经元，新增LinearNeuron，比较同一输入的两种预测；接口见课程。"""

class SingleNeuron:

    def __init__(self,weight,bias):

        self.weight = weight
        self.bias = bias

    def forward(self,x):

        z = self.weight * x + self.bias

        if z >0:
            return z
        else:
            return 0


class RegressionDataset:

    def __init__(self,xs,ys):

        self.xs = xs
        self.ys = ys

    def size(self):

        return len(self.xs)

    def get_item(self,index):

        return (self.xs[index],self.ys[index])

class LinearNeuron:
    
    def __init__(self, weight, bias):
        self.weight = weight
        self.bias = bias

    def forward(self,x):
        z = self.weight * x + self.bias

        return z

# - train_data：xs=`[-1, 0, 1, 2]`，ys=`[-1, 1, 3, 5]`。
# - check_data：xs=`[3, 4]`，ys=`[7, 9]`
xs = [-1, 0, 1, 2]
ys = [-1, 1, 3, 5]
train_data = RegressionDataset(xs,ys)
size = train_data.size()
print(size)
print(train_data.get_item(0))

xs=[3, 4]
ys=[7, 9]
check_data = RegressionDataset(xs,ys)
size = check_data.size()
print(size)
print(check_data.get_item(1))

linear_neuron = LinearNeuron(2,1)
relu_neuron = SingleNeuron(2,1)

print(train_data.xs)
print(len(train_data.xs))

for index in range(len(train_data.xs)):

    input = train_data.xs[index]
    linear_predict = linear_neuron.forward(input)
    relu_predict = relu_neuron.forward(input)
    target = train_data.ys[index]
    print(input,target,linear_predict,relu_predict)