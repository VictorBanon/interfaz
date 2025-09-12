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

const COLOR_SCALE_3 = [
  [0.0, "blue"],
  [0.5, "white"],
  [1.0, "red"]
];
const COLOR_SCALE_4 = [
  [0.0, "blue"],
  [0.333, "white"],
  [0.666, "red"],
  [1.0, "black"]
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

// Recursive iteration
function findFilePath(tree, target, path = []) {
  for (const key in tree) {
    const newPath = [...path, key];
    if (key === target) return newPath;
    const result = findFilePath(tree[key], target, newPath);
    if (result) return result;
  }
}

async function findFilePathFromJSON(target) {
  return fetch(STRUCTURE_PATH)
    .then(response => {
      if (!response.ok) throw new Error(`HTTP error ${response.status}`);
      return response.json();
    })
    .then(tree => findFilePath(tree, target))
    .catch(err => {
      console.error("Failed to load or parse structure.json:", err);
      return null;
    });
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
          const heatmapPath = `${DATA_DIR}/${String(id)}/analysis/${idReplicon}_${tabRightValue}_${tabLeftValue}.csv`;
          renderHeatmapFromCSVPathAndId(heatmapPath, idReplicon);
        });
      });
  });
}
  

// main entrypoint
document.addEventListener("DOMContentLoaded", async function() { 

  buildTaxonomyCard();
});

