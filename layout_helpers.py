from pathlib import Path

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import dcc, html
from plot import plotly_hc_acp


# Load your taxonomy data
output_dir = Path("/home/vic/2024-victor-IRs-Victor/results/Snakemake")
list_with_taxonomy = pd.read_csv(filepath_or_buffer=output_dir/"taxonomy.csv")
df = list_with_taxonomy

columns = list(df.columns)
to_remove = ["full_name", "Replicons_name", "Replicons_type"]
columns = [col for col in columns if col not in to_remove]

# Color theme
bio_colors = {
    "background": "#2e3b2e",   # dark olive/forest green background
    "accent": "#4f6f52",       # rich muted green
    "text": "#e0e6db",         # light sage/cream text for contrast
    "border": "#3f5241",        # darker desaturated border tone
}

def get_main_and_subtabs(tab_value):
    if tab_value == "structural-tab":
        return (
            [dcc.Tabs(
                id="structural-sub-tabs",
                value="hc-tab",
                children=[
                    dcc.Tab(label="HA", value="ha-tab"),
                    dcc.Tab(label="HB", value="hb-tab"),
                    dcc.Tab(label="HC", value="hc-tab"),
                ],
            ),
            html.Div(id="structural-container", style={"height": "33vh"})]
        )
    if tab_value == "kmer-tab":
        return (
            dcc.Tabs(
                id="kmer-sub-tabs",
                value="sub-a",
                children=[
                    dcc.Tab(label="Subtab A", value="sub-a"),
                    dcc.Tab(label="Subtab B", value="sub-b"),
                ],
            )
        )
    if tab_value == "spatial-tab":
        return (
            dcc.Tabs(
                id="spatial-sub-tabs",
                value="sub-a",
                children=[
                    dcc.Tab(label="Subtab A", value="sub-a"),
                    dcc.Tab(label="Subtab B", value="sub-b"),
                ],
            )
        )
    if tab_value == "compositional-tab":
        return (
            dcc.Tabs(
                id="compositional-sub-tabs",
                value="sub-a",
                children=[
                    dcc.Tab(label="Subtab A", value="sub-a"),
                    dcc.Tab(label="Subtab B", value="sub-b"),
                ],
            )
        )
    return html.Div()

def get_structural_subtabs(tab_value):
    if tab_value == "hc-tab":
        # Example plots
        pca_df_1 = pd.read_csv(output_dir/"philogenie"/"Bacteria"/"PC0_superkingdom_Bacteria_hc_all.csv",index_col=0)
        fig1 = plotly_hc_acp("Bacteria","all",pca_df_1)
        pca_df_2 = pd.read_csv(output_dir/"philogenie"/"Bacteria"/"PC1_superkingdom_Bacteria_hc_all.csv",index_col=0)
        fig2 = plotly_hc_acp("Bacteria","all",pca_df_2)

        dropdown_taxons = [
            html.Div([
                html.Label("Taxon", style={"color": bio_colors["text"]}),
                dcc.Dropdown(
                    id = "taxon-dropdown",
                    value=columns[0],
                    options= columns[:-2],
                ),
            ]),
            html.Div([
                html.Label("Value", style={"color": bio_colors["text"]}),
                dcc.Dropdown(
                    id = "value-dropdown",
                    value=df[columns[0]].unique()[0],
                    options=df[columns[0]].unique(),
                ),
            ]),
            ]

        return dbc.Row([
            dbc.Col(dropdown_taxons, style={"height": "100%"}),
            dbc.Col(dcc.Graph(id="plot_pc1",figure=fig1, style={"height": "100%"}), style={"height": "100%"}),
            dbc.Col(dcc.Graph(id="plot_pc2",figure=fig2, style={"height": "100%"}), style={"height": "100%"}),
        ], style={"height": "100%"})
    return html.Div() 