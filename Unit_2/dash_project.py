import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import cufflinks as cf

cf.go_offline()

df = pd.read_csv('51_agro.csv')
df_futures = pd.read_csv('soy_fut.csv')

df = df.groupby(['Crop', 'Treatment', 'Year'],as_index=False).sum()
df_futures =  df_futures.set_index('Date') 
df_futures = df_futures[['Price']]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

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
                marks={str(Year): {'label':str(Year),'style':{'color':'blue',
                 'writing-mode':'vertical-rl',
                 'text-orentation':'upright'} }
                                   for Year in df['Year'].unique()}
            ) #slider dcc
            
        ],                
            className="six columns"),
        html.Div("Soy Future Prices"),      
        html.Div(children=[
            dcc.Graph(id="futures-market"),
            html.Div(id="futures-market-trigger", style={"display": "none"})
        ], className="six columns"),
    ], className="row")
])

@app.callback(output=dash.dependencies.Output("futures-market", "figure"),
              inputs=[dash.dependencies.Input("futures-market-trigger", "children")])
def get_stock_market(_):  
   # return df_futures.iplot(kind="scatter", secondary_y=['Change %'],asFigure=True)
    return df_futures.iplot(kind="scatter",asFigure=True)

@app.callback(output=dash.dependencies.Output('graph-with-slider', 'figure'),
              inputs=[dash.dependencies.Input('year-slider', 'value')])
def update_figure(selected_year):
    filtered_df = df[df.Year == selected_year]
    traces = []
    for i in filtered_df.Crop.unique():
        df_by_Crop = filtered_df[filtered_df['Crop'] == i]
        traces.append(go.Bar(
            x=df_by_Crop['Treatment'],
            y=df_by_Crop['Yield_bu_A'],
            text=df_by_Crop['Crop'],
            name=i
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={ 'title': 'Treatment'},
            yaxis={'title': 'Yield_bu_A', 'range': [0, 1200]},
            margin={'l': 40, 'b': 40, 't': 60, 'r': 10},
            legend={'x': 0, 'y': 1.1},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)