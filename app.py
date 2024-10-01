from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

df = pd.read_csv('data/no_of_cases_adults_15_to_49_by_country_clean.csv')
dm = pd.read_csv('data/no_of_deaths_by_country_clean.csv')
state_list = dm["Country"].unique()

app = Dash(__name__, external_stylesheets=['https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css'])

app.layout = html.Div([
    html.H1("AIDS Cases of adults btn 15 and 49"),
    html.Div([
        dcc.Dropdown(id='dropdown', options=[{'label': country, 'value': country} for country in df['Country'].unique()],
                     value='Albania')
    ]),
    html.Div([
        dcc.Graph(id='chart')
    ]),
    html.Div([
        html.H2("Nbr of deaths across the years"),
        html.Div("Choose the country:"),
        dcc.Dropdown(id="death_dp",
                     options=[{'label': country, 'value': country} for country in state_list],
                     value='Albania'),
        dcc.Graph(id='pie_chart')
    ])
])

@app.callback(
    Output("chart", "figure"),
    Output("pie_chart", "figure"),
    Input("dropdown", "value"),
    Input("death_dp", "value"),
)
def update_line(selected_country, selected_death_country):
    filtered_df = df[df['Country'] == selected_country]
    fig = px.line(filtered_df, x='Year', y='Count_max', title=f'Cases in {selected_country}', template='plotly_dark')

    filtered_dm = dm[dm['Country'] == selected_death_country]
    fig_pie = px.bar_polar(filtered_dm,
                            r=filtered_dm['Year'],
                            theta=filtered_dm['Country'],
                            color=filtered_dm['Year'],
                            template="plotly_white",
                            color_continuous_scale=px.colors.sequential.Plasma)

    return fig, fig_pie

if __name__ == '__main__':
    app.run(debug=True)
