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

// Plotly graphs initialization (your existing graphs)
Plotly.newPlot('plot1_all', [{
  x: ['Ene', 'Feb', 'Mar'],
  y: [20, 14, 23],
  type: 'bar'
}], { title: 'Ventas Mensuales' });

Plotly.newPlot('plot1_coding', [{
  type: 'scatter',
  mode: 'lines+markers',
  x: ['HTML', 'CSS', 'JS'],
  y: [90, 75, 88],
  line: { color: '#10b981' }
}], { title: 'Skills de Programación' });

Plotly.newPlot('plot1_noncoding', [{
  values: [30, 50, 20],
  labels: ['Gestión', 'Comunicación', 'Creatividad'],
  type: 'pie'
}], { title: 'Habilidades Blandas' });

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

Plotly.newPlot('plot2_hc', [{
  r: [3, 6, 8, 5],
  theta: ['DB', 'API', 'Frontend', 'Backend'],
  type: 'barpolar'
}], { title: 'Stack Tecnológico' });

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
  $.get('taxonomy.csv')
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
    ];
  });
}
