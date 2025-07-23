import numpy as np
import pandas as pd

import plotly.graph_objs as go
import plotly.express as px

def plotly_hc(species:str, zone:str, result_obs:pd.DataFrame)->None:
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
        title=f"{species} - {zone}",
        xaxis_title="Arm Length",
        yaxis_title="Gap Length",
        yaxis={
        "tickmode": "linear",
        "tick0": result_obs.index.min(),  # start of ticks
        "dtick": 2,  # step size of 2
        },
        margin=dict(l=0, r=0, t=30, b=0),  # remove all margins
        autosize=True,
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

def plotly_hc_acp(species:str, zone:str, result_obs:pd.DataFrame)->None:
    """Plot hc with plotly."""
    colorscale = [
        [0, "blue"],     
        [0.5, "white"],    
        [1.0, "red"],    
    ] 

    # Format original values as text for display in cells
    text_vals = result_obs.round(2).astype(str) 

    # Create the heatmap
    fig = go.Figure(data=go.Heatmap(
        z=result_obs,
        x=result_obs.columns,  # Column labels
        y=result_obs.index,    # Row labels
        colorscale=colorscale,
        zmin=-1,
        zmax=1,
        #text=text_vals.values,
        texttemplate="%{text}",  # display cell values
        hovertemplate="Value: %{text}<br>Gap: %{y}<br>Arm: %{x}<extra></extra>", 
        colorbar={
            "tickvals": [-1, 0, 1, ],
            "ticktext": ["-1", "0", "1", ]
        },
    ))

    # Add layout details
    fig.update_layout(
        title=f"{species} - {zone}",
        xaxis_title="Arm Length",
        yaxis_title="Gap Length",
        # paper_bgcolor= "#2e3b2e",  
        # font=dict(
        #     family="Arial",
        #     size=16,
        #     color= "#e0e6db",  # any HEX, RGB, or named color
        # ),
        yaxis={
        "tickmode": "linear",
        "tick0": result_obs.index.min(),  # start of ticks
        "dtick": 2,  # step size of 2
        },
        margin=dict(l=0, r=0, t=30, b=0),  # remove all margins
        autosize=True,
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
        # paper_bgcolor= "#2e3b2e",  
        # font=dict(
        #     family="Arial",
        #     size=16,
        #     color= "#e0e6db",  # any HEX, RGB, or named color
        # ),
    )
    fig.update_layout(
        xaxis={"range": [x_min*1.1, x_max*1.1]},
        yaxis={"range": [y_min*1.1, y_max*1.1]},
    )

    return fig
