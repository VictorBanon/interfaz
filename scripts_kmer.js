/*
 * TODO:
 * [x] Align columns
 * [x] Make <select> options in Card4 (taxonomy) update on other selections
 * [ ] Better error handling when there are no plots
 * [ ] Change all Plot references for Card (be consistent!)
 * [x] make FOLDER_TREE and import instead of hardcode
 * [x] weird things append when loading data: file are suspect to be uploaded multiple times
 *
 */

function capitalize(s) {
  return String(s[0]).toUpperCase() + String(s).slice(1);
}

const DATA_DIR = "data";

const TAXONOMIC_ORDER = [
  "kingdom",
  "phylum",
  "class",
  "order",
  "family",
  "genus",
  "species"
];
const TAXONOMIC_ORDER_EXPANDED = [
  ...TAXONOMIC_ORDER,
  "id",
  "id-replicon"
];

const BORDER_SHAPE = [
  { type: "line", x0: 0, y0: 1, x1: 1, y1: 1, xref: "paper", yref: "paper", line: { color: "black", width: 2 } },
  { type: "line", x0: 0, y0: 0, x1: 1, y1: 0, xref: "paper", yref: "paper", line: { color: "black", width: 2 } },
  { type: "line", x0: 0, y0: 0, x1: 0, y1: 1, xref: "paper", yref: "paper", line: { color: "black", width: 2 } },
  { type: "line", x0: 1, y0: 0, x1: 1, y1: 1, xref: "paper", yref: "paper", line: { color: "black", width: 2 } },
];

// Simple utility for WIP features
function renderNotFoundHTML(elementId) {
  document.getElementById(elementId).innerHTML = `
    <div style="
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      height: 100%;
      width: 100%;
      font-size: 1.2em;">
      <div style="font-size: 2em;">&#9888;</div>
      <p>Data Not Found</p>
    </div>
  `;
}

const card1 = document.getElementById('card_1');
const tabButton1 = card1.querySelectorAll('.tab-button');
const card2 = document.getElementById('card_2');
const tabButton2 = card2.querySelectorAll('.tab-button');

// Tab switch click listeners for cards 1 and 2
const tabButtons = [tabButton1, tabButton2];
tabButtons.forEach(buttonGroup => {
  buttonGroup.forEach(button => {
    button.addEventListener('click', () => {
      buttonGroup.forEach(btn => btn.classList.remove('active'));
      button.classList.add('active');
    });
  });
});

// Top-left
async function buildDropdownsCard1() {
  const categoryDropdown = document.getElementById("categoryDropdown");
  const filterDropdown = document.getElementById("filterDropdown");

  fetch(`${DATA_DIR}/taxonomy_values.json`)
    .then(response => response.json())
    .then(data => {
      const taxonKeys = Object.keys(data);

      categoryDropdown.innerHTML = '';
      for (const taxon of taxonKeys) {
        const option = document.createElement("option");
        option.value = taxon;
        option.textContent = taxon;
        categoryDropdown.appendChild(option);
      }

      categoryDropdown.addEventListener("change", function() {
        const selectedTaxon = categoryDropdown.value;
        filterDropdown.innerHTML = "";

        if (data[selectedTaxon]) {
          const values = data[selectedTaxon];

          values.forEach(val => {
            const option = document.createElement("option");
            option.value = val;
            option.textContent = val;
            filterDropdown.appendChild(option);
          });

          if (values.length === 1) {
            filterDropdown.value = values[0];
            filterDropdown.dispatchEvent(new Event("change"));
          } else if (values.length > 1) {
            filterDropdown.value = values[0];
          }
        }
      });

      if (taxonKeys.length > 0) {
        categoryDropdown.value = taxonKeys[0];
        categoryDropdown.dispatchEvent(new Event('change'));
      }
    })
    .catch(err => {
      const msg = "Error loading taxonomy_values.json"
      console.error(msg, err);
      alert(msg);
    });
}

// Recursive iteration
function findFilePath(tree, target, path = []) {
  for (const key in tree) {
    const newPath = [...path, key];
    if (key === target) {
      return newPath;
    }
    const result = findFilePath(tree[key], target, newPath);
    if (result) return result;
  }
  return null;
}

async function findFilePathFromJSON(target) {
  return fetch(`${DATA_DIR}/structure.json`)
    .then(response => {
      if (!response.ok) throw new Error(`HTTP error ${response.status}`);
      return response.json();
    })
    .then(tree => {
      return findFilePath(tree, target);
    })
    .catch(err => {
      console.error("Failed to load or parse structure.json:", err);
      return null;
    });
}

function renderPlotCard1(acpCSVPath) {
  Papa.parse(acpCSVPath, {
    download: true,
    header: true,
    complete: function(results) {
      const xValues = [];
      const yValues = [];
      const pointData = [];

      results.data.forEach(row => {
        xValues.push(parseFloat(row.PC1));
        yValues.push(parseFloat(row.PC2)); 
        pointData.push(row);
      });

      const hoverLabels = pointData.map(row =>
        `PC1: ${row.PC1}<br>PC2: ${row.PC2}<br>ID: ${row.ID}`
      );

      Plotly.newPlot('plot1', [{
        type: 'scatter',
        mode: 'markers',
        x: xValues,
        y: yValues,
        text: hoverLabels,
        hoverinfo: 'text',
        marker: { size: 10 }
      }], {
        title: 'ACP',
        // left, right etc. margins
        margin: {
          l: 0,
          r: 0,
          t: 30,
          b: 0
        },
      }, {
        responsive: true
      });

      // Add click handler to card1 that updates plot3
      document.getElementById('plot1').on('plotly_click', function(eventData) {
        const clickedRow = pointData[eventData.points[0].pointIndex];
        const idReplicon = clickedRow.ID;
        const id = idReplicon.replace(clickedRow.Replicons_type + "_", "");
        const { tabLeftValue, tabRightValue } = getCurrentSelections();
        const heatmapPath = `${DATA_DIR}/${id}/analysis/${idReplicon}_ratio_cod_vs_non_6mer.csv`;

        renderHeatmapFromCSVPathAndId(heatmapPath, idReplicon);
      });

    }
  });
}

function renderPlotCard1_max(acpCSVPath) {
  Papa.parse(acpCSVPath, {
    download: true,
    header: true,
    complete: function(results) {
      const xValues = [];
      const yValues = [];
      const zValues = [];
      const pointData = [];

      const colorScale = [
        [0.0, "blue"],
        [0.333, "white"],
        [0.666, "red"],
        [1.0, "black"]
      ]; 

      results.data.forEach(row => {
        xValues.push(parseFloat(row.size));
        yValues.push(parseFloat(row.gap));
        const z = parseFloat(row.z);
        const logZ = Math.log10(z > 0 ? z : 1e-6); // avoid log(0) or negative values

        zValues.push(logZ);
        pointData.push(row);
      });  

            
      const hoverLabels = pointData.map(row =>
        `size: ${row.size}<br>gap: ${row.gap}<br>value: ${row.z}<br>ID: ${row.ID}`
      );
      var trace1 = { 
        x: xValues, 
        y: yValues, 
        mode: 'markers', 
        name: 'points', 
        text: hoverLabels,
        marker: {  
          size: 20,  
          cmin: -1,
          cmax: 2,
          color: zValues,
          colorscale: colorScale,
        }, 
        type: 'scatter' 
      }; 

      var trace2 = { 
        x: xValues, 
        y: yValues, 
        name: 'density', 
        ncontours: 20, 
        colorscale: "Greys", 
        showscale: false, 
        type: 'histogram2dcontour' 
      };

      var trace3 = {

        x: xValues, 
        name: 'x density', 
        marker: {color: 'rgba(4, 92, 48, 1)'}, 
        yaxis: 'y2', 
        type: 'histogram' 
      };

      var trace4 = { 
        y: yValues, 
        name: 'y density', 
        marker: {color: 'rgba(6, 81, 131, 1)'}, 
        xaxis: 'x2', 
        type: 'histogram' 
      };

      var data = [trace2,trace1, trace3, trace4];

      var layout = { 
        xaxis: { range: [3, 20], title: 'Arm Length' },
        yaxis: { range: [0, 20], title: 'Gap Length' },
        showlegend: false, 
        autosize: true,  
        margin: {t: 50}, 
        hovermode: 'closest', 
        bargap: 0, 
        xaxis: { 
          domain: [0, 0.85], 
          showgrid: false, 
          zeroline: false 
        },

        yaxis: { 
          domain: [0, 0.85], 
          showgrid: false, 
          zeroline: false 
        },

        xaxis2: { 
          domain: [0.85, 1], 
          showgrid: false, 
          zeroline: false 
        },

        yaxis2: { 
          domain: [0.85, 1], 
          showgrid: false, 
          zeroline: false 
        }

      };

      Plotly.newPlot('plot1', data, layout);
      

      // Add click handler to card1 that updates plot3
      document.getElementById('plot1').on('plotly_click', function(eventData) {
        const clickedRow = pointData[eventData.points[0].pointIndex];
        const id = clickedRow.ID;
        const idReplicon = clickedRow["ID-replicon"];
        const { tabLeftValue, tabRightValue } = getCurrentSelections();
        const heatmapPath = `${DATA_DIR}/${id}/analysis/${idReplicon}_${tabRightValue}_${tabLeftValue}.csv`;

        renderHeatmapFromCSVPathAndId(heatmapPath, idReplicon);
      });
    }
  });
}

// Top-right
function renderPlotsCard2(acpCSVPathPlot2, plotName, titleText) {
  Papa.parse(acpCSVPathPlot2, {
    download: true,
    complete: function(results) {
      const matrix = results.data.filter(row => row.length > 0);
      const z = matrix.slice(1).map(row =>
        row.slice(1).map(value => parseFloat(value))
      );

      const colorScale = [
        [0.0, "blue"],
        [0.5, "white"],
        [1.0, "red"]
      ];

      Plotly.newPlot(plotName, [{
        z: z,
        type: 'heatmap',
        colorscale: colorScale,
        zmin: -1,
        zmax: 1,
        colorbar: {
          tickvals: [-1, 0, 1],
          ticktext: [-1, 0, 1],
        }
      }], {
        title: {
          text: titleText,
          font: { size: 18 }
        },
        xaxis: {
          title: { text: "Arm Length" }
        },
        yaxis: {
          title: { text: "Gap Length" },
          tickmode: "linear",
          dtick: 2
        },
        template: "plotly_white",
        shapes: BORDER_SHAPE
      });
    }
  });
}

// Top-left
function buildPlotCard1() {
  // console.log("[BPC1] called buildPlotCard1");
  const { tabLeftValue, tabRightValue, categoryValue, filterValue,graphValue } = getCurrentSelections();

  findFilePathFromJSON(filterValue).then(pathArray => {
    if (!pathArray) {
      console.warn(`folderPath not found with filterValue=${filterValue}. Returning early.`);
      return;
    }

    const folderPath = pathArray.join("/"); // This is not the whole path!
    // console.log(`folderPath=${folderPath} found with filterValue=${filterValue}.`);

    const rootPath = `${DATA_DIR}/philogenie/${folderPath}`; 

    const parameters = [filterValue]
      .map(String)
      .join("_");

    const acpCSVPath = `${rootPath}/${graphValue}_kmer_${parameters}.csv`; 

    if (graphValue === "acp") {
      renderPlotCard1(acpCSVPath);
    }
    if (graphValue === "max") {
      renderPlotCard1_max(acpCSVPath);
    }
    const acp1CSVPath = `${rootPath}/PC0_ratio_cod_vs_non_cod_${parameters}.csv`
    const acp2CSVPath = `${rootPath}/PC1_ratio_cod_vs_non_cod_${parameters}.csv`

    // Check that path exists and display notFoundError in case of failure!
    function checkAndRender(csvPath, elementId, plotLabel) {
      fetch(csvPath, { method: 'HEAD' })
        .then(response => {
          if (response.ok) {
            renderPlotsCard2(csvPath, elementId, plotLabel);
          } else {
            console.warn(`CSV not found: ${csvPath}`);
            renderNotFoundHTML(elementId);
          }
        })
    }

    checkAndRender(acp1CSVPath, "plot2_1", "PC1");
    checkAndRender(acp2CSVPath, "plot2_2", "PC2");
  }).catch(error => {
    console.error("Error resolving pathArray:", error);
  });
}

// Bottom-left
function renderHeatmapFromCSVPathAndId(heatmapCSVPath, id) {
  Papa.parse(heatmapCSVPath, {
    download: true,
    header: true,
    complete: function(heatmapResults) {
      renderHeatmapFromCSV(heatmapResults, id);
    },
  });
}

// Bottom-left
function renderHeatmapFromCSV(results, id) {
  document.getElementById('plot3').innerHTML = ""; 
    
  const colors = {
    "6-mer": "#023047",
    "Inverted repeat": "#219ebc",
    "Palindromes": "#ffb703"
  };  
  const df_plot = results.data.filter(row => !isNaN(row.cod) && !isNaN(row.non));
  // Get unique categories
  const categories = [...new Set(df_plot.map(row => row.color))];

  const traces = [];

  categories.forEach(category => {
    const cat_data = df_plot.filter(row => row.color === category);
    const x = cat_data.map(d => parseFloat(d.cod));
    const y = cat_data.map(d => parseFloat(d.non));
    const hoverText = cat_data.map(d => d.Item);

    // Scatter points
    traces.push({
      type: 'scatter',
      mode: 'markers',
      name: category,
      x,
      y,
      text: hoverText,
      marker: { color: colors[category], opacity: 0.7 },
      xaxis: 'x',
      yaxis: 'y'
    });

    // Horizontal histogram (top)
    traces.push({
      type: 'histogram',
      name: `${category} (x)`,
      x,
      marker: { color: colors[category] },
      opacity: 0.5,
      showlegend: false,
      histnorm: 'probability density',
      xaxis: 'x2',
      yaxis: 'y2'
    });

    // Vertical histogram (right)
    traces.push({
      type: 'histogram',
      name: `${category} (y)`,
      y,
      marker: { color: colors[category] },
      opacity: 0.5,
      showlegend: false,
      histnorm: 'probability density',
      xaxis: 'x3',
      yaxis: 'y3'
    });
  });

  // Add reference dashed lines at ±1
  [-1, 1].forEach(val => {
    traces.push({
      type: 'scatter',
      mode: 'lines',
      x: [val, val],
      y: [-4, 4],
      line: { color: 'black', dash: 'dash' },
      showlegend: false,
      xaxis: 'x',
      yaxis: 'y'
    });
    traces.push({
      type: 'scatter',
      mode: 'lines',
      x: [-4, 4],
      y: [val, val],
      line: { color: 'black', dash: 'dash' },
      showlegend: false,
      xaxis: 'x',
      yaxis: 'y'
    });
  });

  // Add red diagonal
  traces.push({
    type: 'scatter',
    mode: 'lines',
    x: [-4, 4],
    y: [-4, 4],
    line: { color: 'red', dash: 'solid' },
    name: 'Diagonal',
    xaxis: 'x',
    yaxis: 'y'
  });

  // Layout
  const layout = { 
    margin: {
      l: 0,
      r: 0,
      t: 30,
      b: 0
    },
    grid: {
      rows: 2,
      columns: 2,
      pattern: 'independent',
      roworder: 'top to bottom'
    },
    xaxis: {
      domain: [0, 0.8],
      range: [-4, 4],
      tickvals: [-4, -3, -2, -1, 0, 1, 2, 3, 4],
      showgrid: true,
      gridcolor: 'lightgray'
    },
    yaxis: {
      domain: [0, 0.8],
      range: [-4, 4],
      tickvals: [-4, -3, -2, -1, 0, 1, 2, 3, 4],
      showgrid: true,
      gridcolor: 'lightgray'
    },
    xaxis2: {
      domain: [0, 0.8],
      range: [-4, 4],
      anchor: 'y2',
      showgrid: false
    },
    yaxis2: {
      domain: [0.8, 1.0], 
      anchor: 'x2',
      showgrid: false
    },
    xaxis3: {
      domain: [0.8, 1.0], 
      anchor: 'y3',
      showgrid: false
    },
    yaxis3: {
      domain: [0, 0.8],
      range: [-4, 4],
      anchor: 'x3',
      showgrid: false
    },
    barmode: 'overlay', 
    showlegend: true,
    template: 'simple_white'
  };

  // Plot it
  Plotly.newPlot('plot3', traces, layout);
}

// get all important variables
function getCurrentSelections() {
  const activeTopLeftTab = document.querySelector('#tabs_top_left .tab-button.active');
  const activeTopRightTab = document.querySelector('#card_2 .tab-button.active');

  // all | cod | non
  const tabLeftValue = activeTopLeftTab.getAttribute('data-tab');
  // hc
  const tabRightValue = activeTopRightTab.getAttribute('data-tab');

  const categoryDropdown = document.getElementById('categoryDropdown');
  const filterDropdown = document.getElementById('filterDropdown');
  const graphDropdown = document.getElementById('graphDropdown');

  const categoryValue = categoryDropdown.value;
  const filterValue = filterDropdown.value;
  const graphValue = graphDropdown.value;

  const selections = {
    tabLeftValue,
    tabRightValue,
    categoryValue,
    filterValue,
    graphValue
  };

  // console.log('Current Selections:', selections);

  return selections;
}

// Bottom-left default
function buildPlotCard3() {
  document.getElementById('plot3').innerHTML = `
    <div style="
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      height: 100%;
      width: 100%;
      font-size: 1.2em;">
      <div style="font-size: 2em;">&#8593;</div>
      <p>Click on a chromosome to display</p>
    </div>
  `;
}

// Bottom-right
function buildTaxonomyCard() {
  function parseTaxonomyCSV(csv) {
    const result = Papa.parse(csv.trim(), { header: true });
    return result.data.map(row => [
      row.superkingdom || '',
      row.phylum || '',
      row.class || '',
      row.order || '',
      row.family || '',
      row.genus || '',
      row.species || '',
      row.ID || '',
      row['ID-replicon'] || ''
    ]);
  }

  $(document).ready(function() {
    $.get(`${DATA_DIR}/taxonomy.csv`)
      .done(function(csvText) {
        const tableData = parseTaxonomyCSV(csvText);

        const cols = TAXONOMIC_ORDER_EXPANDED.map(order => {
          const columnDefinition = {
            title: capitalize(order),
          };

          // Show full word on hover (by setting the CSS title)
          // * Note that the word ellipsis is controlled by the CSS statically
          columnDefinition.createdCell = function(cell, cellData) {
            cell.setAttribute('title', cellData);
          };

          return columnDefinition;
        });

        const table = $('#taxonomy').DataTable({
          data: tableData,
          columns: cols,
          paging: true,
          pageLength: 10,
          initComplete: function() {
            const api = this.api();
            const filterHeaders = $('.filters th');

            // Add filtering options on top
            api.columns().every(function() {
              const column = this;
              const colIndex = column.index();

              // Create <select> element with default "All" option
              const $select = $('<select><option value="">All</option></select>');

              // Append the <select> to the corresponding filter header cell
              filterHeaders.eq(colIndex)
                .empty()
                .append($select);

              // Populate the <select> with unique, sorted values from the column
              column.data().unique().sort().each(function(value) {
                $select.append(`<option value="${value}">${value}</option>`);
              });

              // When the user changes the <select>, filter the column
              $select.on('change', function() {
                const selection = $.fn.dataTable.util.escapeRegex($(this).val());
                const searchRegex = selection ? `^${selection}$` : '';
                column.search(searchRegex, true, false).draw();
              });

              // Update <select> options for all columns
              $select.on('change', function() {
                const filteredRows = api.rows({ search: 'applied' }); // !!!
                api.columns().every(function() {
                  const otherColumn = this;
                  const otherColIndex = otherColumn.index();

                  const $otherSelect = filterHeaders.eq(otherColIndex).find('select');
                  const currentValue = $otherSelect.val();

                  // Collect unique values for this column from filtered rows only
                  const uniqueValues = [];
                  filteredRows.every(function() {
                    const rowData = this.data();
                    uniqueValues.push(rowData[otherColIndex]);
                  });

                  // These are the updated <select> options
                  const uniqueSorted = [...new Set(uniqueValues)].filter(Boolean).sort();

                  // Clear and rebuild the <select>
                  $otherSelect.empty().append('<option value="">All</option>');
                  uniqueSorted.forEach(val => {
                    $otherSelect.append(`<option value="${val}">${val}</option>`);
                  });

                  // If the current value is still valid, keep it — otherwise reset
                  if (currentValue && uniqueSorted.includes(currentValue)) {
                    $otherSelect.val(currentValue);
                  } else {
                    $otherSelect.val('');
                    otherColumn.search('', true, false);
                  }
                });

                api.draw();
              });
            });
          }
        });

        // Row (card4) click: update plot3
        $('#taxonomy tbody').on('click', 'tr', function() {
          const rowData = table.row(this).data();
          if (!rowData || rowData.length < 9) return;

          const idReplicon = rowData[8];
          const id = rowData[7];
          const { tabLeftValue, tabRightValue } = getCurrentSelections();
          const heatmapPath = `${DATA_DIR}/${String(id)}/analysis/${idReplicon}_ratio_cod_vs_non_6mer.csv`;
          renderHeatmapFromCSVPathAndId(heatmapPath, idReplicon);
        });
      });
  });
}



document.querySelectorAll('#tabs_top_left .tab-button').forEach(button => {
  button.addEventListener('click', function() {
    console.log("Top left tab clicked — rebuilding Plot Card 1");
    buildPlotCard1();
  });
});

document.querySelectorAll('#tabs_top_right .tab-button').forEach(button => {
  button.addEventListener('click', function() {
    console.log("Top right tab clicked — rebuilding Plot Card 2");
    buildPlotCard1();
  });
});

// === Resize active plot on tab switch ===
const observer = new MutationObserver(() => {
  document.querySelectorAll('.tab-content.active div[id^="plot"]').forEach(plot => {
    Plotly.Plots.resize(plot);
  });
});
document.querySelectorAll('.tab-content').forEach(tab => {
  observer.observe(tab, { attributes: true, attributeFilter: ['class'] });
});

// main entrypoint
document.addEventListener("DOMContentLoaded", async function() {
  await buildDropdownsCard1();

  // These two should go into buildDropdownsCard1
  document.getElementById('categoryDropdown').addEventListener('change', function() {
    buildPlotCard1();
  });
  document.getElementById('filterDropdown').addEventListener('change', function() {
    buildPlotCard1();
  });
  document.getElementById('graphDropdown').addEventListener('change', function() {
    buildPlotCard1();
  });

  buildPlotCard1();
  buildPlotCard3();
  buildTaxonomyCard();
});

