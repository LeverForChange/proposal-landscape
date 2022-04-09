from dash import Dash
from dash.dependencies import Input, Output, State

from app.layout.index_string import INDEX_STRING
from app.layout.layout import LAYOUT
from app.callbacks import callbacks

app = Dash(
  __name__,
  title='Lever for Change Landscape',
  update_title=None,
  prevent_initial_callbacks=True
  )
app.index_string = INDEX_STRING
app.layout = LAYOUT

server = app.server

""" Callback definitions """
@app.callback(
  Output('camera-data', 'data'),
  Input('landscape-graph', 'relayoutData'),
  )
def update_camera_data(*args):
  return callbacks.update_camera_data(*args)

@app.callback(
  Output('select-proposal', 'style'),
  Input('search-control', 'value')
)
def toggle_select_competition(value):
  return callbacks.toggle_select_proposal(value)

@app.callback(
  Output('select-competition', 'style'),
  Input('search-control', 'value')
)
def toggle_select_competition(value):
  return callbacks.toggle_search_controls(value, 'select-competition')

@app.callback(
  Output('select-topic', 'style'),
  Input('search-control', 'value')
)
def toggle_select_competition(value):
  return callbacks.toggle_search_controls(value, 'select-topic')

@app.callback(
  Output('document-search', 'style'),
  Input('search-control', 'value')
)
def toggle_document_search(value):
  return callbacks.toggle_search_controls(value, 'document-search')

@app.callback(
  Output('location-search', 'style'),
  Input('search-control', 'value')
)
def toggle_document_search(value):
  return callbacks.toggle_search_controls(value, 'location-search')

@app.callback(
  Output('outlier-threshold', 'className'),
  Input('graph-view-select', 'value')
)
def toggle_outlier_threshold(value):
  return callbacks.toggle_outlier_threshold(value)

@app.callback(
  Output('select-proposal', 'options'),
  Output('select-proposal', 'disabled'),
  Input('select-competition', 'value'),
  Input('select-topic', 'value'),
  Input('document-search', 'value'),
  Input('location-search', 'value')
  )
def update_select_proposal_dropdown(*args):
  return callbacks.update_select_proposal_dropdown(*args)

@app.callback(
  Output('landscape-graph', 'figure'),
  Input('select-proposal', 'value'),
  Input('landscape-graph', 'clickData'),
  Input('graph-view-select', 'value'),
  Input('outlier-threshold', 'value'),
  State('graph-view-select', 'value'),
  State('camera-data', 'data'),
  )
def update_graph(*args):
  return callbacks.update_graph(*args)

@app.callback(
  Output('click-data', 'children'), 
  Input('landscape-graph', 'clickData'),
  Input('select-proposal', 'value'),
  )
def display_proposal_neighbors(*args):
  return callbacks.display_proposal_neighbors(*args)
  
if __name__ == '__main__':
    app.run_server(debug=True)