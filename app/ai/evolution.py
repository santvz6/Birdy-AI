import re
import numpy as np

from config import *
from .neural_network import NeuralNetwork
from pathlib import Path


class Evolution:
    def __init__(self, pop_size:int, folder=None, gen=None):
        self.savez_path = RUN_DIR / "weights"
        self.savez_path.mkdir(parents=True, exist_ok=True)

        self.generation = 1
        self.pop_size = pop_size

        # Best Weights Load
        best_weights = self._load_best_weights(folder, gen)
        if best_weights:
            w1, w2, w3 = best_weights
            
            self.population = []
            self.population.append(NeuralNetwork(weights=(w1, w2, w3)))
            while len(self.population) < self.pop_size:
                self.population.append(NeuralNetwork(weights=(
                    w1 + np.random.randn(9, 10) * 0.1, 
                    w2 + np.random.randn(10, 6) * 0.1,
                    w3 + np.random.randn(6, 1) * 0.1)))
        else:
            logger.debug("Evolution(): loading new weights...")
            self.population = [NeuralNetwork() for _ in range(pop_size)]


    def restart_generation(self):
        # Fitness sort
        self.population.sort(key=lambda x: x.fitness, reverse=True)
        
        new_pop = []
        # Elitism: Keep top 2 without changes
        new_pop.append(NeuralNetwork(weights=(self.population[0].w1, self.population[0].w2, self.population[0].w3)))
        new_pop.append(NeuralNetwork(weights=(self.population[1].w1, self.population[1].w2, self.population[1].w3)))
        # Save Best Weights
        best_nn = self.population[0]
        np.savez(file=self.savez_path / f"gen_{self.generation}.npz", w1=best_nn.w1, w2=best_nn.w2, w3=best_nn.w3)
        logger.debug("Evolution(): savining best weights...")

        # Reproduction
        while len(new_pop) < self.pop_size:
            parent = self.population[np.random.randint(0, 5)] # Top 5
            
            # Weights clone + mutation
            child_w1 = parent.w1 + np.random.randn(9, 10) * 0.1
            child_w2 = parent.w2 + np.random.randn(10, 6) * 0.1
            child_w3 = parent.w3 + np.random.randn(6,  1) * 0.1
            
            new_pop.append(NeuralNetwork(weights=(child_w1, child_w2, child_w3)))

        self.population = new_pop
        self.generation += 1

    

    def _load_best_weights(self, folder, gen):
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
            data = np.load(target)
            logger.debug(f"Evolution(): loading best_weights... | target: {target}")
            return data["w1"], data["w2"], data["w3"]
        return None