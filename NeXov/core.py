import random
import pickle
import json
import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict, Counter
from graphviz import Digraph


class MarkovModel:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.result = []

    def build(self, tokens):
        transitions = defaultdict(Counter)
        for a,b in zip(tokens, tokens[1:]):
            transitions[a][b] += 1

        for state, counter in transitions.items():
            total = sum(counter.values())
            for next_state, count in counter.items():
                self.graph.add_edge(state, next_state, weight=count / total)

    def generate(self, current):
        neighbors = list(self.graph.successors(current))
        if not neighbors:
            return
        weights = [self.graph[current][n]['weight'] for n in neighbors]
        current = random.choices(neighbors, weights=weights)[0]
        self.result.append(current)
        return current

    def visualize(self, output_file: str, font):
        dot = Digraph(format="png")
        dot.attr(rankdir="LR")
        dot.attr('graph', fontname=font)
        dot.attr('node', fontname=font, shape='circle', style='filled', fillcolor='lightblue')
        dot.attr('edge', fontname=font)

        node_degrees = {
            node: self.graph.out_degree(node)
            for node in self.graph.nodes()
        }
        max_degree = max(node_degrees.values()) if node_degrees else 1

        for node, degree in node_degrees.items():
            norm = degree / max_degree
            size = 0.8 + 1.2 * norm
            fontsize = 18 + 27 * norm
            dot.node(
                node,
                width=f"{size:.2f}",
                height=f"{size:.2f}",
                fontsize=f"{fontsize:.1f}"
            )

        edge_weights = [data['weight'] for _, _, data in self.graph.edges(data=True)]
        if not edge_weights:
            edge_weights = [1.0]
        min_w, max_w = min(edge_weights), max(edge_weights)

        def weight_to_color(w):
            norm = (w - min_w) / (max_w - min_w + 1e-9)
            r, g, b, _ = plt.cm.coolwarm(norm)
            return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"

        for u, v, data in self.graph.edges(data=True):
            weight = data.get("weight", 0)
            color = weight_to_color(weight)
            label = f"{weight:.2f}"
            dot.edge(u, v, label=label, color=color)

        output_path = dot.render(output_file, cleanup=True)
        print(f"[+] The model visualization was saved to {output_path}")

    def save_pickle(self, filepath):
        with open(filepath, 'wb') as f:
            pickle.dump(self.graph, f)

    def load_pickle(self, filepath):
        with open(filepath, 'rb') as f:
            self.graph = pickle.load(f)

    def save_json(self, filepath):
        data = nx.readwrite.json_graph.node_link_data(self.graph, edges="edges")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_json(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.graph = nx.readwrite.json_graph.node_link_graph(data, edges="edges")
