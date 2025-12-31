# app/ai/neural_network.py

class NeuralNetwork:
    """A vectorized Multi-Layer Perceptron (MLP) for parallel agent inference.
    
    This class performs the forward pass for the entire population of agents 
    simultaneously, utilizing matrix multiplication for high performance on 
    either CPU or GPU backends.

    Attributes:
        xp (module): The numerical library (numpy or cupy) for matrix operations.
        all_w1 (xp.ndarray): Weights for the input to first hidden layer.
        all_w2 (xp.ndarray): Weights for the first to second hidden layer.
        all_w3 (xp.ndarray): Weights for the second hidden layer to output.
    """
    
    def __init__(self, w1, w2, w3, device="cpu"):
        """Initializes the network with population weights and selects the backend.

        Args:
            w1, w2, w3 (xp.ndarray): Initial weight matrices for the population.
            device (str): Computation device, "cpu" for NumPy or "cuda" for CuPy.
        """
        if device == "cpu":
            import numpy as np
            self.xp = np
        else:
            import cupy as cp
            self.xp = cp

        self.all_w1 = w1
        self.all_w2 = w2
        self.all_w3 = w3
    
  
    def forward(self, x, idx_alive):
        """Performs a vectorized forward pass for all active agents.
        
        This method applies tanh activation functions on hidden layers and a 
        sigmoid activation on the output layer to determine the agent's action.

        Args:
            x (xp.ndarray): Input features for the alive agents.
            idx_alive (xp.ndarray): Indices of the agents currently active in the simulation.

        Returns:
            xp.ndarray: A boolean array where True indicates a jump action (> 0.5).
        """
        x = x[:, self.xp.newaxis, :]
        w1 = self.all_w1[idx_alive]
        w2 = self.all_w2[idx_alive] 
        w3 = self.all_w3[idx_alive] 
        
        z1 = self.xp.matmul(x, w1)
        a1 = self.xp.tanh(z1)
        
        z2 = self.xp.matmul(a1, w2)
        a2 = self.xp.tanh(z2)
        
        z3 = self.xp.matmul(a2, w3)
        output = 1 / (1 + self.xp.exp(-z3))
        
        return output.ravel() > 0.5