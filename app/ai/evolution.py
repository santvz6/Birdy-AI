# app/ai/evolution.py

import re

from config import *
from .neural_network import NeuralNetwork
from pathlib import Path

class Evolution:
    """Manages the genetic algorithm logic for neural network populations.

    This class handles the selection, crossover, and mutation of weights, 
    supporting both CPU (NumPy) and GPU (CuPy) backends for high-performance 
    matrix operations.

    Attributes:
        xp (module): The numerical library module (numpy or cupy) being used.
        savez_path (Path): Directory where the generation weights are stored.
        generation (int): Current evolution cycle count.
        pop_size (int): Total number of individuals in the population.
        w1, w2, w3 (xp.ndarray): Matrices containing weights for all layers and individuals.
        brain (NeuralNetwork): The network instance used for vectorized forward passes.
    """

    def __init__(self, pop_size: int, device="cpu", folder=None, gen=None):
        """Initializes the evolution engine with a population and hardware backend.

        Args:
            pop_size (int): Number of neural networks to evolve.
            device (str): Hardware target, either "cpu" or "cuda" (for cupy).
            folder (str, optional): Specific run folder to load weights from.
            gen (int, optional): Specific generation number to load.
        """
        if device == "cpu":
            import numpy as np
            self.xp = np
        else:
            import cupy as cp
            self.xp = cp

        self.savez_path = RUN_DIR / "weights"
        self.savez_path.mkdir(parents=True, exist_ok=True)
        self.pop_size = pop_size

        # Load and Initialize
        best_weights, self.generation = load_best_weights(folder, gen)

        if best_weights:
            w1_single = self.xp.asarray(best_weights[0])
            w2_single = self.xp.asarray(best_weights[1])
            w3_single = self.xp.asarray(best_weights[2])
            
            # Reproduction and Mutation
            self.w1 = w1_single + self.xp.random.randn(pop_size, 9, 10) * 0.1
            self.w2 = w2_single + self.xp.random.randn(pop_size, 10, 6) * 0.1
            self.w3 = w3_single + self.xp.random.randn(pop_size, 6, 1) * 0.1
            
            # Elitism: The best bird do not change
            self.w1[0], self.w2[0], self.w3[0] = w1_single, w2_single, w3_single
        else:
            self.w1 = self.xp.random.randn(pop_size, 9, 10)
            self.w2 = self.xp.random.randn(pop_size, 10, 6)
            self.w3 = self.xp.random.randn(pop_size, 6, 1)

        # Collective Brain
        self.brain = NeuralNetwork(self.w1, self.w2, self.w3, device=device)

    def restart_generation(self, fitness_array):
        """Performs natural selection and generates the next population of weights.
        
        This method executes elitism by preserving the top individuals, selects parents 
        randomly from the top performers, and applies vectorized Gaussian mutation.

        Args:
            fitness_array (xp.ndarray): An array containing the fitness scores for all individuals.
        """

        # Top 5 fitness indexes
        top_idxs = self.xp.argsort(fitness_array)[::-1][:5]
        best_idx = top_idxs[0]

        # Save
        self.xp.savez(file=self.savez_path / f"gen_{self.generation}.npz", 
                 w1=self.w1[best_idx], w2=self.w2[best_idx], w3=self.w3[best_idx])

        # New Population - New Weights
        new_w1 = self.xp.empty_like(self.w1)
        new_w2 = self.xp.empty_like(self.w2)
        new_w3 = self.xp.empty_like(self.w3)

        # Elitism: Keep 2 best scores without changes
        for i in range(2):
            idx = top_idxs[i]
            new_w1[i], new_w2[i], new_w3[i] = self.w1[idx], self.w2[idx], self.w3[idx]

        # Reproduction and Mutation (Vectorizated)
        # Choose random parents of the Top 5 for the reproduction
        parent_indices = self.xp.random.choice(top_idxs, size=self.pop_size - 2)
        
        # Reproduction and Mutation
        new_w1[2:] = self.w1[parent_indices] + self.xp.random.randn(self.pop_size - 2, 9, 10) * 0.1
        new_w2[2:] = self.w2[parent_indices] + self.xp.random.randn(self.pop_size - 2, 10, 6) * 0.1
        new_w3[2:] = self.w3[parent_indices] + self.xp.random.randn(self.pop_size - 2, 6, 1) * 0.1

        # Update Brain 
        self.w1, self.w2, self.w3 = new_w1, new_w2, new_w3
        self.brain.all_w1 = self.w1
        self.brain.all_w2 = self.w2
        self.brain.all_w3 = self.w3
        
        self.generation += 1
    


def load_best_weights(folder, gen):
    """Searches and loads the best weight matrices from a specific run or the latest one.

    Args:
        folder (str): Name of the data directory folder.
        gen (int): Generation file number to target.

    Returns:
        tuple: (w1, w2, w3) as numpy arrays if found, else None.
    """
    import numpy as np
    if not DATA_DIR.exists(): return None
    
    target = None
    if folder and gen:
        f = DATA_DIR / folder / "weights" / f"gen_{gen}.npz"
        if f.exists(): target = f
    else:
        runs = sorted([d for d in DATA_DIR.iterdir() if d.is_dir()])
        if runs:
            idx = len(runs)
            files = []
            while not files and idx > 0:
                latest_run = runs[idx-1]
                files = list(latest_run.glob("weights/gen_*.npz"))
                if files:
                    target = max(files, key=lambda p: int(re.search(r'\d+', p.name).group()))
                else:
                    idx -= 1
    if target:
        generation = int(re.search(r'\d+', target.name).group())
        data = np.load(target)
        logger.debug(f"Evolution(): loading best_weights... | target: {target}")
        return (data["w1"], data["w2"], data["w3"]), generation
    return None, 1