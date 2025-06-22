Tabs con plots
==============

.. toctree::
    :maxdepth: 2
    :caption: Contents:

    data/index

.. raw:: html

    <style>
    .tab {
      overflow: hidden;
      border-bottom: 1px solid #ccc;
    }
    .tab button {
      background-color: inherit;
      float: left;
      border: none;
      outline: none;
      cursor: pointer;
      padding: 10px 16px;
      transition: background-color 0.3s;
      font-size: 16px;
    }
    .tab button:hover {
      background-color: #ddd;
    }
    .tab button.active {
      background-color: #ccc;
    }
    .tabcontent {
      display: none;
      padding: 12px 0px;
      border-top: none;
    }
    </style>

    <div class="tab">
      <button class="tablinks" onclick="openTab(event, 'Plot1')" id="defaultOpen">Plot 1</button>
      <button class="tablinks" onclick="openTab(event, 'Plot2')">Plot 2</button>
      <button class="tablinks" onclick="openTab(event, 'Plot3')">Plot 3 (Heatmap CSV)</button>
    </div>

    <div id="Plot1" class="tabcontent" style="height:600px;">
      <div id="plotly-div1" style="width:100%; height:100%;"></div>
    </div>
    <div id="Plot2" class="tabcontent" style="height:600px;">
      <div id="plotly-div2" style="width:100%; height:100%;"></div>
    </div>
    <div id="Plot3" class="tabcontent" style="height:600px;">
      <div id="plotly-div3" style="width:100%; height:100%;"></div>
    </div>

    <script src="https://cdn.plot.ly/plotly-2.30.0.min.js"></script>
    <script src="https://d3js.org/d3.v5.min.js"></script>

    <script>
    function openTab(evt, tabName) {
        var i, tabcontent, tablinks;
        tabcontent = document.getElementsByClassName("tabcontent");
        for (i = 0; i < tabcontent.length; i++) {
            tabcontent[i].style.display = "none";
        }
        tablinks = document.getElementsByClassName("tablinks");
        for (i = 0; i < tablinks.length; i++) {
            tablinks[i].className = tablinks[i].className.replace(" active", "");
        }
        var tab = document.getElementById(tabName);
        tab.style.display = "block";
        evt.currentTarget.className += " active";

        var plotDiv = tab.querySelector('div[id^="plotly-div"]');
        if (plotDiv) {
            setTimeout(() => {
                Plotly.Plots.resize(plotDiv);
            }, 100);
        }
    }

    document.getElementById("defaultOpen").click();

    // Plot 1
    Plotly.newPlot('plotly-div1', [{
        x: [1, 2, 3, 4, 5],
        y: [4, 1, 2, 6, 3],
        mode: 'lines+markers',
        type: 'scatter'
    }]);

    // Plot 2
    var trace2 = {
        x: [1, 2, 3, 4, 5],
        y: [2, 5, 3, 4, 7],
        mode: 'lines+markers',
        type: 'scatter',
        text: ['Python', 'JavaScript', 'HTML', 'CSS', 'Java'],  // etiquetas
        hoverinfo: 'text'
    };

    Plotly.newPlot('plotly-div2', [trace2]);

    // Capturar click en Plot 2
    var plot2Div = document.getElementById('plotly-div2');

    plot2Div.on('plotly_click', function(data) {
        var pointIndex = data.points[0].pointIndex;
        var label = trace2.text[pointIndex];

        // Construir link a Wikipedia
        var url = 'https://es.wikipedia.org/wiki/' + encodeURIComponent(label);

        console.log('Abriendo:', url);
        window.open(url, '_blank');  // abrir en nueva pestaña
    });

    // Heatmap CSV
    d3.csv('../_static/heatmap.csv').then(function(rows) {
        var x = Object.keys(rows[0]).slice(1);
        var y = rows.map(row => row['Label']);
        var z = rows.map(row => x.map(c => +row[c]));

        var heatmap = {
            x: x,
            y: y,
            z: z,
            type: 'heatmap',
            colorscale: 'Viridis'
        };

        Plotly.newPlot('plotly-div3', [heatmap]);
    }).catch(function(error) {
        console.error('Error loading CSV:', error);
    });
    </script>
