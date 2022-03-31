import json
import dash

from dash import html

from ..const import df, knn_indices
from ..plots.plots import createLandscape
from ..layout.callbacks import source_card, neighbor_card, sidebar_divider

def update_camera_data(data):
  """ Updates the current camera position and stores in the camera-data component """
  if data:
    return json.dumps(data)
  else:
    return dash.no_update

def update_select_proposal_dropdown(value):
  """ Updates the proposal selector with a list of the given competition's proposals """
  rows = df[df['Competition Domain'] == value].sort_values('Project Title')
  return rows['Project Title']

def update_graph(project_title, click_data, view_type, view_type_state, camera_data):
  """ 
  Redraws the main graph 
  """
  camera_data = json.loads(camera_data)
  eye = camera_data.get('scene.camera', {}).get('eye')

  # figure out if the proposal was selected on the graph or from the dropdown
  ctx = dash.callback_context
  input_ = ctx.triggered[0]['prop_id']

  if 'select-proposal' in input_ and project_title:
    fig = createLandscape(selected_proposal=project_title, eye=eye, view_type=view_type_state)

  elif 'clickData' in input_ and click_data:
    index = click_data['points'][0]['customdata']
    fig = createLandscape(selected_proposal=index, eye=eye, view_type=view_type_state)

  elif 'graph-view-select' in input_ and view_type:
    fig = createLandscape(eye=eye, view_type=view_type)

  else:
    fig = createLandscape(eye=eye)

  return fig

def display_proposal_neighbors(click_data, project_title):
  """ Updates the sidebar with info on the selected proposal and its neighbors, if any """
  # Determine which component triggered the callback
  ctx = dash.callback_context
  input_ = ctx.triggered[0]['prop_id']

  if 'clickData' in input_ and click_data:
    index = click_data['points'][0]['customdata']
    source = df.iloc[index]
    source = source.to_dict()
  elif 'select-proposal' in input_ and project_title:
    source = df[df['Project Title'] == project_title]
    index = int(list(source.index)[0])
    source = source.iloc[0].to_dict()
  else:
    # Clear sidebar if the dropdown is cleared
    return None

  nodes = []
  nodes.append(source_card(source))

  neighbors = knn_indices[index]
  num_neighbors = len(neighbors) - 1
  if num_neighbors:

    nodes.append(sidebar_divider(num_neighbors))

    neighbors = df.iloc[neighbors[1:]]
    neighbors = neighbors.to_dict(orient='records')
    for proposal in neighbors:
      nodes.append(neighbor_card(proposal))

  return html.Div(nodes)