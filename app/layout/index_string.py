# See: https://dash.plotly.com/external-resources#customizing-dash's-html-index-template
INDEX_STRING = '''
<!DOCTYPE html>
<html>
  <head>
    {%metas%}
    <title>{%title%}</title>
    {%favicon%}
    {%css%}
    <style>
      ::-webkit-scrollbar {
          width: 0px;
        }
      ::-webkit-scrollbar-track {
        background: #111;
      }
      ::-webkit-scrollbar-thumb {
        background: #ddd;
      }
      ::-webkit-scrollbar-thumb:hover {
        background: #555;
      }
    </style>
  </head>
  <body>
    {%app_entry%}
    <footer>
      {%config%}
      {%scripts%}
      {%renderer%}
    </footer>
  </body>
</html>
'''