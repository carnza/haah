document.addEventListener('DOMContentLoaded', function () {
    fetch('/static/json/comunas.json') // Ruta al archivo JSON
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            const regionSelect = document.getElementById('region');
            const comunaSelect = document.getElementById('comuna');

            // Cargar regiones en el select
            Object.keys(data.Chile).forEach(region => {
                const option = document.createElement('option');
                option.value = region;
                option.textContent = region;
                regionSelect.appendChild(option);
            });

            // Evento al cambiar de región
            regionSelect.addEventListener('change', function () {
                const selectedRegion = this.value;
                comunaSelect.innerHTML = '<option value="">Selecciona una comuna</option>';
                comunaSelect.disabled = !selectedRegion;

                if (selectedRegion) {
                    data.Chile[selectedRegion].forEach(comuna => {
                        const option = document.createElement('option');
                        option.value = comuna;
                        option.textContent = comuna;
                        comunaSelect.appendChild(option);
                    });
                }
            });
        })
        .catch(error => {
            console.error('Error cargando JSON:', error);
            alert('No se pudo cargar la lista de regiones y comunas. Por favor, intenta más tarde.');
        });
});
