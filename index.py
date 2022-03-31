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
  Output('select-proposal', 'options'),
  Input('select-competition', 'value')
  )
def update_select_proposal_dropdown(*args):
  return callbacks.update_select_proposal_dropdown(*args)

@app.callback(
  Output('landscape-graph', 'figure'),
  Input('select-proposal', 'value'),
  Input('landscape-graph', 'clickData'),
  Input('graph-view-select', 'value'),
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