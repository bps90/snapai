from torch_geometric.data import Data
import networkx as nx
import numpy as np
import torch
import torch.nn.functional as F
from torch_geometric.utils import negative_sampling
from sklearn.metrics import roc_auc_score
from itertools import combinations
from .gcn_encoder import GCNEncoder
from typing import Optional


class LinkPredictionGNN:
    def __init__(self):
        self.__data: Data = None
        self.graph: Optional[nx.Graph | nx.DiGraph] = None
        self.features: Optional[list[tuple[int, list[float]]]] = None
        self.labels: Optional[list[tuple[int, int]]] = None
        self.encoder: Optional[GCNEncoder] = None

    @staticmethod
    def get_features_from_file(file_path: str, have_header: bool = True):
        """Get a list of tuples (id, feature vector) from a file with the following format:
        id, feature1, feature2, ..., featureN
        """
        with open(file_path, 'r') as file:
            lines = [(int(line.strip().split(',')[0]), list(map(float, line.strip().split(',')[1:])))
                     for line in file.readlines()[(1 if have_header else 0):]]

        return lines

    @staticmethod
    def transform_graph_of_objects_to_graph_of_integers(graph: nx.Graph | nx.DiGraph):
        """Transform a graph of objects to a graph of integers"""
        return nx.convert_node_labels_to_integers(graph)

    def create_dataset(self, graph: nx.Graph | nx.DiGraph, features: list[tuple[int, list[float]]], labels: list[tuple[int, int]]):
        x = torch.stack(
            [torch.tensor(features[i][1], dtype=torch.float) for i in graph.nodes()])

        x = F.normalize(x, p=2, dim=1)

        y = torch.tensor(
            [labels[i][1] for i in graph.nodes()], dtype=torch.long)

        edge_index = torch.tensor(
            list(graph.edges), dtype=torch.long).t().contiguous()

        self.__data = Data(x=x, y=y, edge_index=edge_index)

        print(f'Created dataset for Link Prediction GNN: {self.__data}')

    def gen_neg_edge_index(self):
        pos_edge_index = self.__data.edge_index

        neg_edge_index = negative_sampling(
            edge_index=pos_edge_index,
            num_nodes=self.__data.num_nodes,
            num_neg_samples=pos_edge_index.size(1)
        )

        return neg_edge_index

    def decode(self, z, edge_index):
        return (z[edge_index[0]] * z[edge_index[1]]).sum(dim=1)

    def train(self, hidden_dim=32, epochs=10000, lr=0.01):
        self.encoder = GCNEncoder(
            in_channels=self.__data.num_features, hidden_channels=hidden_dim)
        optimizer = torch.optim.Adam(self.encoder.parameters(), lr=lr)

        for epoch in range(1, epochs + 1):
            self.encoder.train()
            optimizer.zero_grad()

            z = self.encoder(self.__data.x, self.__data.edge_index)

            pos_edge_index = self.__data.edge_index
            neg_edge_index = self.gen_neg_edge_index()

            pos_pred = self.decode(z, pos_edge_index)
            neg_pred = self.decode(z, neg_edge_index)

            preds = torch.cat([pos_pred, neg_pred])
            labels = torch.cat([
                torch.ones(pos_pred.size(0)),
                torch.zeros(neg_pred.size(0))
            ])

            loss = F.binary_cross_entropy_with_logits(preds, labels)
            loss.backward()
            optimizer.step()

            # ---- AUC Evaluation ----
            with torch.no_grad():
                probs = torch.sigmoid(preds)
                auc = roc_auc_score(labels.cpu().numpy(), probs.cpu().numpy())

            if epoch % 100 == 0 or epoch == 1:
                print(
                    f'Epoch {epoch}, Loss: {loss.item():.4f}, AUC: {auc:.4f}')

    def save(self):
        if self.encoder is None:
            raise Exception(
                'You must train the model before saving it')
        torch.save(self.encoder.state_dict(),
                   'apps/mobsinet/simulator/gnn/pth/link_prediction_gnn.pth')

    def load(self, in_channels=11, hidden_channels=32):
        self.encoder = GCNEncoder(in_channels, hidden_channels)
        self.encoder.load_state_dict(torch.load(
            'apps/mobsinet/simulator/gnn/pth/link_prediction_gnn.pth'))
        self.encoder.eval()

    def predict_missing_edges(self, top_k=10):
        if self.encoder is None:
            raise Exception(
                'You must train the model before making predictions')
        self.encoder.eval()
        with torch.no_grad():
            z = self.encoder(self.__data.x, self.__data.edge_index)

        # Pares de nós possíveis (excluindo os que já existem no grafo)
        existing_edges = set(map(tuple, self.__data.edge_index.t().tolist()))
        all_possible_edges = combinations(range(self.__data.num_nodes), 2)
        candidate_edges = [
            (u, v) for u, v in all_possible_edges
            if (u, v) not in existing_edges and (v, u) not in existing_edges
        ]

        # Cria edge_index para candidatos
        candidate_edge_index = torch.tensor(
            candidate_edges, dtype=torch.long).t()

        # Faz a predição
        with torch.no_grad():
            scores = torch.sigmoid(self.decode(z, candidate_edge_index))

        # Top-K predições
        topk_indices = torch.topk(scores, top_k).indices
        topk_edges = [candidate_edges[i] for i in topk_indices.tolist()]
        topk_scores = scores[topk_indices].tolist()

        return list(zip(topk_edges, topk_scores))

    def predict_edges_above_threshold_in_new_graph(self, graph: nx.Graph, features: list[tuple[int, list[float]]], threshold=0.96):
        # Transforma grafo para inteiros
        graph = LinkPredictionGNN.transform_graph_of_objects_to_graph_of_integers(
            graph)

        # Cria tensor de features
        x = torch.stack(
            [torch.tensor(features[i][1], dtype=torch.float) for i in graph.nodes()])
        x = F.normalize(x, p=2, dim=1)

        edge_index = torch.tensor(
            list(graph.edges), dtype=torch.long).t().contiguous()

        # Cria novo Data
        new_data = Data(x=x, edge_index=edge_index)

        # Gera embeddings
        if self.encoder is None:
            raise Exception(
                'You must train the model before making predictions')
        self.encoder.eval()
        with torch.no_grad():
            z = self.encoder(new_data.x, new_data.edge_index)

        # Gera pares de nós não conectados
        existing_edges = set(map(tuple, edge_index.t().tolist()))
        all_possible_edges = combinations(range(new_data.num_nodes), 2)
        candidate_edges = [
            (u, v) for u, v in all_possible_edges
            if (u, v) not in existing_edges and (v, u) not in existing_edges
        ]

        if not candidate_edges:
            return []

        candidate_edge_index = torch.tensor(
            candidate_edges, dtype=torch.long).t()

        with torch.no_grad():
            scores = torch.sigmoid(self.decode(z, candidate_edge_index))

        # Filtra pelos que têm score acima do threshold
        result = [
            (candidate_edges[i], scores[i].item())
            for i in range(len(scores))
            if scores[i].item() >= threshold
        ]

        return result
