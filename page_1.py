import pandas as pd
import dash_bootstrap_components as dbc
from main import app
import plotly.express as px
from dash.dependencies import Input, Output
from dash import html, dcc, dash_table
import plotly.graph_objects as go



def app_layout():
    """
    Main app layout.
    """
    return dbc.Container([
        dbc.Row([
            html.H1(
                children="Dash Dashboard",
                className = "text-center p-3",
                style={
                    "color": "black",
                    "text-align": "center"
                }
            )
        ]),
        dbc.Alert(
            [
                html.H4("How to Use?", className="alert-heading"),
                html.P(
                    "Select the Compound ID's from the dropdown list to visualize the assay results."),
                html.Hr(),
                html.P(
                    "Several Compounds can be selected for comparison."
                )
            ], dismissable=True
        ),
        dbc.Card([
            dbc.Row([
                dbc.Col(
                    dcc.Dropdown(
                        dropdown(), 'Select Compound ID', id='compound-dropdown', className="text-center p-3", multi=True, clearable=False),
                    width={"size": 6, "offset": 3}
                )]
            ),
            dbc.Row([
                dbc.Col([],width=1),
                dbc.Col([html.Div(dcc.Graph(id='graph_1',
                                            style={'float': 'top',
                                                   'margin': 'auto',
                                                   'width': '100%',
                                                   'height': '50vh'},
                                            responsive=True,
                                  figure=blank_figure()))]),
                dbc.Col([
                    html.Div(id='tbl')
                ], width=4),
                dbc.Col([], width=1)
            ],justify="evenly")
        ])
   ])


@app.callback(
    Output('graph_1', 'figure'),
    Output('tbl', 'children'),
    Input('compound-dropdown', 'value')
)
def scatter_plot_1(value):
    """
    Generates main concentration vs inhibition scatter plot

    Returns
    -------
    fig : Plotly Figure Object.
        Scatter plot of concentration vs inhibition of selected compounds.
    info_table : Div component.
        Returns data table of additional compound information (label and IC50), if exists.
    """
    df_assay_res = pd.read_csv('static/assay_results.csv')
    df_labels = pd.read_csv('static/compound_labels.csv')
    df_ic50 = pd.read_csv('static/compound_ic50.csv')

    if len(value) == 0:
        return blank_figure(), ""

    data = pd.concat([df_assay_res[df_assay_res['Compound ID'] == i] for i in value])
    data["Compound ID"] = data["Compound ID"].astype(str)
    fig = px.scatter(data, x='Concentration (M)', y='% Inhibition', color='Compound ID', title="Enzyme Inhibition vs Concentration")
    data_labels = pd.concat([df_labels[df_labels['Compound ID'] == i] for i in value])
    data_ic50  = pd.concat([df_ic50[df_ic50['Compound ID'] == i] for i in value])
    compound_info_table = pd.concat([data_labels,data_ic50],axis=1).drop_duplicates()
    merged = pd.merge(data_labels, data_ic50, how='inner', right_on='Compound ID', left_on='Compound ID')
    info_table = html.Div([dbc.Table.from_dataframe(
        merged, striped=True, bordered=True)],
        style={"maxHeight": "500px", "overflow": "scroll"}
    )
    return fig, info_table


def dropdown():
    """
    Gets Compound IDs from input data.

    Returns
    -------
    compounds_list : list
        List of Compounds IDs from input CSV data.
    """
    df_assay_res = pd.read_csv('static/assay_results.csv')
    compounds_list = df_assay_res['Compound ID'].unique()
    return compounds_list


def blank_figure():
    """
    Creates a blank figure to avoid showing default Plotly Graph Template.

    Returns
    -------
    fig : Plotly Figure Object.
    """
    fig = go.Figure(go.Scatter(x=[], y=[]))
    fig.update_layout(template=None)
    fig.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
    fig.update_yaxes(showgrid=False, showticklabels=False, zeroline=False)

    return fig




