import plotly.graph_objects as go

from ..const import topics, knn_indices, df, TOPIC_COLORS

def create_node_traces_by_outlier_score(**kwargs):
  """ Creates a trace including only outlier proposals """
  traces = []
  node_df = kwargs.get('data', df)
  node_df = node_df[
    node_df['Outlier Score'] > kwargs.get('outlier_threshold', 0.6)
    ]

  for label, topic in topics.items():
    data = node_df[node_df.Topic == label]

    node_trace = go.Scatter3d(
      x=data['nodes_x'],
      y=data['nodes_y'],
      z=data['nodes_z'],
      mode='markers',
      line=kwargs.get('line', dict(color='rgba(0,0,0,0)')),
      hovertext=data['Project Title'],
      hoverinfo='text',
      name=', '.join(topic['words'][:2]) if label >= 0 else 'No Topic',
      marker=dict(
        size=node_df['Outlier Score'] ** node_df['Outlier Score'] * 10,
        sizeref=1,
        sizemin=7,
        color=TOPIC_COLORS[label] if label >= 0 else '#999999',
        opacity=kwargs.get('opacity', 0)
        ),
      customdata=list(data.index),
      showlegend=kwargs.get('showlegend', bool(label < 0)),
      )

    traces.append(node_trace)

  return traces