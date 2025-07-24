const ACP_ALL_PATH = '/data/philogenie/Bacteria/acp_all.csv';

// Tab switching logic on "all" region click
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
      activeContent.classList.add('active');
    });
  });
});

document.addEventListener("DOMContentLoaded", function() {
  function onComplete(results) {
    const xValues = [];
    const yValues = [];
    const idValues = [];
    const pointData = []; // Redundant but convenient

    results.data.forEach(row => {
      xValues.push(parseFloat(row.PC1));
      yValues.push(parseFloat(row.PC2));
      idValues.push(row.ID || '');
      pointData.push(row);
    });

    const hoverLabels = pointData.map(row =>
      `PC1: ${row.PC1}<br>` +
      `PC2: ${row.PC2}<br>` +
      `id: ${row.ID}<br>`
    );

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
    document.getElementById('plot1_all').on('plotly_click', function(eventData) {
      const clickedRow = pointData[eventData.points[0].pointIndex];

      const id_replicon = clickedRow.ID;
      const id_replicon_parts = id_replicon.split("_");
      const id = id_replicon_parts.slice(1, 4).join("_");
      const heatmapPath = `/data/${id}/analysis/${id_replicon}_hc_all.csv`;

      console.log(`ID: ${clickedRow.ID}\nReplicon ID: ${id_replicon}`);

      Papa.parse(heatmapPath, {
        download: true,
        dynamicTyping: true,
        complete: function(heatmapResults) {
          const matrix = heatmapResults.data.filter(row => row.length > 0);

          Plotly.newPlot('plot3', [{
            z: matrix.slice(1).map(row => row.slice(1)),
            x: matrix[0].slice(1),
            y: matrix.slice(1).map(row => row[0]),
            type: 'heatmap',
            colorscale: 'YlGnBu'
          }], {
            title: { text: `Heatmap for:\n"${id}"` },
          });

        },
        error: function(err) {
          const msg = `Error loading heatmap for ID ${id}: ${err}`;
          console.error(msg);
          alert(msg);
        }
      });
    });
  };

  Papa.parse(ACP_ALL_PATH, {
    download: true,
    header: true,
    complete: onComplete,
  });
});

function add_plot1() {
  Plotly.newPlot('plot1_coding', [{
    type: 'scatter',
    mode: 'lines+markers',
    x: ['HTML', 'CSS', 'JS'],
    y: [90, 75, 88],
    line: { color: '#10b981' }
  }], { title: 'Skills de Programación' });

  Plotly.newPlot('plot1_noncoding', [{
    type: 'scatter',
    mode: 'lines+markers',
    x: ['HTML', 'CSS', 'JS'],
    y: [90, 75, 88],
    line: { color: '#10b981' }
  }], { title: 'Skills de Programación' });
}

function add_plot2() {
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
}

function add_plot3() {
  // Default previous to click selection
  document.getElementById('plot3').innerHTML = `
    <div style="
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      height: 100%;
      width: 100%;
      font-size: 1.2em;
    ">
      <div style="font-size: 2em;">&#8593;</div>
      <p>Click on a chromosome to display</p>
    </div>
  `;
}

function add_plots() {
  add_plot1(); // top-left (excluding "all" window)
  add_plot2(); // top-right
  add_plot3(); // bottom-left
};

// MutationObserver to resize plots on tab change
const observer = new MutationObserver(() => {
  document.querySelectorAll('.tab-content.active div[id^="plot"]').forEach(plot => {
    Plotly.Plots.resize(plot);
  });
});
document.querySelectorAll('.tab-content').forEach(tab => {
  observer.observe(tab, { attributes: true, attributeFilter: ['class'] });
});

// Bottom-right window
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
    $.get('/data/taxonomy.csv')
      .done(function(csvText) {
        const tableData = parseTaxonomyCSV(csvText);

        $('#taxonomy').DataTable({
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
          pageLength: 5,           // show 5 rows per page
          scrollY: '50px',
          scrollCollapse: true,
          fixedHeader: true,
          autoWidth: false,        // prevent automatic column width, so no horizontal scroll
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
      });
  });
};

function main() {
  add_plots();
  add_table();
}

main();

