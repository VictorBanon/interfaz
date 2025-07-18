from pathlib import Path

import dash
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.express as px
from dash import Input, Output, dcc, html


class InterfazData:
    def __init__(self, taxon_list, path_data):
        self.df = pd.read_csv(path_data / "taxonomy.csv")
        self.df_filter = pd.read_csv(path_data / "taxonomy.csv")
        self.levels = taxon_list

        for taxon in taxon_list:
            self.df[f"{taxon}_acp_1"] = np.random.rand(len(self.df[taxon])).tolist()
            self.df[f"{taxon}_acp_2"] = np.random.rand(len(self.df[taxon])).tolist()

        # ✅ Add suppress_callback_exceptions
        self.app = dash.Dash(
            __name__,
            external_stylesheets=[dbc.themes.BOOTSTRAP],
            suppress_callback_exceptions=True,
        )

        sidebar = self.get_sidebar()

        content = html.Div(
            [
                dcc.Tabs(
                    id="tabs",
                    value="tab-PCA",
                    children=[
                        dcc.Tab(label="PCA", value="tab-PCA"),
                        dcc.Tab(label="Structural", value="tab-Structural"),
                        dcc.Tab(label="Kmer", value="tab-Kmer"),
                        dcc.Tab(label="Spatial", value="tab-Spatial"),
                        dcc.Tab(label="Compositional", value="tab-Compositional"),
                    ],
                ),
                html.Div(id="tab-content", style={
                    "padding": "20px",
                    "backgroundColor": "#f0f8ff",
                    "borderRadius": "10px",
                    "boxShadow": "0px 0px 10px rgba(0,0,0,0.1)",
                }),
            ],
            style={"margin-left": "320px", "padding": "20px"},
        )

        self.layout = html.Div(children=[sidebar, content])
        self.app.layout = self.layout
        self.register_callbacks()

    def get_sidebar(self):
        sidebar_list = [
            html.H2("SINTEF", style={"font-size": "28px", "font-weight": "bold", "color": "white"}),
            html.H4("LIACI Context", style={"font-size": "22px", "color": "white"}),
            html.Hr(style={"borderColor": "white"}),
        ]

        for taxon in self.levels:
            list_options = [{"label": i, "value": i} for i in self.df[taxon].dropna().unique()]
            sidebar_list.append(html.Label(taxon, style={"color": "white"}))
            sidebar_list.append(dcc.Dropdown(
                id={"type": "taxonomy-dropdown", "level": taxon},
                options=list_options,
                multi=True,
                style={"backgroundColor": "#e6f2ff", "color": "#003366"},
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
                "boxShadow": "2px 2px 10px rgba(0,0,0,0.3)",
            },
        )

        return sidebar

    def run(self):
        self.app.run(debug=True)

    def register_callbacks(self):
        # ✅ Tab container callback
        @self.app.callback(
            Output("tab-content", "children"),
            Input("tabs", "value"),
        )
        def render_tab_content(tab):
            styles = {"color": "#003366"}

            if tab == "tab-PCA":
                return html.Div([
                    html.H3("PCA Analysis", style=styles),
                    html.P("Select a taxonomic level to visualize ACP values.", style=styles),
                    dcc.Dropdown(
                        id="pca-taxon-dropdown",
                        options=[{"label": t, "value": t} for t in self.levels],
                        value="phylum",
                        style={"width": "300px", "marginBottom": "20px"},
                    ),
                    dcc.Graph(id="pca-scatter-plot"),
                ])
            if tab == "tab-Structural":
                return html.Div([
                    html.H3("Structural", style=styles),
                    dcc.Tabs(
                        id="Structural-inner-tabs",
                        value="Structural-HC",
                        children=[
                            dcc.Tab(label="HA", value="Structural-HA"),
                            dcc.Tab(label="HB", value="Structural-HB"),
                            dcc.Tab(label="HC", value="Structural-HC"),
                        ],
                        style={"marginTop": "10px"},
                    ),
                    html.Div(id="Structural-inner-content"),
                ])
            if tab == "tab-Kmer":
                return html.Div([
                    html.H3("Kmer", style=styles),
                    dcc.Tabs(
                        id="Kmer-inner-tabs",
                        value="Kmer-ratio",
                        children=[
                            dcc.Tab(label="Kmer-ratio", value="Kmer-ratio"),
                            dcc.Tab(label="Kmer-nucleotide", value="Kmer-nucleotide"),
                        ],
                        style={"marginTop": "10px"},
                    ),
                    html.Div(id="Kmer-inner-content"),
                ])
            if tab == "tab-Spatial":
                return html.Div([
                    html.H3("Spatial", style=styles),
                    dcc.Tabs(
                        id="Spatial-inner-tabs",
                        value="Spatial-Replicon",
                        children=[
                            dcc.Tab(label="Spatial Replicon", value="Spatial-Replicon"),
                            dcc.Tab(label="Spatial Region", value="Spatial-Region"),
                            dcc.Tab(label="Spatial IR", value="Spatial-IR"),
                        ],
                        style={"marginTop": "10px"},
                    ),
                    html.Div(id="Spatial-inner-content"),
                ])
            if tab == "tab-Compositional":
                return html.Div([
                    html.H3("Compositional", style=styles),
                    dcc.Tabs(
                        id="Compositional-inner-tabs",
                        value="Compositional-Catalogue",
                        children=[
                            dcc.Tab(label="Compositional Catalogue" , value="Compositional-Catalogue"),
                            dcc.Tab(label="Compositional Philogenie", value="Compositional-Philogenie"),
                        ],
                        style={"marginTop": "10px"},
                    ),
                    html.Div(id="Compositional-inner-content"),
                ])
            return html.Div("Unknown tab selected", style=styles)

        # ✅ Inner content for Structural tab
        @self.app.callback(
            Output("Structural-inner-content", "children"),
            Input("Structural-inner-tabs", "value"),
        )
        def render_structural_inner_content(tab):
            styles = {"color": "#003366"}

            if tab == "Structural-HA" or tab == "Structural-HB" or tab == "Structural-HC":
                children_ = [
                    html.H3("Structural - HC", style=styles),
                    html.P("Graphs will be loaded per replicon (example only)", style=styles),
                ]
                # This is just an example — replace with actual replicons or logic
                replicons = self.df_filter["ID-replicon"].dropna().unique()[:3]  # limit to 3 for demo
                for replicon in replicons:
                    children_.append(dcc.Graph(id=f"pca-scatter-{replicon}", figure=px.scatter(x=[1, 2], y=[2, 3],title=f"{replicon}()")))
                return html.Div(children_)
            return html.Div(f"Content for {tab} not yet implemented.", style=styles)

        # ✅ PCA scatter plot callback
        @self.app.callback(
            Output("pca-scatter-plot", "figure"),
            Input("pca-taxon-dropdown", "value"),
        )
        def update_pca_scatter(taxon):
            x_col = f"{taxon}_acp_1"
            y_col = f"{taxon}_acp_2"

            fig = px.scatter(
                self.df,
                x=x_col,
                y=y_col,
                color=taxon,
                hover_name=self.levels[-1],
                title=f"PCA Scatter for '{taxon}' ACP values",
                labels={x_col: f"{taxon}_acp_1", y_col: f"{taxon}_acp_2"},
            )

            fig.update_layout(
                plot_bgcolor="#f0f8ff",
                paper_bgcolor="#f0f8ff",
                hovermode="closest",
            )
            return fig


# Run the app
if __name__ == "__main__":
    taxon_list = ["superkingdom", "phylum", "class", "order", "family", "genus", "species", "ID-replicon"]
    data_path = Path("~/Documents/GitHub/2024-victor-IRs-Victor/results/12-rep").expanduser()
    interfaz = InterfazData(taxon_list, data_path)
    interfaz.run()
