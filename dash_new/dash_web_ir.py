import pandas as pd
import numpy as np
import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objs as go

# Load your taxonomy data
list_with_taxonomy = pd.read_csv("/home/vic/2024-victor-IRs-Victor/results/Snakemake/taxonomy.csv")
df = list_with_taxonomy


columns = list(df.columns)
to_remove = ['full_name', 'Replicons_name', 'Replicons_type']
columns = [col for col in columns if col not in to_remove] 



list_options = [
    dcc.Dropdown(
        id=f"sidebar-{column}-dropdown",
        options=list(df[column].unique()),
        multi=True,
        style={ 
                "backgroundColor": "#1E1E2D",
                "color": "#6896C4",
                "padding": "5px"}
    ) for column in columns
    ]


# Sidebar definition (must come before app.layout)
sidebar = html.Div(
    style={
        "width": "280px",
        "height": "100vh",
        "position": "fixed",
        "top": 0,
        "left": 0,
        "backgroundColor": "#1E1E2D",
        "padding": "20px",
        "color": "white",
        "display": "flex",
        "flexDirection": "column",
        "justifyContent": "space-between",
    },
    children=[
        html.Div([
            html.H4("🧬 IR dashboard", style={"marginBottom": "30px"}),

            dbc.Card(
                dbc.CardBody([
                    html.Div("Victor BG", style={"fontWeight": "bold"}),
                    html.Div("PhD Student", style={"fontSize": "12px", "color": "#aaa"})
                ]),
                style={"marginBottom": "30px", "backgroundColor": "#2A2A3C"}
            ),

            dbc.Nav([
                dbc.NavLink("Debrief", href="#", id="nav-debrief", n_clicks=0),
                dbc.NavLink("General", href="#", id="nav-general", n_clicks=0),
                dbc.NavLink(
                    ["Individual", html.Span(f"{len(df)}", className="badge bg-danger ms-2")],
                    href="#", id="nav-individual", n_clicks=0
                ),  
                # Collapsible sub-items for Individual
                html.Div(
                    id="ind-subitems",
                    children=list_options,
                    style={"display": "none"}  # hidden by default
                ),

            ], vertical=True, pills=False),

            html.H6("SHORTCUTS", className="mt-4", style={"fontSize": "12px", "color": "#bbb"}),

            dbc.Nav([
                dbc.NavLink("⚙️ Settings", href="#", id="nav-settings", n_clicks=0),
            ], vertical=True, pills=False),

            dbc.Card(
                dbc.CardBody([
                    html.Div("Used Space", style={"fontWeight": "bold", "fontSize": "12px"}),
                    html.Div("Admin updated 09:12 am", style={"fontSize": "10px", "color": "#aaa"}),
                    html.Div("November 08, 2020", style={"fontSize": "10px", "color": "#aaa"}),
                    dbc.Progress(value=77, color="info", className="mt-2", style={"height": "8px"})
                ]),
                style={"backgroundColor": "#2A2A3C", "marginTop": "200px"}
            ),
        ]),
    ]
)

# Main content area
main_content = html.Div(
    id="main-content",
    style={"marginLeft": "300px", "padding": "20px", "color": "white"},
    children=[
        html.H2("Welcome"),
        html.P("Click a menu item to show content here.")
    ]
)

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# App layout including dcc.Store to track collapse state
app.layout = html.Div([
    dcc.Store(id='ind-collapse-store', data=False),  # stores whether individual submenu is open
    sidebar,
    main_content
])

# Callback to toggle the Individual submenu visibility
@app.callback(
    Output("ind-subitems", "style"),
    Output("ind-collapse-store", "data"),
    Input("nav-individual", "n_clicks"),
    Input("nav-general", "n_clicks"),
    Input("nav-debrief", "n_clicks"),
    Input("nav-settings", "n_clicks"),
    State("ind-collapse-store", "data")
)
def toggle_individual(individual_clicks, general_clicks,debrief_clicks, settings_clicks, is_open):
    ctx = dash.callback_context
    if not ctx.triggered:
        # On app load, submenu is collapsed
        return {"display": "none"}, False

    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_id == "nav-individual":
        # Toggle submenu open/close
        new_state = not is_open
        style = {"display": "block" if new_state else "none"}
        return style, new_state
    else:
        # If another menu clicked, collapse submenu
        return {"display": "none"}, False

# Callback to update main content area when clicking sidebar nav links
@app.callback(
    Output("main-content", "children"),
    [
        Input("nav-debrief", "n_clicks"),
        Input("nav-general", "n_clicks"),
        Input("nav-individual", "n_clicks"),
        Input("nav-settings", "n_clicks"),
    ]
)
def display_content(click_general,click_debrief, click_individual, click_settings):
    ctx = dash.callback_context
    if not ctx.triggered:
        return [html.H2("Welcome"), html.P("Click a menu item to show content here.")]
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    content = html.Div(
        [
            dcc.Tabs(
                id="tabs",
                value="tab-graph",
                children=[ 
                    dcc.Tab(label="Structural", value="tab-Structural", style={"backgroundColor": "#2A2A3C"}, selected_style={"backgroundColor": "#50506D", "color": "white"}),
                    dcc.Tab(label="Kmer", value="tab-Kmer", style={"backgroundColor": "#2A2A3C"}, selected_style={"backgroundColor": "#50506D", "color": "white"}),
                    dcc.Tab(label="Spatial", value="tab-Spatial", style={"backgroundColor": "#2A2A3C"}, selected_style={"backgroundColor": "#50506D", "color": "white"}),
                    dcc.Tab(label="Compositional", value="tab-Compositional", style={"backgroundColor": "#2A2A3C"}, selected_style={"backgroundColor": "#50506D", "color": "white"}),
                ],
                colors={"border": "#ccc", "primary": "#50506D", "background": "#2A2A3C"},
            ),
            html.Div(id="tab-content", style={"padding": "20px", "backgroundColor": "#2A2A3C", "boxShadow": "0px 0px 10px rgba(0,0,0,0.1)"})
        ],
        style={ 
            "padding": "20px",
        }
    ) 

    content_map = {
        "nav-debrief": "Lorem Ipsum",
        "nav-general": content,
        "nav-individual": content,
        "nav-settings": create_dumb_graph()
    }

    content = content_map.get(button_id, "No content available.")

    if isinstance(content, str):
        return [html.H2(button_id.replace("nav-", "").capitalize()), html.P(content)]
    else:
        # If content is a component like a graph
        return [html.H2(button_id.replace("nav-", "").capitalize()), content]


# Callback for outer tab selection
@app.callback(
    Output("tab-content", "children"),
    [Input("tabs", "value")]
)
def render_tab_content(tab):
    styles = {"color": "#003366"}

    if tab == "tab-Structural":
        return html.Div([ 
            dcc.Tabs(
                id='Structural-inner-tabs',
                value='Structural-HC',
                children=[
                    dcc.Tab(label='HA', value='Structural-HA',style={ "backgroundColor": "#2A2A3C"},selected_style={"backgroundColor": "#50506D"}), 
                    dcc.Tab(label='HB', value='Structural-HB',style={ "backgroundColor": "#2A2A3C"},selected_style={"backgroundColor": "#50506D"}), 
                    dcc.Tab(label='HC', value='Structural-HC',style={ "backgroundColor": "#2A2A3C"},selected_style={"backgroundColor": "#50506D"}), 
                ],
                style={ "backgroundColor": "#2A2A3C","marginTop": "10px"},
            ),
            html.Div(id='Structural-inner-content')
        ]) 
    
    elif tab == "tab-Kmer":
        return html.Div([ 
            dcc.Tabs(
                id='Kmer-inner-tabs',
                value='Kmer-ratio',
                children=[
                    dcc.Tab(label='Kmer-ratio', value='Kmer-ratio',style={ "backgroundColor": "#2A2A3C"},selected_style={"backgroundColor": "#50506D"}), 
                    dcc.Tab(label='Kmer-nucleotide', value='Kmer-nucleotide',style={ "backgroundColor": "#2A2A3C"},selected_style={"backgroundColor": "#50506D"}),  
                ],
                style={ "backgroundColor": "#2A2A3C","marginTop": "10px"},
            ),
            html.Div(id='Kmer-inner-content')
        ]) 
    
    elif tab == "tab-Spatial":
        return html.Div([ 
            dcc.Tabs(
                id='Spatial-inner-tabs',
                value='Spatial-Replicon',
                children=[
                    dcc.Tab(label='Spatial Replicon', value='Spatial-Replicon',style={ "backgroundColor": "#2A2A3C"},selected_style={"backgroundColor": "#50506D"}), 
                    dcc.Tab(label='Spatial Region', value='Spatial-Region',style={ "backgroundColor": "#2A2A3C"},selected_style={"backgroundColor": "#50506D"}), 
                    dcc.Tab(label='Spatial IR', value='Spatial-IR',style={ "backgroundColor": "#2A2A3C"},selected_style={"backgroundColor": "#50506D"}), 
                ],
                style={ "backgroundColor": "#2A2A3C","marginTop": "10px"},
            ),
            html.Div(id='Spatial-inner-content')
        ]) 
    
    elif tab == "tab-Compositional":
        return html.Div([ 
            dcc.Tabs(
                id='Compositional-inner-tabs',
                value='Compositional-Catalogue',
                children=[
                    dcc.Tab(label='Compositional Catalogue' , value='Compositional-Catalogue',style={ "backgroundColor": "#2A2A3C"},selected_style={"backgroundColor": "#50506D"}), 
                    dcc.Tab(label='Compositional Philogenie', value='Compositional-Philogenie',style={ "backgroundColor": "#2A2A3C"},selected_style={"backgroundColor": "#50506D"}),  
                ],
                style={ "backgroundColor": "#2A2A3C","marginTop": "10px"},
            ),
            html.Div(id='Compositional-inner-content')
        ]) 
    
    else:
        return html.Div("Unknown tab selected", style=styles)

def create_dumb_graph():
    # Dummy data for settings graph
    x = [1, 2, 3, 4, 5]
    y = [5, 4, 3, 2, 1]

    graph = dcc.Graph(
        figure=go.Figure(
            data=[go.Scatter(x=x, y=y, mode='lines+markers', name='Dumb Line')],
            layout=go.Layout(
                title='Dumb Graph',
                xaxis=dict(title='X Axis'),
                yaxis=dict(title='Y Axis')
            )
        )
    )
    return html.Div([graph])

if __name__ == "__main__":
    app.run(debug=True)
