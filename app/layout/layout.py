from dash import html, dcc

from ..const import df, COMPETITION_NAMES
from ..plots.plots import createLandscape

LAYOUT = html.Div(children=[

  # Main container
  html.Div(children=[

    # Sidebar
    html.Div(children=[

      # Selector/Group By area
      html.Div(children=[
        
        # Competition selector
        dcc.Dropdown(
          [{'label': l, 'value': v} for v, l in COMPETITION_NAMES.items()],
          placeholder='Select a competition',
          clearable=False,
          id='select-competition',
          className='dropdown'
        ),

        # Proposal selector (blank until a competition is chosen)
        dcc.Dropdown(
          [],
          placeholder='Select a proposal',
          id='select-proposal',
          className='dropdown',
          style={'font-size': '12px'}
          ),
        ]),

        dcc.RadioItems(
          ['View by Competition', 'View by Topic'],
          'View by Topic',
          id='graph-view-select',
          inline=True
        ),

      # Info display area
      html.Div(
        [
          '', 
          html.Pre(
            id='click-data', 
            className='proposal-data-container'
            )
        ]),
      ],
      className='sidebar-container'
    ),

    # Graph
    dcc.Graph(
      id='landscape-graph',
      figure=createLandscape(),
      config={
        'displaylogo': False,
        'displayModeBar': True,
        'doubleClick': 'reset'
      },
      className='graph-container'
    ),
  ],
  className='container'
  ),

  dcc.Store(id='camera-data')
  ],           
)