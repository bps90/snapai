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

    # Gerar posições dos nós em 3D
    pos = nx.spring_layout(G, dim=3)

    # Preparar as arestas para Plotly
    edge_x = []
    edge_y = []
    edge_z = []
    for edge in G.edges():
        x0, y0, z0 = pos[edge[0]]
        x1, y1, z1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)
        edge_z.append(z0)
        edge_z.append(z1)
        edge_z.append(None)

    edge_trace = go.Scatter3d(
        x=edge_x, y=edge_y, z=edge_z,
        line=dict(width=2, color='blue'),
        hoverinfo='none',
        mode='lines'
    )

    # Preparar os nós para Plotly
    node_x = []
    node_y = []
    node_z = []
    for node in G.nodes():
        x, y, z = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_z.append(z)

    node_trace = go.Scatter3d(
        x=node_x, y=node_y, z=node_z,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            size=10,
            color='orange',
            opacity=0.8
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
                       title='3D Network graph made with Python',
                       titlefont_size=16,
                       showlegend=False,
                       hovermode='closest',
                       margin=dict(b=0, l=0, r=0, t=0),
                       annotations=[dict(
                           text="3D Network Graph using NetworkX and Plotly",
                           showarrow=False,
                           xref="paper", yref="paper"
                       )],
                       scene=dict(
                            xaxis=dict(range=[0, 500], title='X Axis'),
                            yaxis=dict(range=[0, 500], title='Y Axis'),
                            zaxis=dict(range=[0, 500], title='Z Axis')
                        )
                   )
    )

    graph_div = fig.to_html(full_html=False)

    return graph_div


def update_graph_back():
    # temporary
    config = simConfiguration.Configuration()

    # Função para gerar e retornar o gráfico atualizado
    G = generate_graph()

    # Gerar posições dos nós
    pos = nx.spring_layout(G, dim=config.dimenssions)

    # Preparar as arestas para Plotly
    edge_x = []
    edge_y = []
    edge_z = []
    for edge in G.edges():
        x0, y0, z0 = pos[edge[0]]
        x1, y1, z1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)
        edge_z.append(z0)
        edge_z.append(z1)
        edge_z.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y, z=edge_z,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines'
    )

    # Preparar os nós para Plotly
    node_x = []
    node_y = []
    node_z = []
    for node in G.nodes():
        x, y, z = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_z.append(z)

    node_trace = go.Scatter3d(
        x=node_x, y=node_y, z=node_z,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            size=10,
            color='orange',
            opacity=0.8
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
                        title='3D Network graph made with Python',
                        titlefont_size=16,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=0, l=0, r=0, t=0),
                        annotations=[dict(
                            text="3D Network Graph using NetworkX and Plotly",
                            showarrow=False,
                            xref="paper", yref="paper"
                        )],
                        #xaxis=dict(showgrid=False, zeroline=False, range=[0, config.dimX]),# Limita o eixo X de 0 a max_x
                        #yaxis=dict(showgrid=False, zeroline=False, range=[0, config.dimY]), # Limita o eixo Y de 0 a max_y
                        #zaxis=dict(showgrid=False, zeroline=False, range=[0, config.dimZ]) # Limita o eixo Y de 0 a max_y
                   )
    )

    graph_div = fig.to_html(full_html=False)

    return graph_div