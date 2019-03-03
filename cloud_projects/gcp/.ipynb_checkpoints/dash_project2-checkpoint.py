"""Dash Project."""
import os
import dash
# import flask
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import cufflinks as cf

cf.go_offline()

df = pd.read_csv('51_agro.csv')
df_futures = pd.read_csv('soy_fut.csv')

df = df.groupby(['Treatment', 'Crop', 'Year'], as_index=False).sum()

# df = df.set_index('Treatment')

df_futures = df_futures.set_index('Date')
df_futures = df_futures[['Price']]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# server = flask.Flask(__name__)
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash()
application = app.server

app.layout = html.Div([
    html.Div("Crop Treatments"),
    html.Div(children=[
        html.Div(children=[
            dcc.Graph(id='graph-with-slider'),
            dcc.Slider(
                id='year-slider',
                min=df['Year'].min(),
                max=df['Year'].max(),
                value=df['Year'].min(),
                marks={
                    str(Year): {
                        'label': str(Year),
                        'style': {
                            'color': 'blue',
                            'writing-mode': 'vertical-rl',
                            'text-orentation': 'upright'
                        }
                    } for Year in df['Year'].unique()
                }
            )
        ], className="six columns"),
        html.Div("Soy Future Prices"),
        html.Div(children=[
            dcc.Graph(id="futures-market"),
            html.Div(id="futures-market-trigger", style={"display": "none"})
        ], className="six columns"),
    ], className="row")
])


@app.callback(output=dash.dependencies.Output("futures-market", "figure"),
              inputs=[dash.dependencies.Input("futures-market-trigger", "children")])
def get_soybean_futures(_):
    """Get soybean futures and return as a plotly dictionary."""
    # return df_futures.iplot(kind="scatter", secondary_y=['Change %'],asFigure=True)
    return df_futures.iplot(kind="scatter", asFigure=True)


@app.callback(output=dash.dependencies.Output('graph-with-slider', 'figure'),
              inputs=[dash.dependencies.Input('year-slider', 'value')])
def update_crop_treatments(selected_year):
    """Get current crop treatment based on selected year and return plotly dictionary."""
    filtered_df = df[df.Year == selected_year]
    filtered_df = filtered_df.set_index('Treatment')
    return filtered_df[['Yield_bu_A', 'Crop']].iplot(kind='bar', asFigure=True)


if __name__ == '__main__':
    # app.run_server(debug=True)
    application.run(debug=True, port = 8080)