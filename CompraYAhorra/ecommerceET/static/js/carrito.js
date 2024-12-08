document.addEventListener('DOMContentLoaded', function () {
    let carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    const contadorCarrito = document.getElementById('carrito-contador');
    const listaCarrito = document.getElementById('lista-carrito');
    const totalCarrito = document.getElementById('total-carrito');
    const vaciarCarritoBtn = document.getElementById('vaciar-carrito');
    const totalCarritoInput = document.getElementById('total_carrito'); 

    function actualizarCarrito() {
        localStorage.setItem('carrito', JSON.stringify(carrito));
        contadorCarrito.textContent = carrito.reduce((total, item) => total + item.cantidad, 0);
        listaCarrito.innerHTML = '';
        carrito.forEach(item => {
            const li = document.createElement('li');
            li.classList.add('list-group-item');
            li.textContent = `${item.nombre} - ${item.cantidad} x $${item.precio}`;
            listaCarrito.appendChild(li);
        });
        const total = carrito.reduce((sum, item) => sum + item.precio * item.cantidad, 0);
        totalCarrito.textContent = total.toLocaleString();
    
        // Asegúrate de asignar el total al campo oculto
        if (totalCarritoInput) {
            totalCarritoInput.value = total;
        }
    }

    document.querySelectorAll('.btn-agregar-carrito').forEach(boton => {
        boton.addEventListener('click', function () {
            const nombre = this.getAttribute('data-nombre');
            const precio = parseInt(this.getAttribute('data-precio'), 10);

            const productoExistente = carrito.find(item => item.nombre === nombre);
            if (productoExistente) {
                productoExistente.cantidad++;
            } else {
                carrito.push({ nombre, precio, cantidad: 1 });
            }

            actualizarCarrito();
        });
    });

    vaciarCarritoBtn.addEventListener('click', function () {
        carrito = [];
        actualizarCarrito();
    });

    actualizarCarrito();
});
