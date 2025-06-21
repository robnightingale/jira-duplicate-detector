# Jira Duplicate Issue Detector

Finds duplicate or near-duplicate Jira tickets by comparing summary/description via semantic similarity.

**How it works:**
- Fetches tickets from Jira
- Embeds text meaning using Sentence Transformers
- Groups similar issues using Agglomerative Clustering

# Jira Duplicate Issue Detector

Identifies and groups duplicate or near-duplicate Jira tickets by semantically comparing their summaries and descriptions.  
Supports exporting and **interactive visualization of clusters** via a simple web app.

---

## Features

- **Fetches tickets** from Jira via API
- **Embeds ticket summaries/descriptions** using [Sentence Transformers](https://www.sbert.net/)
- **Clusters similar tickets** automatically
- **Exports clusters** to CSV and JSON for analysis or reporting
- **Visualizes clusters interactively** using [Streamlit](https://streamlit.io)
- **Unit tests** for core logic

---

## Setup

1. **Clone and Install Requirements**

    ```bash
    git clone https://github.com/yourusername/jira-duplicate-detector.git
    cd jira-duplicate-detector
    pip install -r requirements.txt
    ```

2. **(Optional) For interactive web visualization:**

    ```bash
    pip install streamlit plotly pandas networkx
    ```

---

## Usage

### **1. Detect and Export Clusters**

- Edit `main.py` and fill in:
    - `JIRA_BASE` (e.g. `https://yourcompany.atlassian.net`)
    - `JIRA_PROJECT` (e.g. `PROJECTKEY`)
    - `JIRA_TOKEN` (your Jira API token)

- Run the main script:
    ```bash
    python main.py
    ```
    - This fetches tickets, detects clusters, and exports:
        - `clusters.csv` for Excel/Sheets/etc
        - `clusters.json` for programmatic access or web visualization

### **2. Interactive Visualization (Streamlit Web App)**

- After generating `clusters.json`:
    1. Save the supplied `app.py` (see below) into your project folder.
    2. Run:
        ```bash
        streamlit run app.py
        ```
    3. Explore clusters as an interactive graph and see full ticket tables.

---

## app.py

<details>
<summary>Click to expand Streamlit app code example to drop into <code>app.py</code></summary>

```python
import streamlit as st
import pandas as pd
import networkx as nx
import plotly.graph_objs as go
import json

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

</details>

## Usage

1. Install requirements:
    pip install -r requirements.txt

2. Set your Jira credentials and run:
    python main.py

## Testing

    pytest

## Customization

- Adjust the `similarity_threshold` in `main.py` for stricter/looser grouping.

