fetch('datos.json')
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  })
  .then(data => {
    for (let i = 1; i <= 8; i++) {
      const select = document.getElementById(`dropdown${i}`);
      const valores = data[`dropdown${i}`];
      if (select && Array.isArray(valores)) {
        valores.forEach(value => {
          const option = document.createElement('option');
          option.value = value.toLowerCase();
          option.textContent = value;
          select.appendChild(option);
        });
      }
    }
  })
  .catch(error => {
    console.error("Error al cargar los dropdowns:", error);
  });
