import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px

# Load your taxonomy data
list_with_taxonomy = pd.read_csv("~/Documents/GitHub/2024-victor-IRs-Victor/results/12-rep/taxonomy.csv") 
taxon_list = ["superkingdom","phylum","class","order","family","genus","species","ID-replicon"]
taxon_levels = ["superkingdom","phylum","class","order","family","genus","species","ID-replicon"]
df = pd.read_csv("data.csv")
list_with_taxonomy_test = list_with_taxonomy[taxon_list]

for taxon in taxon_list:
    list_with_taxonomy_test[f"{taxon}_acp_1"] = np.random.rand(len(list_with_taxonomy_test[taxon])).tolist()  
    list_with_taxonomy_test[f"{taxon}_acp_2"] = np.random.rand(len(list_with_taxonomy_test[taxon])).tolist()  

list_with_taxonomy_test.to_csv("list_with_taxonomy_test")

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Sidebar construction
sidebar_list = [
    html.H2("SINTEF", style={"font-size": "28px", "font-weight": "bold", "color": "white"}),
    html.H4("LIACI Context", style={"font-size": "22px", "color": "white"}),
    html.Hr(style={"borderColor": "white"}),  
] 

for taxon in taxon_list:
    list_options = [{"label": i, "value": i} for i in list_with_taxonomy[taxon].dropna().unique()]
    sidebar_list.append(html.Label(taxon, style={"color": "white"}))
    sidebar_list.append(dcc.Dropdown(
        id=f"sidebar-{taxon}-dropdown",
        options=list_options,
        multi=True,
        style={"backgroundColor": "#e6f2ff", "color": "#003366"}
    ))
    sidebar_list.append(html.Br())



sidebar = html.Div(
    sidebar_list,
    style={
        "position": "fixed",
        "top": 0,
        "left": 0,
        "bottom": 0,
        "width": "300px",
        "padding": "20px",
        "background": "linear-gradient(180deg, #2e8b57, #3cb371)",
        "overflowY": "scroll",
        "boxShadow": "2px 2px 10px rgba(0,0,0,0.3)"
    },
)

# Main content with outer tabs
content = html.Div(
    [
        dcc.Tabs(
            id="tabs",
            value="tab-graph",
            children=[
                dcc.Tab(label="PCA", value="tab-PCA", style={"backgroundColor": "#b3d9ff"}, selected_style={"backgroundColor": "#3399ff", "color": "white"}),
                dcc.Tab(label="Structural", value="tab-Structural", style={"backgroundColor": "#b3d9ff"}, selected_style={"backgroundColor": "#3399ff", "color": "white"}),
                dcc.Tab(label="Kmer", value="tab-Kmer", style={"backgroundColor": "#b3d9ff"}, selected_style={"backgroundColor": "#3399ff", "color": "white"}),
                dcc.Tab(label="Spatial", value="tab-Spatial", style={"backgroundColor": "#b3d9ff"}, selected_style={"backgroundColor": "#3399ff", "color": "white"}),
                dcc.Tab(label="Compositional", value="tab-Compositional", style={"backgroundColor": "#b3d9ff"}, selected_style={"backgroundColor": "#3399ff", "color": "white"}),
            ],
            colors={"border": "#ccc", "primary": "#3399ff", "background": "#f8f9fa"},
        ),
        html.Div(id="tab-content", style={"padding": "20px", "backgroundColor": "#f0f8ff", "borderRadius": "10px", "boxShadow": "0px 0px 10px rgba(0,0,0,0.1)"})
    ],
    style={
        "margin-left": "320px",
        "padding": "20px",
    }
)

# Layout
app.layout = html.Div(children=[sidebar, content])

# Callback for outer tab selection
@app.callback(
    dash.dependencies.Output("tab-content", "children"),
    [dash.dependencies.Input("tabs", "value")]
)
def render_tab_content(tab):
    styles = {"color": "#003366"}

    if tab == "tab-PCA":
        return html.Div([
            html.H3("PCA Analysis", style=styles),
            html.P("Select a taxonomic level to visualize ACP values.", style=styles),
            dcc.Dropdown(
                id="pca-taxon-dropdown",
                options=[{"label": t, "value": t} for t in taxon_levels],
                value="phylum",  # default
                style={"width": "300px", "marginBottom": "20px"}
            ),
            dcc.Graph(id="pca-scatter-plot")
        ])
    
    elif tab == "tab-Structural":
        return html.Div([
            html.H3("Structural", style=styles),
            dcc.Tabs(
                id='Structural-inner-tabs',
                value='Structural-HC',
                children=[
                    dcc.Tab(label='HA', value='Structural-HA'), 
                    dcc.Tab(label='HB', value='Structural-HB'), 
                    dcc.Tab(label='HC', value='Structural-HC'), 
                ],
                style={"marginTop": "10px"},
            ),
            html.Div(id='Structural-inner-content')
        ]) 
    
    elif tab == "tab-Kmer":
        return html.Div([
            html.H3("Kmer", style=styles),
            dcc.Tabs(
                id='Kmer-inner-tabs',
                value='Kmer-ratio',
                children=[
                    dcc.Tab(label='Kmer-ratio', value='Kmer-ratio'), 
                    dcc.Tab(label='Kmer-nucleotide', value='Kmer-nucleotide'),  
                ],
                style={"marginTop": "10px"},
            ),
            html.Div(id='Kmer-inner-content')
        ]) 
    
    elif tab == "tab-Spatial":
        return html.Div([
            html.H3("Spatial", style=styles),
            dcc.Tabs(
                id='Spatial-inner-tabs',
                value='Spatial-Replicon',
                children=[
                    dcc.Tab(label='Spatial Replicon', value='Spatial-Replicon'), 
                    dcc.Tab(label='Spatial Region', value='Spatial-Region'), 
                    dcc.Tab(label='Spatial IR', value='Spatial-IR'), 
                ],
                style={"marginTop": "10px"},
            ),
            html.Div(id='Spatial-inner-content')
        ]) 
    
    elif tab == "tab-Compositional":
        return html.Div([
            html.H3("Compositional", style=styles),
            dcc.Tabs(
                id='Compositional-inner-tabs',
                value='Compositional-Catalogue',
                children=[
                    dcc.Tab(label='Compositional Catalogue' , value='Compositional-Catalogue'), 
                    dcc.Tab(label='Compositional Philogenie', value='Compositional-Philogenie'),  
                ],
                style={"marginTop": "10px"},
            ),
            html.Div(id='Compositional-inner-content')
        ]) 
    
    else:
        return html.Div("Unknown tab selected", style=styles)
# Callback for outer tab selection
@app.callback(
    dash.dependencies.Output("Structural-inner-content", "children"),
    [dash.dependencies.Input("Structural-inner-tabs", "value")]
)
def render_tab_content(tab):
    styles = {"color": "#003366"}

    if tab == "Structural-HC":
        children_ = [
            html.H3("PCA Analysis", style=styles),
            html.P("Select a taxonomic level to visualize ACP values.", style=styles), 
        ]
        for replicon in list_with_taxonomy["ID-replicon"]:
            children_.append(dcc.Graph(id=f"pca-scatter-{replicon}"))
        return html.Div(children_)  
    else:
        return html.Div("Unknown tab selected", style=styles)
    
@app.callback(
    dash.dependencies.Output("pca-scatter-plot", "figure"),
    [dash.dependencies.Input("pca-taxon-dropdown", "value")]
)  
def update_pca_scatter(taxon):
    x_col = f"{taxon}_acp_1"
    y_col = f"{taxon}_acp_2"

    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        color=taxon,  # color by the "value" column
        hover_name="#Organism Name",
        title=f"PCA Scatter for '{taxon}' ACP values",
        labels={x_col: f"{taxon}_acp_1", y_col: f"{taxon}_acp_2"},
    )

    fig.update_layout(
        plot_bgcolor="#f0f8ff",
        paper_bgcolor="#f0f8ff",
        hovermode="closest"
    )

    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
