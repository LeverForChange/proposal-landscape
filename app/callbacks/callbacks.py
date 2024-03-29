import json
import dash
import pandas as pd

from dash import html, dcc

from ..const import df, knn_indices
from ..plots.plots import createLandscape
from ..layout.callbacks import source_card, neighbor_card, sidebar_divider

def update_camera_data(data):
  """ Updates the current camera position and stores in the camera-data component """
  if data:
    return json.dumps(data)
  else:
    return dash.no_update

def toggle_select_proposal(value):
  if value:
    return {'font-size': '12px'}
  else:
    return {'font-size': '12px', 'display': 'none'}

def toggle_search_controls(*args):
  if args[0] == args[1]:
    return {}
  else:
    return {'display': 'none'}

def toggle_outlier_threshold(value):
  if value == 'Outliers':
    return ''
  return 'hide'

def toggle_welcome_modal(*args):
  ctx = dash.callback_context
  input_ = ctx.triggered[0]['prop_id']
  if 'close' in input_:
    return {'display': 'none'}
  return {'display': 'block'}

def update_select_proposal_dropdown(*args):
  """ Updates the proposal selector with a list of the given competition's proposals """
  ctx = dash.callback_context
  input_ = ctx.triggered[0]['prop_id']

  def to_label_value(rows):
    return [{
      'label': row['Project Title'], 
      'value': i
      } for i, row in rows.iterrows()
      ]

  if 'select-competition' in input_:
    rows = df[
      df['Competition Name'] == args[0]
      ].sort_values('Project Title')

  elif 'select-topic' in input_:
    rows = df[
      df['Topic'] == args[1]
      ].sort_values('Project Title')

  elif 'document-search' in input_:
    tokens = args[2].split(' ')
    results = [
      df[
        df['Document Sanitized'].str.contains(tok, case=False)
        ] for tok in tokens
      ]
    if len(results) == 1:
      rows = results[0]
    else:
      rows = pd.merge(*results)
    rows.sort_values('Project Title', inplace=True)

  elif 'location-search' in input_:
    tokens = args[3].split(' ')
    location_cols = list(
      df.filter(regex='Future Work #[1-5] Location').columns
      )
    results = []
    for col in location_cols:
      for tok in tokens:
        results.append(
          df[
            df[col].str.contains(tok, case=False, na=False)
            ]
          )
    if len(results) == 1:
      rows = results[0]
    else:
      rows = pd.merge(*results)
    rows.sort_values('Project Title', inplace=True)

  options = to_label_value(rows)
  return options, False

def update_graph(
  project_title, 
  click_data,
  view_type,
  outlier_threshold,
  view_type_state,
  camera_data
  ):
  """ 
  Redraws the main graph 
  """
  camera_data = json.loads(camera_data)
  eye = camera_data.get('scene.camera', {}).get('eye')

  # figure out if the proposal was selected on the graph or from the dropdown
  ctx = dash.callback_context
  input_ = ctx.triggered[0]['prop_id']

  if 'select-proposal' in input_ and project_title:
    fig = createLandscape(
      selected_proposal=project_title,
      eye=eye,
      view_type=view_type_state,
      outlier_threshold=outlier_threshold
      )

  elif 'clickData' in input_ and click_data:
    index = click_data['points'][0]['customdata']
    fig = createLandscape(
      selected_proposal=index,
      eye=eye,
      view_type=view_type_state,
      outlier_threshold=outlier_threshold
      )

  elif 'graph-view-select' in input_ and view_type:
    fig = createLandscape(
      eye=eye, 
      view_type=view_type, 
      outlier_threshold=outlier_threshold
      )

  elif 'outlier-threshold' in input_ and view_type:
    fig = createLandscape(
      eye=eye,
      view_type=view_type_state,
      outlier_threshold=outlier_threshold
      )

  else:
    fig = createLandscape(eye=eye)

  return fig

def update_selected_proposal(click_data, project_index):
  """ Updates the sidebar with info on the selected proposal and its neighbors, if any """
  # Determine which component triggered the callback
  ctx = dash.callback_context
  input_ = ctx.triggered[0]['prop_id']

  if 'clickData' in input_ and click_data:
    index = click_data['points'][0]['customdata']

  elif 'select-proposal' in input_ and project_index:
    index = project_index
    
  else:
    # Clear sidebar if the dropdown is cleared
    return None, None

  source = df.iloc[index]
  source = source.to_dict()

  nodes = []
  nodes.append(source_card(source))

  neighbors = knn_indices[index]
  num_neighbors = len(neighbors)
  if num_neighbors:

    nodes.append(sidebar_divider(num_neighbors))

    neighbors = df.iloc[neighbors]
    neighbors = neighbors.to_dict(orient='records')
    for proposal in neighbors:
      nodes.append(neighbor_card(proposal))

  return html.Div(nodes), index

def download_dataframe(*args):
  index = args[1]
  neighbors = knn_indices[index]
  indices = [index] + neighbors
  cols = [
    'Project Title',
    'Organization Name',
    'Competition Name',
    'Document Sanitized',
    'GlobalView MediaWiki Title'
    ]

  download_df = df.iloc[indices, :]
  download_df = download_df[cols]

  download_df['URL'] = download_df['GlobalView MediaWiki Title'].apply(
    lambda x: f"https://torque.leverforchange.org/GlobalView/index.php/{x}"
    )
  download_df.rename({'Document Sanitized': 'Executive Summary'}, inplace=True)
  download_df.drop(columns=['GlobalView MediaWiki Title'], inplace=True)

  return dcc.send_data_frame(
    download_df.to_excel,
    'LFC Landscape.xlsx',
    sheet_name='Main',
    index=False
    )

def show_download_button(index):
  if index:
    return 'button'
  else:
    return 'button hide'