import torch
import torch.nn.functional as F
from torch_geometric.data import Data
import networkx as nx
import numpy as np
from sklearn.base import ClassifierMixin
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib  # type: ignore
from .gcn_encoder import GCNEncoder2
from typing import Optional


class NodeClassificationGNN:
    def __init__(self):
        self.__data: Data = None
        self.graph: Optional[nx.Graph] = None
        self.features: Optional[list[tuple[int, list[float]]]] = None
        self.labels: Optional[list[tuple[int, int]]] = None
        self.encoder: Optional[GCNEncoder2] = None
        self.classifier: Optional[ClassifierMixin] = None

    def create_dataset(self, graph: nx.Graph, features: list[tuple[int, list[float]]], labels: list[tuple[int, int]]):
        x = torch.stack(
            [torch.tensor(features[i][1], dtype=torch.float)
             for i in graph.nodes()]
        )
        x = F.normalize(x, p=2, dim=1)

        y = torch.tensor(
            [labels[i][1] for i in graph.nodes()], dtype=torch.long
        )

        edge_index = torch.tensor(
            list(graph.edges), dtype=torch.long).t().contiguous()

        self.__data = Data(x=x, y=y, edge_index=edge_index)

        print(self.__data)

    def train(self, hidden_dim=32, epochs=500, lr=0.01):
        self.encoder = GCNEncoder2(self.__data.num_features, hidden_dim)
        optimizer = torch.optim.Adam(self.encoder.parameters(), lr=lr)

        for epoch in range(1, epochs + 1):
            self.encoder.train()
            optimizer.zero_grad()

            z = self.encoder(self.__data.x, self.__data.edge_index)
            out = F.log_softmax(z, dim=1)

            loss = F.nll_loss(out, self.__data.y)
            loss.backward()
            optimizer.step()

            if epoch % 50 == 0 or epoch == 1:
                print(f"Epoch {epoch}, Loss: {loss.item():.4f}")

        # Gera embeddings finais
        self.encoder.eval()
        with torch.no_grad():
            z = self.encoder(self.__data.x, self.__data.edge_index)

        # Classificação supervisionada (fora do grafo)
        X = z.detach().cpu().numpy()
        y = self.__data.y.cpu().numpy()

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        self.classifier = RandomForestClassifier(n_estimators=100)
        self.classifier.fit(X_train, y_train)
        y_pred = self.classifier.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        print(f"Classificação Final - Acurácia: {acc:.4f}")
        print(classification_report(y_test, y_pred))

    def save(self):
        if self.encoder is None:
            raise Exception(
                'You must train the model before saving it')
        torch.save(self.encoder.state_dict(
        ), 'apps/mobsinet/simulator/gnn/pth/node_classification_gnn.pth')
        joblib.dump(self.classifier,
                    'apps/mobsinet/simulator/gnn/pth/node_classifier.pkl')

    def load(self, in_channels=11, hidden_channels=32):
        self.encoder = GCNEncoder2(in_channels, hidden_channels)
        self.encoder.load_state_dict(torch.load(
            'apps/mobsinet/simulator/gnn/pth/node_classification_gnn.pth'))
        self.encoder.eval()
        self.classifier = joblib.load(
            'apps/mobsinet/simulator/gnn/pth/node_classifier.pkl')

    def predict_node_labels(self, graph: nx.Graph, features: list[tuple[int, list[float]]]):
        x = torch.stack(
            [torch.tensor(features[i][1], dtype=torch.float)
             for i in graph.nodes()]
        )
        x = F.normalize(x, p=2, dim=1)

        edge_index = torch.tensor(
            list(graph.edges), dtype=torch.long).t().contiguous()

        data = Data(x=x, edge_index=edge_index)

        if self.encoder is None or self.classifier is None:
            raise Exception(
                'You must train the model before making predictions')
        self.encoder.eval()
        with torch.no_grad():
            z = self.encoder(data.x, data.edge_index)

        X_new = z.detach().cpu().numpy()

        preds = self.classifier.predict(X_new)

        return list(zip(graph.nodes(), preds))
