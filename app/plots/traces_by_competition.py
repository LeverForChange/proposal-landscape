import plotly.graph_objects as go

from ..const import df, knn_indices, COMPETITION_NAMES, COMPETITION_COLORS

def create_node_traces_by_competition(**kwargs):
  """ Creates a set of scatter traces, one for each competition """
  traces = []
  node_df = kwargs.get('data', df)
  competitions = node_df['Competition Domain'].unique()

  for comp in competitions:
    data = node_df[node_df['Competition Domain'] == comp]

    node_trace = go.Scatter3d(
      x=data['nodes_x'], y=data['nodes_y'], z=data['nodes_z'],
      mode='markers',
      line=kwargs.get('line', dict(color='rgba(0,0,0,0)')),
      hovertext=data['Project Title'], hoverinfo='text',
      name=COMPETITION_NAMES[comp],
      marker=dict(
        size=[len(knn_indices[i]) / 4 for i, v in data.iterrows()],
        sizeref=0.85,
        sizemin=7,
        color=COMPETITION_COLORS[comp],
        opacity=kwargs.get('opacity', 0)
        ),
      customdata=list(data.index),
      showlegend=kwargs.get('showlegend', True),
      )

    traces.append(node_trace)

  return traces