from dash import html, dcc

from ..const import topics, COMPETITION_NAMES
from ..plots.plots import createLandscape

LAYOUT = html.Div(children=[

  # Main container
  html.Div(children=[

    # Sidebar
    html.Div(children=[

      # Title/links
      html.Div(children=[
        html.H3('Lever for Change Proposal Landscape'),
        html.A(
          'Leave Feedback', 
          href='https://docs.google.com/document/d/1SvPGF_vcBuYObYy0HjORnxPz5V1kDgSJtrchQCICyZs/edit?usp=sharing', 
          target='_blank', 
          className='button'
          )
        ],
        className='center',
        style={
          'margin-bottom': '1rem'
        }
      ),

      # Selector/Group By area
      html.Div(children=[
        
        dcc.Tabs(
          parent_className='custom-tabs',
          className='custom-tabs-container',
          children=[
            dcc.Tab(
              label='Proposal Search',
              className='custom-tab',
              selected_className='custom-tab--selected',
              children=[

                # Search control
                dcc.Dropdown(
                  [
                    {'label': 'Competition', 'value': 'select-competition'},
                    {'label': 'Topic', 'value': 'select-topic'},
                    {'label': 'Text', 'value': 'document-search'},
                    {'label': 'Project Location', 'value': 'location-search'}
                  ],
                  placeholder='Search by...',
                  id='search-control',
                  className='dropdown'
                ),

                # Competition selector
                dcc.Dropdown(
                  [{'label': l, 'value': v} for v, l in COMPETITION_NAMES.items()],
                  placeholder='Select a competition',
                  clearable=False,
                  id='select-competition',
                  className='dropdown',
                  style={'display': 'none'}
                ),

                # Topic selector
                dcc.Dropdown(
                  [{'label': ', '.join(l['words']), 'value': v} for v, l in topics.items()][1:], # exclude no topic
                  placeholder='Select a topic',
                  clearable=False,
                  id='select-topic',
                  className='dropdown',
                  style={'display': 'none'}
                ),

                # Doc search
                dcc.Input(
                  id='document-search',
                  type='search',
                  debounce=True,
                  placeholder='enter search terms...',
                  className='input',
                  style={'display': 'none'}
                ),

                # location search
                dcc.Input(
                  id='location-search',
                  type='search',
                  debounce=True,
                  placeholder='enter search terms...',
                  className='input',
                  style={'display': 'none'}
                ),

                # Proposal selector (blank until a competition is chosen)
                dcc.Dropdown(
                  [],
                  placeholder='Select a proposal',
                  id='select-proposal',
                  disabled=True,
                  className='dropdown',
                  style={
                    'font-size': '12px',
                    'display': 'none'
                    }
                  ),
              ]),
          
          # Graph options tab
          dcc.Tab(
            label='Graph Options',
            className='custom-tab',
            selected_className='custom-tab--selected',
            children=[
              html.Div(children=[
                html.B(
                'Highlight:',
                style={'width': '20%'}
                ),
              ],
                className='row center',
                style={'margin-top': '0.5rem', 'margin-bottom': '0.5rem'}
              ),
              dcc.RadioItems(
                options=['Topics', 'Competitions', 'Outliers'],
                value='Topics',
                id='graph-view-select',
                inline=True,
                className='row between',
                style={'margin-bottom': '1rem'}
              ),
              dcc.Slider(
                0, 1, 0.05,
                marks={
                  0: {'label': 'Less Unique', 'style': {'width': 'min-content', 'color': 'white'}},
                  1: {'label': 'More Unique', 'style': {'width': 'min-content', 'color': 'white'}},
                  },
                value=0.6,
                className='hide',
                id='outlier-threshold'
              )
              ],
            )
        ]),
      ]),
  
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