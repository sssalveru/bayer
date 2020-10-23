import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from app import app
from app import server

from apps import PFDS
PLOTLY_LOGO = "https://upload.wikimedia.org/wikipedia/commons/f/f7/Logo_Bayer.svg"

app.title = "Berkeley CPV Dashboard"
nav_item = dbc.NavItem(dbc.NavLink("Home", href="/"))

# make a reuseable dropdown for the different examples
dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("Cell Culture"),
        dbc.DropdownMenuItem(divider=True),
        dbc.DropdownMenuItem("Isolation"),
        dbc.DropdownMenuItem(divider=True),
        dbc.DropdownMenuItem("Drug Substance", href='/apps/PFDS'),
        dbc.DropdownMenuItem(divider=True),
        dbc.DropdownMenuItem("Drug Product"),
    ],
    nav=True,
    in_navbar=True,
    label="Kovaltry",
)

dropdown1 = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("Cell Culture"),
        dbc.DropdownMenuItem(divider=True),
        dbc.DropdownMenuItem("Isolation"),
        dbc.DropdownMenuItem(divider=True),
        dbc.DropdownMenuItem("Drug Substance"),
        dbc.DropdownMenuItem(divider=True),
        dbc.DropdownMenuItem("Drug Product"),
    ],
    nav=True,
    in_navbar=True,
    label="Jivi",
)

logo = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="45px")),
                        dbc.Col(dbc.NavbarBrand("CPV Interactive Dashboard", className="ml-2")),
                    ],
                    align="center",
                    no_gutters=True,
                ),
                # href="https://plot.ly",
            ),
            dbc.NavbarToggler(id="navbar-toggler2"),
            dbc.Collapse(
                dbc.Nav(
                    [nav_item, dropdown, dropdown1], className="ml-auto", navbar=True
                ),
                id="navbar-collapse2",
                navbar=True,
            ),
        ]
    ),
    color="primary",
    dark=True,
    className="mb-5",
)


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    logo,
    html.Div(id='page-content', children=[])
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/PFDS':
        return PFDS.layout
    else:
        return html.Div([dbc.Row(dbc.Col(html.H2("Welcome"),
                    style={"textAlign": "center"})),])


def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


app.callback(
    Output(f"navbar-collapse2", "is_open"),
    [Input(f"navbar-toggler2", "n_clicks")],
    [State(f"navbar-collapse2", "is_open")],
)(toggle_navbar_collapse)

if __name__ == "__main__":
    app.run_server(debug=True)

