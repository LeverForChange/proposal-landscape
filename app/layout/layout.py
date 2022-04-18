from dash import html, dcc

from ..const import topics, COMPETITION_NAMES
from ..plots.plots import createLandscape

LAYOUT = html.Div(children=[

  # Welcome modal
  html.Div(
    className='modal',
    style={'display': 'block'},
    id='welcome-modal',
    children=[
      html.Div(
        className='modal-content',
        children=[
          html.H1(className='center', children='Welcome to the Lever For Change Proposal Landscape!'),
          html.H4(className='center', children=html.Span([
            'Please consider leaving feedback or a note about how you used this tool ',
            html.A('here.', href='https://docs.google.com/document/d/1SvPGF_vcBuYObYy0HjORnxPz5V1kDgSJtrchQCICyZs/edit?usp=sharing', target='_blank')
            ]),
          ),
          html.P('1) Nearly everything in the interface is clickable. Click + drag to rotate the graph, and scroll to zoom in/out. Click/double click on legend items, under "Click to toggle:" to show/hide items on the graph. Click directly on points to view more detailed information about them. Click on proposal info cards to view their page on GlobalView.'),
          html.P('2) By default, the graph is colored by Topic. Note that topics displayed are different from Primary Subject Area. The topics you see are generated via machine learning analysis of the dataset.'),
          html.P('3) To change how the graph is colored, click the "Graph Options" tab on the left, and choose one fo the other highlight options. Choosing "Outliers" will also allow you to specify the threshold at which a proposal is considered an outlier.'),
          html.P('4) Use the "Proposal Search" tab to find a specific propoal & its similar proposals. You can also click directly on points in the graph to do so!'),
          html.P('5) When using the "Proposal Search" tab, first choose a metric to search by (Competition, Text, Topic, or Geography). Then enter your search terms or choose from the resulting dropdown selection. Finally, a list of proposals will be returned in the final dropdown. Choosing a proposal from the final dropdown will highlight the point in the graph and display more detailed information about it and its neighbors in the sidebar.'),
          html.Div(className='row center', children=html.Button(
            id='close-welcome-modal', className='button', children='Close')
          ),
        ]
      )
    ]
  ),

  # Main container
  html.Div(children=[

    # Sidebar
    html.Div(children=[

      # Title/links
      html.Div(children=[
        html.H3('Lever for Change Proposal Landscape'),
        html.Div(className='row around', children=[
          html.A(
            'Leave Feedback', 
            href='https://docs.google.com/document/d/1SvPGF_vcBuYObYy0HjORnxPz5V1kDgSJtrchQCICyZs/edit?usp=sharing', 
            target='_blank', 
            className='button'
          ),
          html.A(id='open-welcome-modal', className='button', children='View Instructions')
          ])
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

                # Download .xlsx
                html.Div(
                  className='center', 
                  style={'margin-top': '1rem'}, 
                  children=[
                    html.Button('Download to Excel', id='download-btn', className='button hide')
                ])
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

    dcc.Graph(
      id='landscape-graph',
      figure=createLandscape(),
      config={
        'displaylogo': False,
        'displayModeBar': True,
        'doubleClick': 'reset'
      },
      className='graph-container',
      loading_state={
        'component_name': 'graph-loader'
      }
    )
  ],
  className='container'
  ),

  dcc.Store(id='camera-data'),
  dcc.Store(id='selected-proposal'),
  dcc.Download(id='download-dataframe')
  ],           
)