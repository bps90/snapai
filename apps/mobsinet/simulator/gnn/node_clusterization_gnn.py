from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
import torch
import torch.nn.functional as F
import networkx as nx
from torch_geometric.data import Data
from .gcn_encoder import GCNEncoder


class NodeClusterizationGNN:
    def __init__(self):
        self.encoder = None
        self.data = None
        self.embeddings = None

    def create_dataset(self, graph: nx.Graph, features: list[tuple[int, list[float]]]):
        x = torch.stack([
            torch.tensor(features[i][1], dtype=torch.float) for i in graph.nodes()
        ])
        x = F.normalize(x, p=2, dim=1)

        edge_index = torch.tensor(
            list(graph.edges), dtype=torch.long).t().contiguous()
        self.data = Data(x=x, edge_index=edge_index)

    def train_encoder(self, in_channels, hidden_channels=32):
        self.encoder = GCNEncoder(in_channels, hidden_channels)
        self.encoder.eval()
        with torch.no_grad():
            self.embeddings = self.encoder(self.data.x, self.data.edge_index)

    def cluster_nodes(self, n_clusters=2):
        if self.embeddings is None:
            raise ValueError(
                "Embeddings not computed. Call train_encoder first.")

        kmeans = KMeans(n_clusters=n_clusters)
        clusters = kmeans.fit_predict(self.embeddings.cpu().numpy())

        return clusters


class NodeClusterizationDBSCAN:
    def __init__(self):
        self.encoder = None
        self.data = None
        self.embeddings = None

    def create_dataset(self, graph: nx.Graph, features: list[tuple[int, list[float]]]):
        x = torch.stack([
            torch.tensor(features[i][1], dtype=torch.float) for i in graph.nodes()
        ])
        x = F.normalize(x, p=2, dim=1)

        edge_index = torch.tensor(
            list(graph.edges), dtype=torch.long).t().contiguous()
        self.data = Data(x=x, edge_index=edge_index)

    def train_encoder(self, in_channels, hidden_channels=32):
        self.encoder = GCNEncoder(in_channels, hidden_channels)
        self.encoder.eval()
        with torch.no_grad():
            self.embeddings = self.encoder(self.data.x, self.data.edge_index)

    def cluster_nodes(self, eps=0.5, min_samples=5):
        if self.embeddings is None:
            raise ValueError(
                "Embeddings not computed. Call train_encoder first.")

        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        clusters = dbscan.fit_predict(self.embeddings.cpu().numpy())

        return clusters
