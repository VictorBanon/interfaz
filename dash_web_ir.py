import pandas as pd
import numpy as np
import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from pathlib import Path
from dash.exceptions import PreventUpdate

# Load your taxonomy data
output_dir = Path("/home/banongav/Documents/GitHub/2024-victor-IRs-Victor/results/12-rep/")
output_dir = Path("/home/vic/2024-victor-IRs-Victor/results/Snakemake")
#
list_with_taxonomy = pd.read_csv(filepath_or_buffer=output_dir/"taxonomy.csv")
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

list_options_gen = [
    dcc.Dropdown(
        id=f"sidebar-taxon-gen-dropdown",
        options=columns[:-2],
        multi=False,
        style={ 
                "backgroundColor": "#1E1E2D",
                "color": "#6896C4",
                "padding": "5px"}
    )  ,
    dcc.Dropdown(
        id=f"sidebar-value-gen-dropdown",
        options=[],
        multi=False,
        style={ 
                "backgroundColor": "#1E1E2D",
                "color": "#6896C4",
                "padding": "5px"}
    )  
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
                dbc.NavLink(
                    ["General"],
                    href="#", id="nav-general", n_clicks=0
                ),  
                # Collapsible sub-items for Individual
                html.Div(
                    id="gen-subitems",
                    children=list_options_gen,
                    style={"display": "none"}  # hidden by default
                ),
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
    dcc.Store(id='gen-collapse-store', data=False),  # stores whether individual submenu is open
    sidebar,
    main_content
])

# Callback to update sidebar-value-gen-dropdown based on sidebar-taxon-gen-dropdown
@app.callback(
    Output("sidebar-value-gen-dropdown", "options"),
    Input("sidebar-taxon-gen-dropdown", "value")
)
def update_value_dropdown(selected_taxa):
    if selected_taxa is None:
        return []  # or return columns to show all options
    # Here you can apply filtering logic if needed
    # For now, we'll just return all except selected_taxa
    return [{"label": taxon, "value": taxon}
            for taxon in df[selected_taxa].unique()]

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
    

@app.callback(
    Output("gen-subitems", "style"),
    Output("gen-collapse-store", "data"),
    Input("nav-individual", "n_clicks"),
    Input("nav-general", "n_clicks"),
    Input("nav-debrief", "n_clicks"),
    Input("nav-settings", "n_clicks"),
    State("gen-collapse-store", "data")
)
def toggle_individual(individual_clicks, general_clicks,debrief_clicks, settings_clicks, is_open):
    ctx = dash.callback_context
    if not ctx.triggered:
        # On app load, submenu is collapsed
        return {"display": "none"}, False

    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_id == "nav-general":
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

    content_general = html.Div(
        [
            dcc.Tabs(
                id="tabs-gen",
                value="tab-gen-Structural",
                children=[ 
                    dcc.Tab(label="Structural", value="tab-gen-Structural", style={"backgroundColor": "#2A2A3C"}, selected_style={"backgroundColor": "#50506D", "color": "white"}),
                    dcc.Tab(label="Kmer", value="tab-gen-Kmer", style={"backgroundColor": "#2A2A3C"}, selected_style={"backgroundColor": "#50506D", "color": "white"}),
                    dcc.Tab(label="Spatial", value="tab-gen-Spatial", style={"backgroundColor": "#2A2A3C"}, selected_style={"backgroundColor": "#50506D", "color": "white"}),
                    dcc.Tab(label="Compositional", value="tab-gen-Compositional", style={"backgroundColor": "#2A2A3C"}, selected_style={"backgroundColor": "#50506D", "color": "white"}),
                ],
                colors={"border": "#ccc", "primary": "#50506D", "background": "#2A2A3C"},
            ),
            html.Div(id="tab-gen-content", style={"padding": "20px", "backgroundColor": "#2A2A3C", "boxShadow": "0px 0px 10px rgba(0,0,0,0.1)"})
        ],
        style={ 
            "padding": "20px",
        }
    ) 
    content_individual = html.Div(
        [
            dcc.Tabs(
                id="tabs",
                value="tab-Structural",
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
        "nav-general": content_general,
        "nav-individual": content_individual,
        "nav-settings": "Lorem Ipsum"
    }

    content = content_map.get(button_id, "No content available.")

    if isinstance(content, str):
        return [html.H2(button_id.replace("nav-", "").capitalize()), html.P(content)]
    else:
        # If content is a component like a graph
        return [html.H2(button_id.replace("nav-", "").capitalize()), content]



# Callback for outer tab selection
# TODO(VICTOR): https://dash.plotly.com/advanced-callbacks
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

# Callback for outer tab selection
# TODO(VICTOR): https://dash.plotly.com/advanced-callbacks
@app.callback(
    Output("tab-gen-content", "children"),
    [Input("tabs-gen", "value")]
)
def render_tab_content_gen(tab): 
    styles = {"color": "#003366"}

    if tab == "tab-gen-Structural":
        return html.Div([ 
            dcc.Tabs(
                id='gen-Structural-inner-tabs',
                value='Structural-HC',
                children=[
                    dcc.Tab(label='HA', value='Structural-HA',style={ "backgroundColor": "#2A2A3C"},selected_style={"backgroundColor": "#50506D"}), 
                    dcc.Tab(label='HB', value='Structural-HB',style={ "backgroundColor": "#2A2A3C"},selected_style={"backgroundColor": "#50506D"}), 
                    dcc.Tab(label='HC', value='Structural-HC',style={ "backgroundColor": "#2A2A3C"},selected_style={"backgroundColor": "#50506D"}), 
                ],
                style={ "backgroundColor": "#2A2A3C","marginTop": "10px"},
            ),
            html.Div(id='Structural-gen-inner-content')
        ]) 
    
    elif tab == "tab-gen-Kmer":
        return html.Div([ 
            dcc.Tabs(
                id='gen-Kmer-inner-tabs',
                value='Kmer-ratio',
                children=[
                    dcc.Tab(label='Kmer-ratio', value='Kmer-ratio',style={ "backgroundColor": "#2A2A3C"},selected_style={"backgroundColor": "#50506D"}), 
                    dcc.Tab(label='Kmer-nucleotide', value='Kmer-nucleotide',style={ "backgroundColor": "#2A2A3C"},selected_style={"backgroundColor": "#50506D"}),  
                ],
                style={ "backgroundColor": "#2A2A3C","marginTop": "10px"},
            ),
            html.Div(id='gen-Kmer-inner-content')
        ]) 
    
    elif tab == "tab-gen-Spatial":
        return html.Div([ 
            dcc.Tabs(
                id='gen-Spatial-inner-tabs',
                value='Spatial-Replicon',
                children=[
                    dcc.Tab(label='Spatial Replicon', value='Spatial-Replicon',style={ "backgroundColor": "#2A2A3C"},selected_style={"backgroundColor": "#50506D"}), 
                    dcc.Tab(label='Spatial Region', value='Spatial-Region',style={ "backgroundColor": "#2A2A3C"},selected_style={"backgroundColor": "#50506D"}), 
                    dcc.Tab(label='Spatial IR', value='Spatial-IR',style={ "backgroundColor": "#2A2A3C"},selected_style={"backgroundColor": "#50506D"}), 
                ],
                style={ "backgroundColor": "#2A2A3C","marginTop": "10px"},
            ),
            html.Div(id='gen-Spatial-inner-content')
        ]) 
    
    elif tab == "tab-gen-Compositional":
        return html.Div([ 
            dcc.Tabs(
                id='gen-Compositional-inner-tabs',
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


# ✅ Inner content for Structural tab
@app.callback(
    Output("Structural-inner-content", "children"),
    Input("Structural-inner-tabs", "value")
)
def render_structural_inner_content(tab):
    styles = {"color": "#003366"}

    if tab == "Structural-HC":
        children_ = [
            html.H3("Structural - HC", style=styles),
            html.P("Graphs will be loaded per replicon (example only)", style=styles), 
        ] 
        # This is just an example — replace with actual replicons or logic 
        for index, row in df[:3].iterrows(): 
            list_hc = []
            for zone in ["all","coding","non_coding"]: 
                try:
                    result_obs = pd.read_csv(
                        output_dir/row["ID"]/ "analysis" / f"{row['ID-replicon']}_hc_{zone}.csv",
                        index_col=0
                    ) 
                    # Append the plot 
                    list_hc.append(
                        dcc.Graph(
                            id=f"pca-scatter-{zone}-{row['ID-replicon']}",
                            figure=plotly_hc(row,zone,result_obs)
                        )
                    ) 
                except: 
                    # Append the plot 
                    list_hc.append("Error"                    ) 
            children_.append(html.Div(
                style={'display': 'flex', 'justifyContent': 'space-around'},
                children= list_hc
            )
            ) 

        return html.Div(children_)   
    else:
        return html.Div(f"Content for {tab} not yet implemented.", style=styles)



# ✅ Inner content for Structural tab
@app.callback(
    Output("Structural-gen-inner-content", "children"),
    Input("gen-Structural-inner-tabs", "value"), 
    Input("sidebar-value-gen-dropdown", "value"),
    Input("sidebar-taxon-gen-dropdown", "value")
)
def render_structural_inner_content(tab,value,taxon):
    styles = {"color": "#003366"}

    if tab == "Structural-HC":
        children_ = [
            html.H3("Structural - HC", style=styles),
            html.P("Graphs will be loaded per replicon (example only)", style=styles), 
        ]  
        list_hc = []
        for zone in ["all","cod","non"]:  
            path = output_dir/"philogenie"
            print(taxon,value)
            df_tmp=df[df[taxon]==value].iloc[0]
            for i in range(columns.index(taxon)+1): 
                print(df_tmp[columns[i]])
                path = path/df_tmp[columns[i]]
            path = path/f"acp_{zone}.csv"
            result_obs = pd.read_csv(path)#,index_col=0)   
            print(result_obs)
            # Append the plot 
            list_hc.append(
                dcc.Graph( 
                    figure=plotly_acp_plot(zone,result_obs,taxon)
                )
            )  
        children_.append(html.Div(
            style={'display': 'flex', 'width': '40%'},
            children= list_hc
        )
        ) 

        return html.Div(children_)   
    else:
        return html.Div(f"Content for {tab} not yet implemented.", style=styles)


def plotly_hc(row:pd.Series, zone:str, result_obs:pd.DataFrame)->None:
    """Plot hc with plotly."""
    colorscale = [
        [0.0, "blue"],     # log10(0.1)
        [0.333, "white"],  # log10(1)
        [0.666, "red"],    # log10(10)
        [1.0, "black"],    # log10(100)
    ]

    # Convert data to log scale for proper color mapping
    z_log = np.log10(result_obs)


    # Format original values as text for display in cells
    text_vals = result_obs.round(2).astype(str)

    # Define custom Plotly colorscale
    colorscale = [
        [0.0, "blue"],
        [0.333, "white"],
        [0.666, "red"],
        [1.0, "black"],
    ]

    # Create the heatmap
    fig = go.Figure(data=go.Heatmap(
        z=z_log,
        x=result_obs.columns,  # Column labels
        y=result_obs.index,    # Row labels
        colorscale=colorscale,
        zmin=-1,
        zmax=2,
        #text=text_vals.values,
        texttemplate="%{text}",  # display cell values
        hovertemplate="Value: %{text}<br>Gap: %{y}<br>Arm: %{x}<extra></extra>",
        colorbar={
            "tickvals": [-1, 0, 1, 2],
            "ticktext": ["10⁻¹", "10⁰", "10¹", "10²"],
            "title": "Log Scale",
        },
    ))

    # Add layout details
    fig.update_layout(
        title=f"{row["species"]} - {zone}",
        xaxis_title="Arm Length",
        yaxis_title="Gap Length",
        yaxis={
        "tickmode": "linear",
        "tick0": result_obs.index.min(),  # start of ticks
        "dtick": 2,  # step size of 2
        },  
        template="plotly_white", 
            shapes=[
        # Top border
        {"type": "line", "xref": "paper", "yref": "paper", "x0": 0, "y0": 1, "x1": 1, "y1": 1,
             "line": {"color": "black", "width": 2}},
        # Bottom border
        {"type": "line", "xref": "paper", "yref": "paper", "x0": 0, "y0": 0, "x1": 1, "y1": 0,
             "line": {"color": "black", "width": 2}},
        # Left border
        {"type": "line", "xref": "paper", "yref": "paper", "x0": 0, "y0": 0, "x1": 0, "y1": 1,
             "line": {"color": "black", "width": 2}},
        # Right border
        {"type": "line", "xref": "paper", "yref": "paper", "x0": 1, "y0": 0, "x1": 1, "y1": 1,
             "line": {"color": "black", "width": 2}},
    ],
    )

 
    return fig

import plotly.express as px

def plotly_acp_plot(i_name:str, pca_df:pd.DataFrame,taxon)->None:
    """Plot with Plotly the ACP."""
    # Prepare data for Plotly
    pca_df["Explained Variance 1"] = "?"#f"{pca.explained_variance_ratio_[0] * 100:.2f}%"
    pca_df["Explained Variance 2"] = "?"#f"{pca.explained_variance_ratio_[1] * 100:.2f}%" 

    # Create the Plotly scatter plot
    fig = px.scatter(
        pca_df,
        x="PC1",
        y="PC2",
        color=taxon,
        symbol="Type",
        hover_data=[taxon,"ID"],
        labels={
            "PC1": "Principal Component 1 (?)",#{pca.explained_variance_ratio_[0] * 100:.2f}%)",
            "PC2": "Principal Component 2 (?)",#{pca.explained_variance_ratio_[1] * 100:.2f}%)",
        },
        title=f"PCA {i_name}",
        template="plotly_white",  # Removes the grey background
    )

    # Increase marker size
    fig.update_traces(marker={"size": 12})

    # Get axis range for proper cross-lines
    x_min, x_max = pca_df["PC1"].min(), pca_df["PC1"].max()
    y_min, y_max = pca_df["PC2"].min(), pca_df["PC2"].max()

    # Add custom black axes at x=0 and y=0
    fig.add_shape(type="line",
                  x0=-100, x1=100,
                  y0=0, y1=0,
                  line={"color": "black", "width": 2})
    fig.add_shape(type="line",
                  x0=0, x1=0,
                  y0=-100, y1=100,
                  line={"color": "black", "width": 2})

    # Update layout
    fig.update_layout(
        xaxis={
            "title": "Principal Component 1 (?)",#{pca.explained_variance_ratio_[0] * 100:.2f}%)",
            "zeroline": False,
        },
        yaxis={
            "title": "Principal Component 2 (?)",#{pca.explained_variance_ratio_[1] * 100:.2f}%)",
            "zeroline": False,
        },
        margin={"t": 50, "b": 50, "l": 50, "r": 50},
        showlegend=True,
        legend_title="color",
    )
    fig.update_layout(
        xaxis={"range": [x_min*1.1, x_max*1.1]},
        yaxis={"range": [y_min*1.1, y_max*1.1]},
    ) 

    return fig


if __name__ == "__main__":
    app.run(debug=True)
