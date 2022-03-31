import plotly.graph_objects as go

from ..const import topics, knn_indices, df, TOPIC_COLORS

def create_node_traces_by_topic(**kwargs):
  """ Creates a set of scatter traces, one for each HDBSCAN topic """
  traces = []
  node_df = kwargs.get('data', df)

  for label, topic in topics.items():
    data = node_df[node_df.Topic == label]

    node_trace = go.Scatter3d(
      x=data['nodes_x'], y=data['nodes_y'], z=data['nodes_z'],
      mode='markers',
      line=kwargs.get('line', dict(color='rgba(0,0,0,0)')),
      hovertext=data['Project Title'], hoverinfo='text',
      name=', '.join(topic['words'][:2]) if label >= 0 else 'No Topic',
      marker=dict(
        size=[len(knn_indices[i]) / 4 for i, v in data.iterrows()],
        sizeref=0.85,
        sizemin=7,
        color=TOPIC_COLORS[label] if label >= 0 else '#999999',
        opacity=kwargs.get('opacity', 0)
        ),
      customdata=list(data.index),
      showlegend=kwargs.get('showlegend', bool(label < 0)),
      )

    traces.append(node_trace)

  return traces

def create_topic_label_trace():
  """ Creates a trace with text labels, one for each topic """
  topic_values = list(topics.values())[1:]
  x = [topic['exemplar'][0] for topic in topic_values]
  y = [topic['exemplar'][1] for topic in topic_values]
  z = [topic['exemplar'][2] for topic in topic_values]
  text = [', '.join(topic['words'][:2]) for topic in topic_values]

  trace = go.Scatter3d(
    x=x, y=y, z=z,
    mode='text',
    hoverinfo='none',
    text=text,
    textfont=dict(color='#bbb'),
    showlegend=True,
    name='Topic Labels'
  )
  return trace