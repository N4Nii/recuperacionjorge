from flask import Flask, request, jsonify
from flask_cors import CORS
import database
import os

app = Flask(__name__)
CORS(app)

database.init_db()

@app.route('/')
def serve_index():
    return jsonify({"status": "API de Muebles activa"}), 200

@app.route('/api/productos', methods=['GET'])
def get_productos():
    categoria = request.args.get('categoria')
    q = request.args.get('q')
    conn = database.get_db_connection()
    
    query = 'SELECT * FROM productos WHERE 1=1'
    params = []
    
    if categoria and categoria != 'Todos':
        query += ' AND categoria = ?'
        params.append(categoria)
    if q:
        query += ' AND nombre LIKE ?'
        params.append(f'%{q}%')
        
    productos = conn.execute(query, params).fetchall()
    conn.close()
    return jsonify([dict(p) for p in productos])

@app.route('/api/productos/<int:prod_id>', methods=['GET'])
def get_producto_detalle(prod_id):
    conn = database.get_db_connection()
    producto = conn.execute('SELECT * FROM productos WHERE id = ?', (prod_id,)).fetchone()
    conn.close()
    if producto:
        return jsonify(dict(producto))
    return jsonify({'error': 'Producto no encontrado'}), 404

@app.route('/api/pedidos', methods=['POST'])
def crear_pedido():
    data = request.json
    conn = database.get_db_connection()
    cursor = conn.cursor()
    
    for item in data.get('items', []):
        cursor.execute('UPDATE productos SET stock = stock - ? WHERE id = ?', (item['cantidad'], item['id']))
        
    cursor.execute('INSERT INTO pedidos (usuario_id, total, metodo_pago, estado) VALUES (?, ?, ?, ?)',
                   (data.get('usuario_id'), data['total'], data.get('metodo_pago', 'Tarjeta'), 'pagado'))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Pedido procesado con éxito', 'estado': 'pagado'}), 201

if __name__ == '__main__':
    # Captura el puerto dinámico de Render o usa 5000 por defecto
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)