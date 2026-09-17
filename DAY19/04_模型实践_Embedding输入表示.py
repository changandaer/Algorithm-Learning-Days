"""DAY19模型实践：实现EmbeddingTable，把类别转换成输入向量；模型短练及接口见课程，三步和新实现自己完成。"""

# class SingleNeuron:

#     def __init__(self,weight,bias):

#         self.weight = weight
#         self.bias = bias
    
#     def forward(self,x):

#         z = self.weight * x + self.bias
#         if z > 0:
#             return z
#         else:
#             return 0

#     def fit(self,xs,ys,candidate_weights):
        
#         for candidate_weight in candidate_weights:

#             train_modle = SingleNeuron(candidate_weight,self.bias)
#             ys_hat = []

#             for x_s in xs:

#                 ys_hat.append(train_modle.forward(x_s))
            
#             if ys_hat == ys:

#                 self.weight = candidate_weight

#                 return candidate_weight

# neuron_a = SingleNeuron(0, 1)
# neuron_b = SingleNeuron(0, 0)
# xs = [0, 1, 2]
# ys = [1, 3, 5]
# candidates = [1, 2, 3]

# assert neuron_a.fit(xs, ys, candidates) == 2
# assert neuron_a.weight == 2
# assert neuron_a.bias == 1
# assert neuron_a.forward(3) == 7

# assert neuron_b.fit([1, 2], [3, 6], candidates) == 3
# assert neuron_b.forward(3) == 9
# assert neuron_a.weight == 2

# assert neuron_a.fit(xs, [1, 2, 3], candidates) == 1
# assert neuron_a.forward(3) == 4
# assert neuron_b.weight == 3
# assert neuron_b.bias == 0

# assert neuron_a.fit([-1, 0, 1], [0, 1, 3], candidates) == 2
# assert neuron_a.forward(-1) == 0
# assert neuron_a.forward(3) == 7
# assert neuron_a.weight == 2
# assert neuron_a.bias == 1
# assert xs == [0, 1, 2]
# assert ys == [1, 3, 5]
# assert candidates == [1, 2, 3]

class EmbeddingTable:

    def __init__(self,vectors):
        self.vectors = vectors

    def forward(self, token):

        if token in self.vectors:
            return self.vectors[token]
    
    def encode(self, tokens):

        encode_vectors = []
        for encode_token in tokens:
            if encode_token in self.vectors:
                encode_vectors.append(self.vectors[encode_token]) 
        
        return encode_vectors






embeddingtable_A = EmbeddingTable({"猫": [1.0, 0.5], "狗": [0.75, 0.5], "车": [0.0, 1.0]})
vector = embeddingtable_A.forward("狗")
encode_vectors = embeddingtable_A.encode(["车", "猫", "车"])
print(vector)
print(encode_vectors)

assert embeddingtable_A.encode([]) == []
assert embeddingtable_A.encode(["猫"]) == [[1.0, 0.5]]

embeddingtable_B = EmbeddingTable({"猫": [-1.0, 0.0], "狗": [0.0, 0.0], "车": [1.0, 1.0]})
assert embeddingtable_B.forward("猫") == [-1.0, 0.0]
assert embeddingtable_B.encode(["猫", "车"]) == [[-1.0, 0.0], [1.0, 1.0]]
assert embeddingtable_A.forward("猫") == [1.0, 0.5]
