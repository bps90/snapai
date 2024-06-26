from django.http import JsonResponse
from django.shortcuts import render
import networkx as nx
import plotly.graph_objects as go

def generate_graph():
    # Função para gerar o grafo (isso pode ser dinâmico conforme necessário)
    G = nx.Graph()
    G.add_edges_from([
        ('A', 'B'),
        ('A', 'C'),
        ('B', 'D'),
        ('C', 'D')
    ])
    return G

def graph_view(request):
    # Renderizar a página inicial com o gráfico
    return render(request, 'graph.html')

def update_graph():
    # Função para gerar e retornar o gráfico atualizado
    G = generate_graph()

    # Gerar posições dos nós
    pos = nx.spring_layout(G)

    # Preparar as arestas para Plotly
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines'
    )

    # Preparar os nós para Plotly
    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
        )
    )

    # Adicionar textos de hover
    node_text = []
    for node, adjacencies in G.adjacency():
        node_text.append(f'{node}<br># of connections: {len(adjacencies)}')
    node_trace.text = node_text

    # Criar a figura
    fig = go.Figure(data=[edge_trace, node_trace],
                   layout=go.Layout(
                       title='Network graph made with Python',
                       titlefont_size=16,
                       showlegend=False,
                       hovermode='closest',
                       margin=dict(b=0, l=0, r=0, t=0),
                       annotations=[dict(
                           text="Network Graph using NetworkX and Plotly",
                           showarrow=False,
                           xref="paper", yref="paper"
                       )],
                       xaxis=dict(showgrid=False, zeroline=False),
                       yaxis=dict(showgrid=False, zeroline=False)
                   )
    )

    graph_div = fig.to_html(full_html=False)

    return graph_div