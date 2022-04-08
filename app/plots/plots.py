import plotly.graph_objects as go

from .traces_by_competition import create_node_traces_by_competition
from .traces_by_topic import create_node_traces_by_topic, create_topic_label_trace
from .traces_by_selected_proposal import create_selected_proposal_traces
from .traces_by_outlier_score import create_node_traces_by_outlier_score

def createLandscape(**kwargs):
  """ Create the landscape graph, by default it creates one trace per competition with no highlighting """
  traces = []
  selected_proposal = kwargs.get('selected_proposal')
  view_type = kwargs.get('view_type', 'Topics')

  if selected_proposal:
    opacity = 0.5
    traces.extend(
      create_selected_proposal_traces(selected_proposal, by=view_type)
    )
  else:
    opacity = 0.65

  if view_type == 'Topics':
    traces.extend(
      create_node_traces_by_topic(opacity=opacity)
    )
  elif view_type == 'Competitions':
    traces.extend(
      create_node_traces_by_competition(opacity=opacity)
    )
  elif view_type == 'Outliers':
     traces.extend(
      create_node_traces_by_outlier_score(opacity=opacity, **kwargs)
    )

  traces.append(create_topic_label_trace())

  layout = go.Layout(
    showlegend=True,
    clickmode='select',
    margin=dict(l=0, r=0, t=0, b=0),
    legend=dict(
      bgcolor='rgba(0,0,0,0)',
      orientation='v',
      x=0.01, y=1,
      font=dict(
        color='#ccc',
        size=12
        ),
      title=dict(
        text='Click to toggle:'
        ),
      itemwidth=30,
      itemsizing='constant'
      ),
    modebar=dict(
      remove='resetCameraLastSave3d',
      orientation='v',
    ),
    scene=dict(
      bgcolor='#111',
      xaxis_visible=False, 
      yaxis_visible=False,
      zaxis_visible=False,
      camera=dict(
        eye=kwargs.get('eye', dict(x=1, y=1, z=1))
        )
      )
    )

  fig = go.Figure(
    data=[*traces],
    layout=layout
    )
  
  return fig

if __name__ == '__main__':
  fig = createLandscape()
  fig.show()