from pathlib import Path

def taxon_rst(file_path:Path,link_list,taxon)->None:

    rst_file = f"""{taxon}  
==============

.. toctree::
    :maxdepth: 2
    :caption: Contents:

"""
    rst_file += "\n".join(link_list) 

    rst_file += """
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
    """
    rst_file += """
    <!-- Top Level Tabs -->
    <div class="tab">
      <button class="tablinks" onclick="openTopTab(event, 'TabI')" id="defaultTopOpen">Structural</button>
      <button class="tablinks" onclick="openTopTab(event, 'TabII')">Kmer</button>
      <button class="tablinks" onclick="openTopTab(event, 'TabIII')">Spatial</button>
      <button class="tablinks" onclick="openTopTab(event, 'TabIV')">Compositional</button>
    </div>
    """
    rst_file += """
    <!-- Content for Structural -->
    <div id="TabI" class="tabcontent">

      <!-- Second Level Tabs -->
      <div class="tab">
        <button class="tablinks2" onclick="openSecondTab(event, 'Plot1')" id="defaultSecondOpen">Ratio plot</button>  
      </div>
      <div id="Plot1" class="tabcontent" style="height:600px;">
        <div id="plotly-div1" style="width:100%; height:100%;"></div>
      </div> 

    </div>
    """
    rst_file += """
    <!-- Content for Kmer -->
    <div id="TabII" class="tabcontent">
      <p>Here is some other content for Kmer. You can add more stuff here.</p>
    </div>
    """
    rst_file += """
    <!-- Content for Spatial -->
    <div id="TabIII" class="tabcontent">
      <p>Here is some other content for Spatial. You can add more stuff here.</p>
    </div>
    """
    rst_file += """
    <!-- Content for Compositional-->
    <div id="TabIV" class="tabcontent">
      <p>Here is some other content for Compositional. You can add more stuff here.</p>
    </div> 
    """
    rst_file += """
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
    </script>
    """
 
    # Write text to the file 
    file_path.write_text(rst_file, encoding='utf-8')
    print(file_path) 