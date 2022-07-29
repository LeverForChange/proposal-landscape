from dash import html, dcc

from ..const import topics, COMPETITION_NAMES

def resolve_topic(val):
  if val == -1:
    return 'No Topic'
  return ', '.join(topics[val]['words'][:2])

def resolve_global_view_url(source):
  return f"https://torque.leverforchange.org/GlobalView/index.php/{source['GlobalView MediaWiki Title']}"
  
def source_card(source):
  """ HTML structure for the card displaying the selected proposal """
  return html.Div([
    html.A([
      html.H2(source['Project Title']),
      html.P(['Organization: ', html.B(source.get('Organization Name'))]),
      html.P(['Competition: ', html.B(COMPETITION_NAMES[source.get('Competition Name')])]),
      html.P(['Topic: ', html.B(resolve_topic(source.get('Topic')))]),
      dcc.Markdown(source['Document Sanitized']),
      ],
      href=resolve_global_view_url(source),
      target='_blank'
    )],
    className='source-card'
  )

def neighbor_card(source):
  """ HTML structure for the cards displaying the selected proposal's neighbors """
  return html.Div([
    html.A([
      html.H3(source['Project Title']),
      html.P(['Organization: ', html.B(source.get('Organization Name'))]),
      html.P(['Competition: ', html.B(COMPETITION_NAMES[source.get('Competition Name')])]),
      html.P(['Topic: ', html.B(resolve_topic(source.get('Topic')))]),
      dcc.Markdown(source['Document Sanitized']),
      ],
      href=resolve_global_view_url(source),
      target='_blank'
    )],
    className='neighbor-card'
  )

def sidebar_divider(n_neighbors):
  return html.H3(
    [f'Similar proposals ({n_neighbors})'],
    className='sidebar-divider'
  )