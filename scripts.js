// Tab switching logic
document.querySelectorAll('.card').forEach(card => {
  const buttons = card.querySelectorAll('.tab-button');
  const contents = card.querySelectorAll('.tab-content');

  buttons.forEach(button => {
    button.addEventListener('click', () => {
      const target = button.getAttribute('data-tab');

      // Deactivate all buttons and contents in this card
      buttons.forEach(btn => btn.classList.remove('active'));
      contents.forEach(content => content.classList.remove('active'));

      // Activate the selected
      button.classList.add('active');
      const activeContent = card.querySelector(`#${target}`);
      if (activeContent) {
        activeContent.classList.add('active');
      }
    });
  });
});

document.addEventListener("DOMContentLoaded", function () {
  Papa.parse('/data/philogenie/Bacteria/acp_all.csv', {
    download: true,
    header: true,
    complete: function (results) {
      const data = results.data;

      const xValues = [];
      const yValues = [];
      const idValues = [];
      const id_repValues = [];

      // Store full data so we can access the clicked point's data later
      const pointData = [];

      data.forEach(row => {
        if (row.PC1 && row.PC2) {
          xValues.push(parseFloat(row.PC1));
          yValues.push(parseFloat(row.PC2));
          idValues.push(row.ID || '');
          id_repValues.push(row.ID || '');
          pointData.push(row);
        }
      });

      const hoverLabels = xValues.map((_, i) =>
        `PC1: ${xValues[i]}<br>` +
        `PC2: ${yValues[i]}<br>` +
        `id: ${idValues[i]}<br>` +
        `id replicon: ${id_repValues[i]}<br>`  
      );

      // Initial plot in plot1_all
      Plotly.newPlot('plot1_all', [{
        type: 'scatter',
        mode: 'markers',
        x: xValues,
        y: yValues,
        text: hoverLabels,
        hoverinfo: 'text',
        marker: { size: 10 },
        line: { color: '#10b981' }
      }], {
        title: 'ACP All CSV Plot'
      });

      // Click handler to update plot3
      const plotElement = document.getElementById('plot1_all');
      plotElement.on('plotly_click', function (eventData) {
        const pointIndex = eventData.points[0].pointIndex;
        const clickedRow = pointData[pointIndex];

        const id = clickedRow.ID;
        const id_replicon = clickedRow.ID;
        const name = clickedRow.ID; 

        const parts = id_replicon.split("_");
        const rebuild_id = parts.slice(1, 4).join("_");

        // const heatmapPath = `/data/GCF_014054525.1_ASM1405452v1/analysis/${id_replicon}_hc_all.csv`;
        const heatmapPath = `/data/${rebuild_id}/analysis/${id_replicon}_hc_all.csv`;

        Papa.parse(heatmapPath, {
          download: true,
          dynamicTyping: true,
          complete: function (heatmapResults) {
            const rawMatrix = heatmapResults.data;

            // Remove empty rows
            const matrix = rawMatrix.filter(row => row.length > 0);

            // Extract x-axis labels from the first row, skipping the top-left corner cell
            const xLabels = matrix[0].slice(1);

            // Extract y-axis labels from the first column (excluding the first row)
            const yLabels = matrix.slice(1).map(row => row[0]);

            // Extract z matrix: everything except the first row and first column
            const z = matrix.slice(1).map(row => row.slice(1));

            // Plot
            Plotly.newPlot('plot3', [{
              z: z,
              x: xLabels,
              y: yLabels,
              type: 'heatmap',
              colorscale: 'YlGnBu'
            }], {
              //title: `Mapa de Calor para "${name}"`,
              xaxis: { title: 'Columnas' },
              yaxis: { title: 'Filas' }
            });
          },
          error: function (err) {
            console.error(`Error loading heatmap for ID ${id}:`, err);
            alert(`No se pudo cargar el heatmap para ID: ${heatmapPath}`);
          }
        });
      });
    }
  });
});


Plotly.newPlot('plot1_coding', [{
  type: 'scatter',
  mode: 'lines+markers',
  x: ['HTML', 'CSS', 'JS'],
  y: [90, 75, 88],
  line: { color: '#10b981' }
}], { title: 'Skills de Programación' });

Plotly.newPlot('plot1_noncoding',  [{
  type: 'scatter',
  mode: 'lines+markers',
  x: ['HTML', 'CSS', 'JS'],
  y: [90, 75, 88],
  line: { color: '#10b981' }
}], { title: 'Skills de Programación' });

Plotly.newPlot('plot2_ha', [{
  values: [25, 30, 45],
  labels: ['A', 'B', 'C'],
  type: 'pie',
  hole: 0.4
}], { title: 'Distribución de Categorías' });

Plotly.newPlot('plot2_hb', [{
  type: 'scatterpolar',
  r: [39, 28, 30],
  theta: ['Comunicación', 'Productividad', 'Creatividad'],
  fill: 'toself'
}], { title: 'Radar de Habilidades', polar: { radialaxis: { visible: true } } });

Plotly.newPlot('plot2_hc_1', [{
  z: [
    [1, 20, 30],
    [20, 1, 60],
    [30, 60, 1]
  ],
  x: ['Semana 1', 'Semana 2', 'Semana 3'],
  y: ['HTML', 'CSS', 'JS'],
  type: 'heatmap',
  colorscale: 'YlGnBu'
}], {
  title: 'Mapa de Calor de Progreso',
  xaxis: { title: 'Semana' },
  yaxis: { title: 'Skill' }
});
Plotly.newPlot('plot2_hc_2', [{
  z: [
    [1, 20, 30],
    [20, 1, 60],
    [30, 60, 1]
  ],
  x: ['Semana 1', 'Semana 2', 'Semana 3'],
  y: ['HTML', 'CSS', 'JS'],
  type: 'heatmap',
  colorscale: 'YlGnBu'
}], {
  title: 'Mapa de Calor de Progreso',
  xaxis: { title: 'Semana' },
  yaxis: { title: 'Skill' }
});

Plotly.newPlot('plot3', [{
  z: [
    [1, 20, 30],
    [20, 1, 60],
    [30, 60, 1]
  ],
  x: ['Semana 1', 'Semana 2', 'Semana 3'],
  y: ['HTML', 'CSS', 'JS'],
  type: 'heatmap',
  colorscale: 'YlGnBu'
}], {
  title: 'Mapa de Calor de Progreso',
  xaxis: { title: 'Semana' },
  yaxis: { title: 'Skill' }
});

// MutationObserver to resize plots on tab change
const observer = new MutationObserver(() => {
  document.querySelectorAll('.tab-content.active div[id^="plot"]').forEach(plot => {
    Plotly.Plots.resize(plot);
  });
});
document.querySelectorAll('.tab-content').forEach(tab => {
  observer.observe(tab, { attributes: true, attributeFilter: ['class'] });
});

$(document).ready(function () {
  $.get('data/taxonomy.csv')
    .done(function (csvText) {
      const tableData = parseTaxonomyCSV(csvText);

      const table = $('#taxonomy').DataTable({
        data: tableData,
        columns: [
          { title: 'Kingdom' },
          { title: 'Phylum' },
          { title: 'Class' },
          { title: 'Order' },
          { title: 'Family' },
          { title: 'Genus' },
          { title: 'Species' },
          { title: 'ID' },
          { title: 'ID-replicon' },
        ],
        orderCellsTop: true,
        lengthChange: false,
        info: false,
        paging: true,
        pageLength: 5,               // show 5 rows per page
        scrollY: '50px',
        scrollCollapse: true,
        fixedHeader: true,
        autoWidth: false,            // prevent automatic column width, so no horizontal scroll
        initComplete: function () {
        var api = this.api();

        api.columns().every(function () {
            var column = this;
            var select = $('<select><option value="">All</option></select>')
            .appendTo($('.filters th').eq(column.index()).empty())
            .on('change', function () {
                var val = $.fn.dataTable.util.escapeRegex($(this).val());
                column.search(val ? '^' + val + '$' : '', true, false).draw();
            });

            column.data().unique().sort().each(function (d) {
            if (d) select.append('<option value="' + d + '">' + d + '</option>');
            });
        });
        }

      });
    });
});


// CSV parsing helper function
function parseTaxonomyCSV(csv) {
  const lines = csv.trim().split('\n');
  const headers = lines[0].split(',').map(h => h.trim());
  const rows = lines.slice(1);

  const colMap = {
    superkingdom: headers.indexOf('superkingdom'),
    phylum: headers.indexOf('phylum'),
    class: headers.indexOf('class'),
    order: headers.indexOf('order'),
    family: headers.indexOf('family'),
    genus: headers.indexOf('genus'),
    species: headers.indexOf('species'),
    id: headers.indexOf('ID'),
    id_replicon: headers.indexOf('ID-replicon'),
  };

  return rows.map(row => {
    const cols = row.split(',');
    return [
      cols[colMap.superkingdom] || '',
      cols[colMap.phylum] || '',
      cols[colMap.class] || '',
      cols[colMap.order] || '',
      cols[colMap.family] || '',
      cols[colMap.genus] || '',
      cols[colMap.species] || '',
      cols[colMap.id] || '',
      cols[colMap.id_replicon] || '',
    ];
  });
}
