import pygame as pg
import numpy as np
from config import *

class Utils:

    def __init__(self):
        pass

    def draw_network(self, screen, bird, start_x, start_y, inputs):
        weights = [bird.brain.w1, bird.brain.w2, bird.brain.w3]
        layer_sizes = [w.shape[0] for w in weights] + [weights[-1].shape[1]]
        
        node_radius = 8
        layer_gap = 100
        node_gap = 35
        
        nodes = []
        for i, size in enumerate(layer_sizes):
            layer_nodes = [
                (start_x + i * layer_gap, start_y + (j - size/2) * node_gap)
                for j in range(size)
            ]
            nodes.append(layer_nodes)

        # Edges Draw
        # We Iterate for each pair of layers and weights
        for l in range(len(weights)):
            current_w_matrix = weights[l]
            for i, start_node in enumerate(nodes[l]):
                for j, end_node in enumerate(nodes[l+1]):
                    weight = current_w_matrix[i][j]
                    
                    # Visibility Filter
                    if abs(weight) > 0.1: 
                        color = (0, 255, 0) if weight > 0 else (255, 0, 0)
                        width = max(1, int(abs(weight) * 2))
                        pg.draw.line(screen, color, start_node, end_node, width)

        # Nodes Draw
        for i, layer in enumerate(nodes):
            for j, node_pos in enumerate(layer):
                node_color = (40, 40, 40)
                if i == 0 and j < len(inputs): # Sensores
                    val = max(0, min(255, int(abs(inputs[j]) * 255)))
                    node_color = (val, val, 255)
                elif i == len(nodes) - 1: # Salida
                    node_color = (255, 255, 0) if bird.speed_y < 0 else (40, 40, 40)
                
                pg.draw.circle(screen, node_color, node_pos, node_radius)
                pg.draw.circle(screen, (200, 200, 200), node_pos, node_radius, 1)

    def draw_debug_line(self, screen_alpha, start_pos, end_pos, dash_length=10, color=WHITE):
        """Dibuja una línea a trazos desde el pájaro hasta el objetivo con una X final."""
        x1, y1 = start_pos
        x2, y2 = end_pos
        
        # 1. Calcular la distancia y el ángulo
        dl = dash_length
        dx = x2 - x1
        dy = y2 - y1
        distance = np.hypot(dx, dy)
        
        if distance == 0: return

        # Calcular cuántos trozos caben
        num_dashes = int(distance / dl)
        
        # 2. Dibujar los trazos (usamos un bucle simple)
        for i in range(0, num_dashes, 2):
            start = (x1 + (dx * i / num_dashes), y1 + (dy * i / num_dashes))
            end = (x1 + (dx * (i + 1) / num_dashes), y1 + (dy * (i + 1) / num_dashes))
            pg.draw.line(screen_alpha, color, start, end, 2)

        # 3. Dibujar la "X" en el destino
        size = 8
        # Línea 1 de la X (\)
        pg.draw.line(screen_alpha, color, (x2 - size, y2 - size), (x2 + size, y2 + size), 2)
        # Línea 2 de la X (/)
        pg.draw.line(screen_alpha, color, (x2 - size, y2 + size), (x2 + size, y2 - size), 2)