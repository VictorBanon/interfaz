# rst_updater.py

import re
from pathlib import Path

def rst_individual(
    rst_file_path,
    plot1_data,
    plot2_data,
    click_event,
    heatmap_data
):
    rst_path = Path(rst_file_path)
    content = rst_path.read_text(encoding='utf-8')

    # --- Plot 1 ---
    content = re.sub(
        r"Plotly\.newPlot\('plotly-div1'.*?\}\]\);",
        plot1_data.strip(),
        content,
        flags=re.DOTALL
    )

    # --- Plot 2 ---
    content = re.sub(
        r"var trace2 = \{.*?Plotly\.newPlot\('plotly-div2', \[trace2\]\);",
        plot2_data.strip(),
        content,
        flags=re.DOTALL
    )

    # --- Click event ---
    content = re.sub(
        r"var plot2Div = document\.getElementById\('plotly-div2'\);.*?window\.open\(url, '_blank'\);",
        click_event.strip(),
        content,
        flags=re.DOTALL
    )

    # --- Heatmap ---
    content = re.sub(
        r"var xLabels = \[.*?Plotly\.newPlot\('plotly-div3', \[heatmap\]\);",
        heatmap_data.strip(),
        content,
        flags=re.DOTALL
    )

    # Save
    rst_path.write_text(content, encoding='utf-8')
    print(f"RST file '{rst_file_path}' updated.")

 

# Define your new content
plot1_data = """
Plotly.newPlot('plotly-div1', [{
    x: [10, 20, 30],
    y: [1, 4, 9],
    mode: 'lines+markers',
    type: 'scatter'
}]);
"""

plot2_data = """
var trace2 = {
    x: [10, 20, 30],
    y: [5, 15, 25],
    mode: 'lines+markers',
    type: 'scatter',
    text: ['A', 'B', 'C'],
    hoverinfo: 'text'
};

Plotly.newPlot('plotly-div2', [trace2]);
"""

click_event = """
var plot2Div = document.getElementById('plotly-div2');
plot2Div.on('plotly_click', function(data) {
    var pointIndex = data.points[0].pointIndex;
    var label = trace2.text[pointIndex];

    var url = 'https://example.com/page/' + encodeURIComponent(label);
    console.log('Opening URL:', url);
    window.open(url, '_blank');
});
"""

heatmap_data = """
var xLabels = ['X1', 'X2'];
var yLabels = ['Y1', 'Y2'];
var zValues = [
    [5, 10],
    [15, 20]
];

var heatmap = {
    x: xLabels,
    y: yLabels,
    z: zValues,
    type: 'heatmap',
    colorscale: 'Cividis'
};

Plotly.newPlot('plotly-div3', [heatmap]);
"""

# Call the update function
update_rst(
    'my_tabs.rst',
    plot1_data,
    plot2_data,
    click_event,
    heatmap_data
)
