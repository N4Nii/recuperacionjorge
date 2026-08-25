// Reemplaza con la URL de tu backend en Render agregando /api al final
const API_URL = 'https://TU-BACKEND.onrender.com/api'; 

let carrito = JSON.parse(localStorage.getItem('cart')) || [];
let productoSeleccionado = null;
let tallaSeleccionada = null;

document.addEventListener('DOMContentLoaded', () => {
    cargarProductos('Todos');
    actualizarCarritoUI();
});

async function cargarProductos(categoria = '') {
    const res = await fetch(`${API_URL}/productos?categoria=${encodeURIComponent(categoria)}`);
    const productos = await res.json();
    
    const container = document.getElementById('grid-productos');
    container.innerHTML = productos.map(p => `
        <div class="card-producto" onclick="abrirDetalle(${p.id})">
            ${p.descuento > 0 ? `<span class="badge-discount">-${p.descuento}%</span>` : ''}
            <img src="${p.imagen}" alt="${p.nombre}">
            <h4>${p.nombre}</h4>
            <div class="price-container">
                <span class="price-current">$${p.precio.toFixed(2)}</span>
                ${p.precio_original ? `<span class="price-original">$${p.precio_original.toFixed(2)}</span>` : ''}
            </div>
        </div>
    `).join('');
}

function filtrarCategoria(cat, btn) {
    if (btn) {
        document.querySelectorAll('.pill').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
    }
    cargarProductos(cat);
}

function filtrarYCerrar(cat) {
    filtrarCategoria(cat, null);
    toggleMenuLateral();
}

function toggleSearch() {
    document.getElementById('search-bar-container').classList.toggle('open');
}

function ejecutarBusqueda(e) {
    const q = e.target.value;
    fetch(`${API_URL}/productos?q=${encodeURIComponent(q)}`)
        .then(res => res.json())
        .then(productos => {
            const container = document.getElementById('grid-productos');
            container.innerHTML = productos.map(p => `
                <div class="card-producto" onclick="abrirDetalle(${p.id})">
                    <img src="${p.imagen}">
                    <h4>${p.nombre}</h4>
                    <div class="price-container">
                        <span class="price-current">$${p.precio.toFixed(2)}</span>
                    </div>
                </div>
            `).join('');
        });
}

async function abrirDetalle(id) {
    const res = await fetch(`${API_URL}/productos/${id}`);
    productoSeleccionado = await res.json();
    
    document.getElementById('detail-img').src = productoSeleccionado.imagen;
    document.getElementById('detail-title').innerText = productoSeleccionado.nombre;
    document.getElementById('detail-price').innerText = `$${productoSeleccionado.precio.toFixed(2)} MXN`;
    document.getElementById('detail-old-price').innerText = productoSeleccionado.precio_original ? `$${productoSeleccionado.precio_original.toFixed(2)}` : '';

    const tallas = productoSeleccionado.tallas ? productoSeleccionado.tallas.split(',') : ['S', 'M', 'L'];
    const sizeContainer = document.getElementById('size-options');
    sizeContainer.innerHTML = tallas.map(t => `<button class="size-btn" onclick="seleccionarTalla('${t.trim()}', this)">${t.trim()}</button>`).join('');

    tallaSeleccionada = null;
    document.getElementById('product-detail-view').style.display = 'block';
}

function seleccionarTalla(talla, elem) {
    tallaSeleccionada = talla;
    document.querySelectorAll('.size-btn').forEach(b => b.classList.remove('selected'));
    elem.classList.add('selected');
}

function agregarAlCarritoDesdeDetalle() {
    if (!tallaSeleccionada) return alert("Por favor selecciona una talla");
    
    const existe = carrito.find(i => i.id === productoSeleccionado.id && i.talla === tallaSeleccionada);
    if (existe) {
        existe.cantidad += 1;
    } else {
        carrito.push({
            id: productoSeleccionado.id,
            nombre: productoSeleccionado.nombre,
            precio: productoSeleccionado.precio,
            talla: tallaSeleccionada,
            imagen: productoSeleccionado.imagen,
            cantidad: 1
        });
    }
    localStorage.setItem('cart', JSON.stringify(carrito));
    actualizarCarritoUI();
    cerrarDetalle();
    toggleCarrito();
}

function actualizarCarritoUI() {
    const total = carrito.reduce((sum, item) => sum + (item.precio * item.cantidad), 0);
    document.getElementById('cart-subtotal').innerText = total.toFixed(2);

    let descPct = 0;
    if (total >= 2999) descPct = 0.30;
    else if (total >= 2699) descPct = 0.25;
    else if (total >= 1299) descPct = 0.20;

    const descuento = total * descPct;
    const totalFinal = total - descuento;

    const progressFill = document.getElementById('progress-bar-fill');
    const progressText = document.getElementById('discount-progress-text');
    let pctWidth = Math.min((total / 2999) * 100, 100);
    progressFill.style.width = `${pctWidth}%`;

    if (total >= 2999) {
        progressText.innerHTML = "¡Obtienes <strong>30% de descuento</strong>!";
    } else if (total >= 2699) {
        progressText.innerHTML = `Agrega <strong>$${(2999 - total).toFixed(2)}</strong> para 30% desc.`;
    } else if (total >= 1299) {
        progressText.innerHTML = `Agrega <strong>$${(2699 - total).toFixed(2)}</strong> para 25% desc.`;
    } else {
        progressText.innerHTML = `Agrega <strong>$${(1299 - total).toFixed(2)}</strong> para 20% desc.`;
    }

    document.getElementById('cart-total').innerText = totalFinal.toFixed(2);
    
    document.getElementById('cart-items').innerHTML = carrito.map(i => `
        <div style="display:flex; gap:10px; margin-bottom:10px; border-bottom:1px solid #eee; padding-bottom:5px;">
            <img src="${i.imagen}" width="40" height="50" style="object-fit:cover;">
            <div style="flex:1;">
                <p style="font-size:10px; font-weight:bold;">${i.nombre}</p>
                <small style="font-size:9px;">Talla: ${i.talla} | Cant: ${i.cantidad}</small><br>
                <strong style="font-size:11px;">$${(i.precio * i.cantidad).toFixed(2)}</strong>
            </div>
        </div>
    `).join('');
}

function toggleCarrito() { document.getElementById('cart-drawer').classList.toggle('open'); }
function toggleMenuLateral() { document.getElementById('menu-lateral').classList.toggle('open'); }
function cerrarDetalle() { document.getElementById('product-detail-view').style.display = 'none'; }
function cargarHome() { document.getElementById('product-detail-view').style.display = 'none'; cargarProductos('Todos'); }

function irAPagar() {
    if (carrito.length === 0) return alert("Tu carrito está vacío");
    toggleCarrito();
    document.getElementById('checkout-view').style.display = 'block';
}

function cerrarCheckout() { document.getElementById('checkout-view').style.display = 'none'; }

function togglePaymentFields(showTarjeta) {
    document.getElementById('tarjeta-fields').style.display = showTarjeta ? 'flex' : 'none';
}

async function procesarPagoFinal(e) {
    e.preventDefault();
    const total = parseFloat(document.getElementById('cart-total').innerText);
    const metodo = document.querySelector('input[name="payment_method"]:checked').value;

    const res = await fetch(`${API_URL}/pedidos`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            usuario_id: 1, 
            total: total, 
            metodo_pago: metodo, 
            items: carrito 
        })
    });

    if (res.ok) {
        alert("¡Pago realizado con éxito! Gracias por tu compra.");
        carrito = [];
        localStorage.removeItem('cart');
        actualizarCarritoUI();
        cerrarCheckout();
    } else {
        alert("Hubo un error al procesar el pedido.");
    }
}