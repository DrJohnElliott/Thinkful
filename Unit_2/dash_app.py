import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import cufflinks as cf

cf.go_offline()

df = pd.read_csv(
    'https://raw.githubusercontent.com/plotly/'
    'datasets/master/gapminderDataFiveYear.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div("Hello World"),
    html.Div(children=[
        html.Div(children=[
            dcc.Graph(id='graph-with-slider'),
            dcc.Slider(
                id='year-slider',
                min=df['year'].min(),
                max=df['year'].max(),
                value=df['year'].min(),
                marks={str(year): str(year) for year in df['year'].unique()}
            )
        ], className="six columns"),
        html.Div("Good by World"),
        html.Div(children=[
            dcc.Graph(id="stock-market"),
            html.Div(id="stock-market-trigger", style={"display": "none"})
        ], className="six columns"),
    ], className="row")
])


@app.callback(output=dash.dependencies.Output("stock-market", "figure"),
              inputs=[dash.dependencies.Input("stock-market-trigger", "children")])
def get_stock_market(_):
    # https://plot.ly/ipython-notebooks/cufflinks/
    df = cf.datagen.lines()
    return df.iplot(kind="scatter", asFigure=True)


@app.callback(output=dash.dependencies.Output('graph-with-slider', 'figure'),
              inputs=[dash.dependencies.Input('year-slider', 'value')])
def update_figure(selected_year):
    filtered_df = df[df.year == selected_year]
    traces = []
    for i in filtered_df.continent.unique():
        df_by_continent = filtered_df[filtered_df['continent'] == i]
        traces.append(go.Scatter(
            x=df_by_continent['gdpPercap'],
            y=df_by_continent['lifeExp'],
            text=df_by_continent['country'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'type': 'log', 'title': 'GDP Per Capita'},
            yaxis={'title': 'Life Expectancy', 'range': [20, 90]},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)