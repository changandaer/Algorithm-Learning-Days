"""DAY21模型实践：实现RegressionDataset，按下标取输入和标签，再把输入送给已有神经元；准确接口与结果见课程。"""

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

        return len(xs)

    def get_item(self,index):

        return (self.xs[index],self.ys[index])

neuron = SingleNeuron(2,1)

regression = RegressionDataset([-1, 0, 1, 2],[-1, 1, 3, 5])
assert regression.get_item(0) == (-1, -1)
assert regression.get_item(2) == (1, 3)
assert regression.get_item(3) == (2, 5)
assert regression.get_item(0) == (-1, -1)

        
for index in range(len(regression.xs)):

    input = regression.xs[index]
    predict = neuron.forward(input)
    target = regression.ys[index]
    print(input,predict,target)




