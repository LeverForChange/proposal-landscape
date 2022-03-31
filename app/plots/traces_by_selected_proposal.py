import plotly.graph_objects as go

from .traces_by_competition import create_node_traces_by_competition
from .traces_by_topic import create_node_traces_by_topic
from ..const import embeddings, df, knn_indices

def create_edge_trace(source, indices):
  """ Creates the links between a selected proposal and its neighbors """
  edges_x, edges_y, edges_z = [], [], []
  source = source.to_dict(orient='list')
  x0, y0, z0 = source['nodes_x'][0], source['nodes_y'][0], source['nodes_z'][0]

  for target in indices[1:]:
    x1, y1, z1 = embeddings[target][0], embeddings[target][1], embeddings[target][2]
    edges_x += [x0, x1, None]
    edges_y += [y0, y1, None]
    edges_z += [z0, z1, None]

  edge_trace = go.Scatter3d(
    x=edges_x, y=edges_y, z=edges_z,
    hoverinfo='none',
    name='links',
    mode='lines',
    opacity=0.8,
    showlegend=False,
    line=dict(
      color='white',
      width=1
      )
    )

  return edge_trace

def create_selected_proposal_traces(selected_proposal, by='competition'):
  """
  When a proposal is selected:
    1) Create a single-point scatter trace with the selected point highlighted as white
    2) Create a set of highlighted competition traces, one for each neighbor of the selected point
    3) Create a set of link traces to highlight the connections
  """
  traces = []

  if isinstance(selected_proposal, int):
    source = df.iloc[[selected_proposal]]
    index = selected_proposal

  elif isinstance(selected_proposal, str):
    source = df[df['Project Title'] == selected_proposal]
    index = list(source.index)[0]

  line = dict(width=15, color='white')

  source_trace = go.Scatter3d(
    x=source['nodes_x'], y=source['nodes_y'], z=source['nodes_z'],
    mode='markers',
    hovertext=source['Project Title'],
    hoverinfo='text',
    customdata=[index],
    name='Selected Proposal',
    marker=dict(size=7, color='white', opacity=1),
    line=line,
    showlegend=False
  )
  traces.append(source_trace)

  neighbors = df.iloc[knn_indices[index]].iloc[1:]
  if by == 'competition':
    traces.extend(
      create_node_traces_by_competition(data=neighbors, opacity=0.9, line=line, showlegend=False)
      )
  elif by == 'topic':
    traces.extend(
      create_node_traces_by_topic(data=neighbors, opacity=0.9, line=line, showlegend=False)
      )
  traces.append(
    create_edge_trace(source, knn_indices[index])
    )
  return traces