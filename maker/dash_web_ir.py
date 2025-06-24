import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# Initialize the app with a Bootstrap theme for styling
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Sidebar layout (left panel)
sidebar = html.Div(
    [
        html.H2("SINTEF", style={"font-size": "24px", "font-weight": "bold"}),
        html.H4("LIACI Context", style={"font-size": "20px"}),
        html.Hr(),

        html.Label("Choose Inspection(s)"),
        dcc.Dropdown(
            options=[
                {"label": "Aberfoyle I on 2022-02-21", "value": "inspection1"},
                # Add more options here
            ],
            multi=True,
            value=["inspection1"]
        ),

        html.Br(),
        html.Label("Telemetry Similarities"),
        dcc.Slider(0, 5, step=1, value=2),

        html.Label("Visual Similarities"),
        dcc.Slider(0, 20, step=1, value=8),

        html.Label("Image Quality"),
        dcc.Slider(0, 15, step=1, value=6),

        html.Br(),
        html.Label("Extras"),
        dbc.Checklist(
            options=[
                {"label": "mosaics", "value": "mosaics"},
                {"label": "clusters", "value": "clusters"}
            ],
            value=["clusters"],
            inline=False
        ),

        html.Br(),
        html.Label("Inspection criteria"),
        dbc.Checklist(
            options=[
                {"label": "marine growth", "value": "marine_growth"},
                {"label": "paint peel", "value": "paint_peel"},
                {"label": "corrosion", "value": "corrosion"},
                {"label": "defect", "value": "defect"}
            ],
            value=[],
            inline=False
        ),

        html.Br(),
        html.Label("Classifications"),
        dbc.Checklist(
            options=[
                {"label": "anode", "value": "anode"},
                {"label": "propeller", "value": "propeller"},
                {"label": "bilge keel", "value": "bilge_keel"},
                {"label": "sea chest grating", "value": "sea_chest_grating"},
                {"label": "lover board valves", "value": "lover_board_valves"}
            ],
            value=[],
            inline=False
        ),

        html.Br(),
        html.P("Publication Date: 30.08.2022"),
        html.P(
            "License: Creative Commons Attribution Non Commercial Share Alike 4.0",
            style={"font-size": "12px"}
        ),
    ],
    style={
        "position": "fixed",
        "top": 0,
        "left": 0,
        "bottom": 0,
        "width": "300px",
        "padding": "20px",
        "background-color": "#f8f9fa",
        "overflow-y": "scroll"
    },
)

# Content layout (main panel with tabs)
content = html.Div(
    [
        dcc.Tabs(id="tabs", value="tab-graph", children=[
            dcc.Tab(label="Graph View", value="tab-graph"),
            dcc.Tab(label="Clusters", value="tab-clusters"),
            dcc.Tab(label="Histograms", value="tab-histograms"),
            dcc.Tab(label="Tables", value="tab-tables"),
            dcc.Tab(label="Headings", value="tab-headings"),
        ]),

        html.Div(id="tab-content", style={"padding": "20px", "margin-left": "320px"})
    ]
)

# App layout
app.layout = html.Div([sidebar, content])

# Callback to display content based on selected tab
@app.callback(
    dash.dependencies.Output("tab-content", "children"),
    [dash.dependencies.Input("tabs", "value")]
)
def render_tab_content(tab):
    if tab == "tab-graph":
        return html.Div([
            html.H3("Graph View"),
            html.P("Here the network graph would be displayed.")
            # You can embed a plotly network graph here
        ])
    elif tab == "tab-clusters":
        return html.Div([
            html.H3("Clusters"),
            html.P("Cluster visualization would go here.")
        ])
    elif tab == "tab-histograms":
        return html.Div([
            html.H3("Histograms"),
            html.P("Histograms would go here.")
        ])
    elif tab == "tab-tables":
        return html.Div([
            html.H3("Tables"),
            html.P("Data tables would go here.")
        ])
    elif tab == "tab-headings":
        return html.Div([
            html.H3("Headings"),
            html.P("Headings or other info.")
        ])
    else:
        return html.Div("Unknown tab selected")

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
