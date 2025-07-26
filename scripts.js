const card1 = document.getElementById('card_1');
const tabButton1 = card1.querySelectorAll('.tab-button');
const card2 = document.getElementById('card_2');
const tabButton2 = card2.querySelectorAll('.tab-button');

// Tab click listeners
tabButton1.forEach(button => {
  button.addEventListener('click', () => {
    const target = button.getAttribute('data-tab');
    tabButton1.forEach(btn => btn.classList.remove('active'));
    button.classList.add('active');
  });
});

// Tab click listeners
tabButton2.forEach(button => {
  button.addEventListener('click', () => {
    const target = button.getAttribute('data-tab');
    tabButton2.forEach(btn => btn.classList.remove('active'));
    button.classList.add('active');
    updatePlotCard2(target);
  });
});

const FOLDER_TREE = {
  "Bacteria": {
    "Proteobacteria": {
      "Betaproteobacteria": {
        "Neisseriales": {
          "Neisseriaceae": {
            "Simonsiella": {}
          }
        },
        "Burkholderiales": {
          "Burkholderiaceae": {
            "Burkholderia": {
              "Burkholderia cenocepacia": {}
            }
          }
        },
        "Nitrosomonadales": {}
      }
    }
  }
};

const TAXONOMIC_ORDER = [
  "superkingdom",
  "phylum",
  "class",
  "order",
  "family",
  "genus",
  "species"
];

// === MAIN ACP SCATTER PLOT ===
function buildMainSection(regionCSVPath) {
  const { tabLeftValue, tabRightValue, categoryValue, filterValue } = getCurrentSelections();

  const pathArray = findFilePath(FOLDER_TREE, filterValue);
  if (!pathArray) {
    // console.log('folderPath not found. Returning early.');
    return;
  }
  const folderPath = pathArray.join('/');

  // Get all levels before the selected one
  const index = TAXONOMIC_ORDER.indexOf(categoryValue);
  const levelsBefore = index > 0 ? TAXONOMIC_ORDER.slice(0, index) : [];
  console.log("Levels before", categoryValue, "are:", levelsBefore);

  const acpCSVPath = `./data/philogenie/${folderPath}/acp_${tabLeftValue}.csv`;
  console.log('acpCSVPath:', acpCSVPath);

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
        title: 'ACP'
      });

      // Add click handler to update plot3
      document.getElementById('plot1').on('plotly_click', function(eventData) {
        const clickedRow = pointData[eventData.points[0].pointIndex];
        const id_replicon = clickedRow.ID;
        const id = id_replicon.split('_').slice(1, 4).join('_');
        const { tabLeftValue, tabRightValue } = getCurrentSelections();

        const heatmapPath = `./data/${id}/analysis/${id_replicon}_${tabRightValue}_${tabLeftValue}.csv`;

        Papa.parse(heatmapPath, {
          download: true,
          dynamicTyping: true,
          complete: function(heatmapResults) {
            try {
              renderHeatmapFromCSV(heatmapResults, clickedRow.ID);  // Replace with actual ID if dynamic
            } catch (e) {
              console.error("Error rendering heatmap:", e);
              alert("Failed to render heatmap.");
            }
          },
          error: function(err) {
            console.error("Error loading heatmap CSV:", err);
            alert(`Error loading heatmap: ${err.message}`);
          }
        });
      });
    }
  });

  const csv_acp_1 = `./data/philogenie/${folderPath}/PC0_${categoryValue}_${filterValue}_${tabRightValue}_${tabLeftValue}.csv`

  Papa.parse(csv_acp_1, {
    download: true,
    complete: function(results) {
      const data = results.data.filter(row => row.length > 0);

      const xValues = data[0].slice(1);
      const yValues = data.slice(1).map(row => row[0]);
      const zValues = data.slice(1).map(row =>
        row.slice(1).map(val => parseFloat(val))
      );

      Plotly.newPlot('plot2_1', [{
        type: 'heatmap',
        z: zValues,
        x: xValues,
        y: yValues,
        hoverongaps: false,
        colorscale: 'YlGnBu',
        hovertemplate: 'X: %{x}<br>Y: %{y}<br>Z: %{z}<extra></extra>'
      }], {
        title: 'Heatmap View',
        xaxis: { title: 'Columns' },
        yaxis: { title: 'Rows' }
      });
    }
  });

  const csv_acp_2 = `./data/philogenie/${folderPath}/PC1_${categoryValue}_${filterValue}_${tabRightValue}_${tabLeftValue}.csv`

  Papa.parse(csv_acp_2, {
    download: true,
    complete: function(results) {
      const data = results.data.filter(row => row.length > 0);

      const xValues = data[0].slice(1);
      const yValues = data.slice(1).map(row => row[0]);
      const zValues = data.slice(1).map(row =>
        row.slice(1).map(val => parseFloat(val))
      );

      Plotly.newPlot('plot2_2', [{
        type: 'heatmap',
        z: zValues,
        x: xValues,
        y: yValues,
        hoverongaps: false,
        colorscale: 'YlGnBu',
        hovertemplate: 'X: %{x}<br>Y: %{y}<br>Z: %{z}<extra></extra>'
      }], {
        title: 'Heatmap View',
        xaxis: { title: 'Columns' },
        yaxis: { title: 'Rows' }
      });
    }
  });
}

function renderHeatmapFromCSV(heatmapResults, id) {
  // Clear the plot (to get rid of the default on click)
  document.getElementById('plot3').innerHTML = "";

  const matrix = heatmapResults.data.filter(row => row.length > 0);

  const xLabels = matrix[0].slice(1); // Columns
  const yLabels = matrix.slice(1).map(row => row[0]); // Rows
  const zValuesRaw = matrix.slice(1).map(row =>
    row.slice(1).map(value => parseFloat(value))
  );

  // Convert to log10, handling zeros and negatives
  const zLog = zValuesRaw.map(row =>
    row.map(val => (val > 0 ? Math.log10(val) : -1)) // Clamp log10(0) to -1
  );

  // Create text labels
  const textVals = zValuesRaw.map(row =>
    row.map(val => isNaN(val) ? "" : val.toFixed(2))
  );

  const colorScale = [
    [0.0, "blue"],
    [0.333, "white"],
    [0.666, "red"],
    [1.0, "black"]
  ];

  Plotly.newPlot('plot3', [{
    z: zLog,
    x: xLabels,
    y: yLabels,
    text: textVals,
    type: 'heatmap',
    colorscale: colorScale,
    zmin: -1,
    zmax: 2,
    texttemplate: "%{text}",
    hovertemplate: "Value: %{text}<br>Gap: %{y}<br>Arm: %{x}<extra></extra>",
    colorbar: {
      tickvals: [-1, 0, 1, 2],
      ticktext: ["10⁻¹", "10⁰", "10¹", "10²"],
      title: "Log Scale"
    }
  }], {
    title: {
      text: `Heatmap for <i>${id}</i>`,
      font: { size: 18 }
    },
    xaxis: {
      title: "Arm Length"
    },
    yaxis: {
      title: "Gap Length",
      tickmode: "linear",
      tick0: parseFloat(yLabels[0]) || 0,
      dtick: 2
    },
    template: "plotly_white",
    shapes: [
      { type: "line", x0: 0, y0: 1, x1: 1, y1: 1, xref: "paper", yref: "paper", line: { color: "black", width: 2 } },
      { type: "line", x0: 0, y0: 0, x1: 1, y1: 0, xref: "paper", yref: "paper", line: { color: "black", width: 2 } },
      { type: "line", x0: 0, y0: 0, x1: 0, y1: 1, xref: "paper", yref: "paper", line: { color: "black", width: 2 } },
      { type: "line", x0: 1, y0: 0, x1: 1, y1: 1, xref: "paper", yref: "paper", line: { color: "black", width: 2 } },
    ]
  });
}

// get all important variables
function getCurrentSelections() {
  // Tabs (get the active button's data-tab)
  const activeTopLeftTab = document.querySelector('#tabs_top_left .tab-button.active');
  const activeTopRightTab = document.querySelector('#card_2 .tab-button.active');

  const tabLeftValue = activeTopLeftTab ? activeTopLeftTab.getAttribute('data-tab') : null;
  const tabRightValue = activeTopRightTab ? activeTopRightTab.getAttribute('data-tab') : null;

  // Dropdowns
  const categoryDropdown = document.getElementById('categoryDropdown');
  const filterDropdown = document.getElementById('filterDropdown');

  const categoryValue = categoryDropdown ? categoryDropdown.value : null;
  const filterValue = filterDropdown ? filterDropdown.value : null;

  return {
    tabLeftValue,
    tabRightValue,
    categoryValue,
    filterValue
  };
}

function findFilePath(tree, target, path = []) {
  for (const key in tree) {
    const newPath = [...path, key];
    if (key === target) {
      return newPath; // ✅ return array
    }
    const result = findFilePath(tree[key], target, newPath);
    if (result) return result;
  }
  return null; // 🔁 or [] if you prefer
}

document.getElementById('categoryDropdown').addEventListener('change', function() {
  buildMainSection();
});

document.getElementById('filterDropdown').addEventListener('change', function() {
  buildMainSection();
});

document.querySelectorAll('#tabs_top_left .tab-button').forEach(button => {
  button.addEventListener('click', function() {
    buildMainSection();
  });
});

document.querySelectorAll('#tabs_top_right .tab-button').forEach(button => {
  button.addEventListener('click', function() {
    buildMainSection();
  });
});

// === INITIAL PLOT RENDER ===
document.addEventListener("DOMContentLoaded", function() {
  buildMainSection();
});

// === PLOT3 DEFAULTS ===  
function addPlots3() {
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

function addPlots() {
  addPlots3();
}

// === TABLE (CARD 2) + CLICK HANDLER FOR plot3 ===
function add_table() {
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
    $.get(`./data/taxonomy.csv`)
      .done(function(csvText) {
        const tableData = parseTaxonomyCSV(csvText);
        const table = $('#taxonomy').DataTable({
          data: tableData,
          columns: [
            { title: 'Kingdom' }, { title: 'Phylum' }, { title: 'Class' },
            { title: 'Order' }, { title: 'Family' }, { title: 'Genus' },
            { title: 'Species' }, { title: 'ID' }, { title: 'ID-replicon' }
          ],
          orderCellsTop: true,
          lengthChange: false,
          info: false,
          paging: true,
          pageLength: 5,
          scrollY: '50px',
          scrollCollapse: true,
          fixedHeader: true,
          autoWidth: false,
          initComplete: function() {
            var api = this.api();
            api.columns().every(function() {
              var column = this;
              var select = $('<select><option value="">All</option></select>')
                .appendTo($('.filters th').eq(column.index()).empty())
                .on('change', function() {
                  var val = $.fn.dataTable.util.escapeRegex($(this).val());
                  column.search(val ? '^' + val + '$' : '', true, false).draw();
                });
              column.data().unique().sort().each(function(d) {
                if (d) select.append('<option value="' + d + '">' + d + '</option>');
              });
            });
          }
        });

        // Row click: update plot3
        $('#taxonomy tbody').on('click', 'tr', function() {
          const rowData = table.row(this).data();
          if (!rowData || rowData.length < 9) return;

          const id_replicon = rowData[8];
          const id = rowData[7];
          const { tabLeftValue, tabRightValue, categoryValue, filterValue } = getCurrentSelections();
          const dataDir = './data/';
          const heatmapPath = `${dataDir}${String(id)}/analysis/${id_replicon}_${tabRightValue}_${tabLeftValue}.csv`;

          Papa.parse(heatmapPath, {
            download: true,
            dynamicTyping: true,
            complete: function(heatmapResults) {
              try {
                renderHeatmapFromCSV(heatmapResults, "some_species_id");  // Replace with actual ID if dynamic
              } catch (e) {
                console.error("Error rendering heatmap:", e);
                alert("Failed to render heatmap.");
              }
            },
            error: function(err) {
              console.error("Error loading heatmap CSV:", err);
              alert(`Error loading heatmap: ${err.message}`);
            }
          });
        });
      });
  });
}

// === Resize active plot on tab switch ===
const observer = new MutationObserver(() => {
  document.querySelectorAll('.tab-content.active div[id^="plot"]').forEach(plot => {
    Plotly.Plots.resize(plot);
  });
});
document.querySelectorAll('.tab-content').forEach(tab => {
  observer.observe(tab, { attributes: true, attributeFilter: ['class'] });
});

document.addEventListener("DOMContentLoaded", function() {
  const categoryDropdown = document.getElementById("categoryDropdown");
  const filterDropdown = document.getElementById("filterDropdown");

  fetch(`./data/taxonomy_values.json`)
    .then(response => { return response.json(); })
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
      console.error("Error loading taxonomy_values.json:", err);
      alert("No se pudo cargar el archivo taxonomy_values.json.");
    });
});

function main() {
  addPlots();
  add_table();
}

main();

