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
const TAXONOMY_VALUES_PATH = `${DATA_DIR}/taxonomy_values.json`;
const STRUCTURE_PATH = `${DATA_DIR}/structure.json`

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
 
 
 

const list = document.getElementById('bacteria-list-NCBI');
const content = document.getElementById('content');

list.addEventListener('click', function(e) {
  if (e.target.tagName === 'LI') {
    const title = e.target.getAttribute('data-title');

    content.innerHTML = '<p><em>Loading Wikipedia summary...</em></p>';

    fetch(`https://en.wikipedia.org/api/rest_v1/page/summary/${title}`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Wikipedia article not found.');
        }
        return response.json();
      })
      .then(data => {
        content.innerHTML = `
          <h3>${data.title}</h3>
          <p>${data.extract}</p>
          <p><a href="https://en.wikipedia.org/wiki/${title}" target="_blank">Read more on Wikipedia</a></p>
        `;
      })
      .catch(err => {
        content.innerHTML = `<p>Error: ${err.message}</p>`;
      });
  }
});
function buildHierarchy(data, levels) {
  const root = { name: "root", children: [] };
  data.forEach(row => {
    let current = root;
    levels.forEach(level => {
      const value = row[level];
      if (!value) return;
      let child = current.children.find(d => d.name === value);
      if (!child) {
        child = { name: value, children: [] };
        current.children.push(child);
      }
      current = child;
    });
  });
  return root;
}

function renderDendrogram() {
  const card = document.getElementById("card_1");
  const { width, height } = card.getBoundingClientRect();
  const svg = d3.select("#taxonomy_dendrogram")
    .attr("width", width)
    .attr("height", height);
  svg.selectAll("*").remove();

  const g = svg.append("g");

  const zoomBehavior = d3.zoom()
    .scaleExtent([0.5, 5])
    .on("zoom", (event) => {
      g.attr("transform", event.transform);
    });

  svg.call(zoomBehavior);

  d3.csv("./data/taxonomy.csv").then(data => {
    const levels = Object.keys(data[0]).filter(col => col !== "ID-replicon");
    const hierarchyData = buildHierarchy(data, levels);
    let root = d3.hierarchy(hierarchyData.children[0]);
    root.x0 = height / 2;
    root.y0 = 0;

    root.children.forEach(collapse);

    const treeLayout = d3.tree().size([height - 100, width - 200]);

    function collapse(d) {
      if (d.children) {
        d._children = d.children;
        d._children.forEach(collapse);
        d.children = null;
      }
    }

    let i = 0;
    function update(source) {
      console.log("name:", source.data.name); 
      treeLayout(root);
      const nodes = root.descendants();
      const links = root.links();

      const node = g.selectAll(".node")
        .data(nodes, d => d.id || (d.id = ++i));

      const nodeEnter = node.enter().append("g")
        .attr("class", "node")
        .attr("transform", d => `translate(${source.y0},${source.x0})`)
        .on("click", (event, d) => {
          if (d.children) {
            d._children = d.children;
            d.children = null;
          } else {
            d.children = d._children;
            d._children = null;
          }
          update(d);
        });

      nodeEnter.append("circle")
        .attr("r", 5)
        .style("fill", d => d._children ? "lightsteelblue" : "#fff");

      nodeEnter.append("text")
        .attr("dy", "-0.8em")
        .attr("text-anchor", "middle")
        .style("font-size", "8px")
        .text(d => d.data.name.length > 20 
          ? d.data.name.slice(0, 20) + "…" 
          : d.data.name);

      const nodeUpdate = nodeEnter.merge(node);
      nodeUpdate.transition().duration(300)
        .attr("transform", d => `translate(${d.y},${d.x})`);
      nodeUpdate.select("circle")
        .style("fill", d => d._children ? "lightsteelblue" : "#fff");

      node.exit().transition().duration(300)
        .attr("transform", d => `translate(${source.y},${source.x})`)
        .remove();

      const link = g.selectAll(".link")
        .data(links, d => d.target.id);

      link.enter().insert("path", "g")
        .attr("class", "link")
        .merge(link)
        .transition().duration(300)
        .attr("d", d3.linkHorizontal()
          .x(d => d.y)
          .y(d => d.x)
        );

      link.exit().transition().duration(300).remove();

      nodes.forEach(d => {
        d.x0 = d.x;
        d.y0 = d.y;
      });
    }

    update(root);

    d3.select("#zoom-in").on("click", () => {
      svg.transition().call(zoomBehavior.scaleBy, 1.2);
    });
    d3.select("#zoom-out").on("click", () => {
      svg.transition().call(zoomBehavior.scaleBy, 0.8);
    });
    d3.select("#zoom-reset").on("click", () => {
      svg.transition().call(zoomBehavior.transform, d3.zoomIdentity);
    });
  });
}

renderDendrogram();
window.addEventListener("resize", renderDendrogram);


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
          const { tabRightValue } = getCurrentSelections();
          const heatmapPath = `${DATA_DIR}/${String(id)}/analysis/${idReplicon}_${tabRightValue}_${tabLeftValue}.csv`;
          renderHeatmapFromCSVPathAndId(heatmapPath, idReplicon);
        });
      });
  });
}
 
 
 

// main entrypoint 
buildTaxonomyCard(); 

