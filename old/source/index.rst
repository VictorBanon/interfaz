Tabs con plots
==============

.. toctree::
    :maxdepth: 2 

    data/Bacteria/index

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

    <!-- Top Level Tabs -->
    <div class="tab">
      <button class="tablinks" onclick="openTopTab(event, 'TabI')" id="defaultTopOpen">Tab A (With Plots)</button>
      <button class="tablinks" onclick="openTopTab(event, 'TabII')">Tab B (Other Content)</button>
      <button class="tablinks" onclick="openTopTab(event, 'TabIII')">Tab B (Other Content)</button>
      <button class="tablinks" onclick="openTopTab(event, 'TabIV')">Tab B (Other Content)</button>
    </div>

    <!-- Content for Tab A -->
    <div id="TabI" class="tabcontent">

      <!-- Second Level Tabs inside TabA -->
      <div class="tab">
        <button class="tablinks2" onclick="openSecondTab(event, 'Plot1')" id="defaultSecondOpen">Ratio plot</button> 
        <button class="tablinks2" onclick="openSecondTab(event, 'Plot2')">Heatmap</button>
      </div>

      <div id="Plot1" class="tabcontent" style="height:600px;">
        <div id="plotly-div1" style="width:100%; height:100%;"></div>
      </div>
      <div id="Plot2" class="tabcontent" style="height:600px;">
        <div id="plotly-div2" style="width:100%; height:100%;"></div>
      </div> 

    </div>

    <!-- Content for Tab B -->
    <div id="TabII" class="tabcontent">
      <p>Here is some other content for Tab B. You can add more stuff here.</p>
    </div>
    <!-- Content for Tab B -->
    <div id="TabIII" class="tabcontent">
      <p>Here is some other content for Tab B. You can add more stuff here.</p>
    </div>
    <!-- Content for Tab B -->
    <div id="TabIV" class="tabcontent">
      <p>Here is some other content for Tab B. You can add more stuff here.</p>
    </div>

    <script src="https://cdn.plot.ly/plotly-2.30.0.min.js"></script>

    <script>
    // Top Level Tabs
    function openTopTab(evt, tabName) {
        var i, tabcontent, tablinks;
        tabcontent = document.querySelectorAll('div.tabcontent');
        for (i = 0; i < tabcontent.length; i++) {
            tabcontent[i].style.display = "none";
        }
        tablinks = document.getElementsByClassName("tablinks");
        for (i = 0; i < tablinks.length; i++) {
            tablinks[i].className = tablinks[i].className.replace(" active", "");
        }
        document.getElementById(tabName).style.display = "block";
        evt.currentTarget.className += " active";
    }

    // Second Level Tabs
    function openSecondTab(evt, tabName) {
        var i, tabcontent, tablinks;
        tabcontent = document.querySelectorAll('#TabI > .tabcontent');
        for (i = 0; i < tabcontent.length; i++) {
            tabcontent[i].style.display = "none";
        }
        tablinks = document.getElementsByClassName("tablinks2");
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

    // Initialize both levels
    document.getElementById("defaultTopOpen").click();
    setTimeout(() => {
        document.getElementById("defaultSecondOpen").click();
    }, 100);

    // Plot 1 
    var trace2 = {
        x: [1, 2, 3, 4, 5],
        y: [2, 5, 3, 4, 7],
        mode: 'lines+markers',
        type: 'scatter',
        text: ['Actinobacteria', 'Firmicutes', 'Proteobacteria'],
        hoverinfo: 'text'
    };

    Plotly.newPlot('plotly-div1', [trace2]);

    // Click event Plot 2
    var plot2Div = document.getElementById('plotly-div1');
    plot2Div.on('plotly_click', function(data) {
        var pointIndex = data.points[0].pointIndex;
        var label = trace2.text[pointIndex];

        // Build relative path to target file
        var relativePath = 'data/' + label + '/index.html';

        // Get current folder path
        var basePath = window.location.pathname.substring(0, window.location.pathname.lastIndexOf('/')) + '/';

        // Final URL
        var url = 'file://' + basePath + relativePath;

        console.log('Opening:', url);
        window.open(url, '_blank');
    });

    // Inline Heatmap (Plot 2)
    var xLabels = ['A', 'B', 'C', 'D'];
    var yLabels = ['Row 1', 'Row 2', 'Row 3'];
    var zValues = [
        [1, 20, 30, 50],
        [20, 1, 60, 80],
        [30, 60, 1, 90]
    ];

    var heatmap = {
        x: xLabels,
        y: yLabels,
        z: zValues,
        type: 'heatmap',
        colorscale: 'Viridis'
    };

    Plotly.newPlot('plotly-div2', [heatmap]);
    </script>