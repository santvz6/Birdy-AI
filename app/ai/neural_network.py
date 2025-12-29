import numpy as np


class NeuralNetwork:
    """A simple MultiLayerPerceptron."""
    
    def __init__(self, weights=None):
        if weights:
            self.w1, self.w2, self.w3 = weights
        else:
            self.w1 = np.random.randn(9, 10) 
            self.w2 = np.random.randn(10, 6)
            self.w3 = np.random.randn(6, 1)
        
        self.fitness = 0

    def forward(self, x):
        z1 = np.dot(x, self.w1)
        a1 = np.tanh(z1)
        
        z2 = np.dot(a1, self.w2)
        a2 = np.tanh(z2)
        
        z3 = np.dot(a2, self.w3)
        output = 1 / (1 + np.exp(-z3)) 
        
        return output.item() > 0.5 