import streamlit as st
import pandas as pd
import networkx as nx
import plotly.graph_objs as go
import json

# Load data (CSV or JSON clusters)
def load_clusters_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def make_graph_from_clusters(clusters):
    G = nx.Graph()
    for i, group in enumerate(clusters):
        ids = [issue['id'] for issue in group]
        for id in ids:
            G.add_node(id, summary=group[ids.index(id)]['summary'])
        for j in range(len(ids)):
            for k in range(j+1, len(ids)):
                G.add_edge(ids[j], ids[k], cluster=i)
    return G

def plotly_graph(G):
    pos = nx.spring_layout(G, k=0.7)
    edge_trace = go.Scatter(
        x=[],
        y=[],
        line=dict(width=1, color='#888'),
        hoverinfo='none',
        mode='lines'
    )

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace['x'] += [x0, x1, None]
        edge_trace['y'] += [y0, y1, None]

    node_trace = go.Scatter(
        x=[], y=[],
        text=[],
        mode='markers+text',
        textposition="bottom center",
        hoverinfo='text',
        marker=dict(
            showscale=False,
            color=[],
            size=18,
            line_width=2
        )
    )

    for node in G.nodes():
        x, y = pos[node]
        node_trace['x'].append(x)
        node_trace['y'].append(y)
        node_trace['text'].append(f"{node}: {G.nodes[node].get('summary', '')}")

    fig = go.Figure(data=[edge_trace, node_trace],
        layout=go.Layout(
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20,l=5,r=5,t=40),
            xaxis=dict(showgrid=False, zeroline=False),
            yaxis=dict(showgrid=False, zeroline=False)))
    return fig

# Streamlit UI
st.title('Jira Duplicate Clusters Interactive Graph')
clusters = load_clusters_json('clusters.json')
G = make_graph_from_clusters(clusters)
fig = plotly_graph(G)
st.plotly_chart(fig, use_container_width=True)

with st.expander("Show clusters as tables"):
    for i, group in enumerate(clusters):
        st.subheader(f"Cluster {i} ({len(group)} tickets)")
        df = pd.DataFrame(group)
        st.write(df)