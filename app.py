from pathlib import Path

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html
import plotly.graph_objects as go
from layout_helpers import get_main_and_subtabs, get_structural_subtabs
from plot import plotly_hc, plotly_acp_plot,plotly_hc_acp

# Load your taxonomy data
output_dir = Path("data")
list_with_taxonomy = pd.read_csv(filepath_or_buffer=output_dir/"taxonomy.csv")
df = list_with_taxonomy

columns = list(df.columns)
to_remove = ["full_name", "Replicons_name", "Replicons_type"]
columns = [col for col in columns if col not in to_remove]

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Sample figure
sample_fig = px.scatter(x=[1, 2, 3], y=[4, 1, 6])

# Color theme
bio_colors = {
    "background": "#2e3b2e",   # dark olive/forest green background
    "accent": "#4f6f52",       # rich muted green
    "text": "#e0e6db",         # light sage/cream text for contrast
    "border": "#3f5241",        # darker desaturated border tone
}

#define plots
pca_df = pd.read_csv(output_dir/"philogenie"/"Bacteria"/"acp_all.csv")
top_figure   = plotly_acp_plot("all",pca_df,columns[0])
boton_figure = go.Figure()  #plotly_hc
# sub_left__figure = plotly_hc
# sub_right_figure = plotly_hc 

#Define dropdowns
dropdown_rows = []
# Iterate over columns two at a time
for i in range(0, len(columns), 2):
    row = dbc.Row([
        dbc.Col(
            html.Div([
                html.Label(f"{columns[i]}", style={"color": bio_colors["text"]}),
                dcc.Dropdown(
                    id = f"{columns[i]}-dropdown",
                    options=df[columns[i]].unique(), 
                ),
            ]),
            width=6,
        ),
        dbc.Col(
            html.Div([
                html.Label(f"{columns[i+1]}", style={"color": bio_colors["text"]}),
                dcc.Dropdown(
                    id = f"{columns[i+1]}-dropdown",
                    options=df[columns[i+1]].unique(),  
                ),
            ]),
            width=6,
        ) if i + 1 < len(columns) else dbc.Col(),  # Empty col if odd number of columns
    ])
    dropdown_rows.append(row)


# App layout
app.layout = html.Div(style={
    "height": "100vh",
    "width": "100vw",
    "margin": "0",
    "padding": "0",
    "backgroundColor": bio_colors["background"],
    "overflow": "hidden",
}, children=[

    dbc.Row(style={"height": "100%"}, children=[

        # Sidebar
        dbc.Col(html.Div("sidebar", style={
            "height": "100%",
            "padding": "20px",
            "background-color": bio_colors["accent"],
            "color": "white",
            "font-weight": "bold",
            "border-radius": "0px",
        }), width=2, style={"height": "100%"}),

        # Main content
        dbc.Col([
            # Top Section (50%)
            dbc.Row([
                dbc.Col(
                    [dcc.Tabs(id="part-tabs",
                        value="all",
                        children=[
                        dcc.Tab(label="All", value="all"),
                        dcc.Tab(label="Coding", value="coding"),
                        dcc.Tab(label="Non Coding", value="non_coding"), 
                    ]),
                    dcc.Graph(id="plot_i", figure=top_figure,style={'height': '500px'}  )],
                    width=6
                    ),
                dbc.Col([
                    dcc.Tabs(id="main-tabs",
                        value="structural-tab",
                        children=[
                        dcc.Tab(label="Structural", value="structural-tab"),
                        dcc.Tab(label="Kmer", value="kmer-tab"),
                        dcc.Tab(label="Spatial", value="spatial-tab"),
                        dcc.Tab(label="Compositional", value="compositional-tab"),
                    ]),
                    html.Div(id="subtab-container"),
                ], width=6),
            ], style={"height": "50%", "padding": "10px"}),

            # Bottom Section (50%)
            dbc.Row([
                dbc.Col(
                    dcc.Graph(id="plot_ii", figure=go.Figure(), style={"height": "100%"}), 
                    width=6),
                dbc.Col(dropdown_rows, width=6, style={"padding": "10px", "overflowY": "auto"}),
            ], style={"height": "50%", "padding": "10px"}),
        ], width=10, style={"height": "100%", "padding": "10px"}),
    ]),
])



@app.callback(
    Output("subtab-container", "children"),
    Input("main-tabs", "value"),
)
def update_tabs(tab):
    return get_main_and_subtabs(tab)

@app.callback(
    Output("structural-container", "children"),
    Input("structural-sub-tabs", "value"),
)
def update_structural_subtabs(tab=None):
    if tab is None:
        return dash.no_update
    return get_structural_subtabs(tab)

list_relations = []
for i in range(len(columns)-1):
    list_relations.append([f"{columns[i+1]}-dropdown",f"{columns[i]}-dropdown"])    
list_relations.append(["value-dropdown","taxon-dropdown"])    

for relation in list_relations:
    @app.callback(
        Output(relation[0], 'options'),
        Input( relation[0], 'id'),
        Input( relation[1], 'value'),
        Input( relation[1], 'id')
    )
    def update_sub_dropdown(id_I,category,id_II): 
        name_I  = id_I.split( "-dropdown")[0]
        name_II = id_II.split("-dropdown")[0]
        if name_II == "taxon": 
            return df[category].unique()
        else: 
            if category is None :
                return df[name_I].unique()
            else:
                return df[df[name_II]==category][name_I].unique()

@app.callback(
    Output('ID-replicon-dropdown', 'value'),
    Input('plot_i', 'clickData')
)
def update_dropdown(clickData):
    if clickData is None:
        return None
    # Extract label from customdata 
    return clickData["points"][0]["customdata"][1]

@app.callback(
    Output('plot_ii', 'figure'),
    Input('ID-replicon-dropdown', 'value'), 
    Input('part-tabs', 'value'), 
)
def update_graph(selected_value,zone):
    if selected_value is None:
        return go.Figure()
    else:
        print(selected_value)

        row = df[df["ID-replicon"] == selected_value].iloc[0]

        species = row["full_name"] 
        path_file = output_dir/row["ID"]/"analysis"/f"{row["ID-replicon"]}_hc_{zone}.csv"
        print(path_file)
        result_obs = pd.read_csv(path_file,index_col=0)

        fig =  plotly_hc(species, zone, result_obs)

        return fig
    

@app.callback(
    Output('plot_i', 'figure'),
    Output('plot_pc1', 'figure'),
    Output('plot_pc2', 'figure'),
    Input('value-dropdown', 'value'), 
    Input('taxon-dropdown', 'value'), 
    Input('part-tabs', 'value'),  
)
def update_graph(value,taxon,zone):
    if value is None:
        return go.Figure()
    else:

        row = df[df[taxon] == value].iloc[0]  

        path_file = output_dir/"philogenie"

        for column in columns:
            path_file = path_file/str(row[column] )
            if column==taxon:
                break

        dic_zone={"all":"all","coding":"cod","non_coding":"non"}

        zone_ = dic_zone[zone]

        path_file_acp = path_file/f"acp_{zone_}.csv" 
        result_obs = pd.read_csv(path_file_acp) 
        fig_acp =  plotly_acp_plot(zone_,result_obs,taxon)

        path_file_pcI = path_file/f"PC0_{taxon}_{value}_hc_{zone_}.csv" 
        result_obs = pd.read_csv(path_file_pcI,index_col=0) 
        fig_pcI =  plotly_hc_acp(value,zone_,result_obs)
        
        path_file_pcII = path_file/f"PC1_{taxon}_{value}_hc_{zone_}.csv"
        result_obs = pd.read_csv(path_file_pcII,index_col=0) 
        fig_pcII =  plotly_hc_acp(value,zone_,result_obs)

        return fig_acp,fig_pcI,fig_pcII 

if __name__ == "__main__":
    app.run(debug=True)
