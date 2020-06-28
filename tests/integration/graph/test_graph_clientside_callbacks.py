import pytest
from dash.testing.application_runners import import_app

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State, ClientsideFunction
from dash.exceptions import PreventUpdate

@pytest.mark.parametrize("is_eager", [True, False])
def test_grcc001_clientside_relayout(dash_duo, is_eager):
    app = dash.Dash(__name__, eager_loading=is_eager)
    initial_graph_title = "initial title"
    header = html.Div(
        id='header',
        children=[html.Button(id='update-title', children=['Update Title'])],
    )
    graph = html.Div(
        children=[
            dcc.Graph(
                id='clientside-graph',
                figure=dict(
                    layout=dict(title=initial_graph_title),
                    data=[
                        dict(
                            x=[1, 2, 3, 4],
                            y=[5, 4, 3, 6],
                            line=dict(shape='spline'),
                        )
                    ],
                ),
            )
        ],
    )

    app.clientside_callback(
        ClientsideFunction('pytest', 'relayout'),
        Output('header', 'style'),
        [Input('update-title', 'n_clicks')],
        [State('clientside-graph', 'figure')],
    )

    app.layout = html.Div(
        [header, graph]
    )

    dash_duo.start_server(app)

    dash_duo.wait_for_contains_text('#clientside-graph', initial_graph_title)
    dash_duo.wait_for_element('#update-title').click()
    dash_duo.wait_for_contains_text('#clientside-graph', "{}-new".format(initial_graph_title))
