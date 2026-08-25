import sqlite3

def get_db_connection():
    conn = sqlite3.connect('tienda.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio REAL NOT NULL,
            precio_original REAL,
            descuento INTEGER DEFAULT 0,
            stock INTEGER NOT NULL,
            imagen TEXT NOT NULL,
            colores TEXT,
            tallas TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            total REAL NOT NULL,
            metodo_pago TEXT NOT NULL,
            estado TEXT DEFAULT 'pagado',
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
    ''')

    cursor.execute('SELECT COUNT(*) FROM productos')
    if cursor.fetchone()[0] == 0:
        productos = [
            # NOVEDADES
            ('Blazer Corto Asimétrico Botón Lateral', 'Novedades', 1299.00, None, 0, 15, 'https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=600', 'Blanco, Negro', 'XS, S, M, L'),
            ('Palazzo Halter con Cut Out en Cintura', 'Novedades', 799.00, None, 0, 12, 'https://images.unsplash.com/photo-1509631179647-0177331693ae?w=600', 'Negro, Café', 'XS, S, M, L, XL'),
            ('Chaleco Sastre Estructurado Solapa', 'Novedades', 899.00, None, 0, 20, 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=600', 'Hueso, Negro', 'S, M, L'),
            ('Top Lino Escote Cuadrado Botones', 'Novedades', 699.00, None, 0, 18, 'https://images.unsplash.com/photo-1539109136881-3be0616acf4b?w=600', 'Beige, Blanco', 'XS, S, M, L'),
            ('Pantalón Wide Leg Lino Tiro Alto', 'Novedades', 999.00, None, 0, 10, 'https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=600', 'Arena, Olivo', 'XS, S, M, L'),
            ('Chaqueta Crop Tacto Piel Cierre', 'Novedades', 1499.00, None, 0, 8, 'https://images.unsplash.com/photo-1520975661595-6453be3f7070?w=600', 'Negro, Vino', 'S, M, L'),
            ('Vestido Midi Satinado Escote Fluido', 'Novedades', 1099.00, None, 0, 14, 'https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=600', 'Verde Olivo, Negro', 'XS, S, M'),
            ('Falda Midi Plisada Efecto Metalizado', 'Novedades', 849.00, None, 0, 16, 'https://images.unsplash.com/photo-1583496661160-fb5886a0aaaa?w=600', 'Plata, Champagne', 'S, M, L'),
            ('Top Manga Larga Semitransparente Punto', 'Novedades', 599.00, None, 0, 22, 'https://images.unsplash.com/photo-1618244972963-dbee1a7edc95?w=600', 'Negro, Blanco', 'XS, S, M, L'),
            ('Blusa Cuello Bobo Manga Abullonada', 'Novedades', 749.00, None, 0, 11, 'https://images.unsplash.com/photo-1604014237800-1c9102c219da?w=600', 'Marfil, Rosa', 'S, M, L'),

            # HS X ANNA SARELLY
            ('Blazer Oversized HS x Anna Sarelly Grey', 'HS x Anna Sarelly', 1899.00, None, 0, 10, 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=600', 'Gris Jaspe, Negro', 'XS, S, M, L'),
            ('Top Corsetero Estructurado Satén', 'HS x Anna Sarelly', 799.00, None, 0, 15, 'https://images.unsplash.com/photo-1502716119720-b23a93e5fe1b?w=600', 'Champagne, Negro', 'XS, S, M'),
            ('Pantalón Cargo Sastre Tiro Caído', 'HS x Anna Sarelly', 1199.00, None, 0, 12, 'https://images.unsplash.com/photo-1506629082955-511b1aa562c8?w=600', 'Gris, Beige', 'S, M, L'),
            ('Vestido Mini Asimétrico Cut Out', 'HS x Anna Sarelly', 1299.00, None, 0, 9, 'https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?w=600', 'Negro', 'XS, S, M'),
            ('Chaqueta Biker Oversized Vintage Effect', 'HS x Anna Sarelly', 2199.00, None, 0, 6, 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=600', 'Café Gastado', 'S, M, L'),
            ('Falda Mini Tablada Tiro Bajo', 'HS x Anna Sarelly', 699.00, None, 0, 18, 'https://images.unsplash.com/photo-1582142839970-2b9322773f5f?w=600', 'Gris Marino', 'XS, S, M'),
            ('Top Draped Neck Espalda Descubierta', 'HS x Anna Sarelly', 649.00, None, 0, 14, 'https://images.unsplash.com/photo-1539109136881-3be0616acf4b?w=600', 'Plata, Negro', 'S, M'),
            ('Conjunto Sastre Bicolor Edición Especial', 'HS x Anna Sarelly', 2499.00, None, 0, 7, 'https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=600', 'Negro/Gris', 'S, M, L'),
            ('Vestido Camisero Popelina Pop Art', 'HS x Anna Sarelly', 1399.00, None, 0, 13, 'https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=600', 'Blanco', 'S, M, L'),
            ('Top Tejido Calado Metallic Thread', 'HS x Anna Sarelly', 849.00, None, 0, 16, 'https://images.unsplash.com/photo-1618244972963-dbee1a7edc95?w=600', 'Dorado, Plata', 'XS, S, M'),

            # VESTIDOS
            ('Vestido Corto Manga Abullonada Azul', 'Vestidos', 899.00, None, 0, 20, 'https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=600', 'Azul Cielo, Blanco', 'XS, S, M, L'),
            ('Vestido Estampado Lunares Espalda Abierta', 'Vestidos', 999.00, None, 0, 15, 'https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=600', 'Marfil/Negro', 'S, M, L'),
            ('Vestido Largo Lino Tiras Ajustables', 'Vestidos', 1199.00, None, 0, 12, 'https://images.unsplash.com/photo-1496747611176-843222e1e57c?w=600', 'Arena, Terracota', 'XS, S, M, L'),
            ('Vestido Ajustado Acanalado Escote Bardo', 'Vestidos', 749.00, None, 0, 25, 'https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?w=600', 'Negro, Beige', 'XS, S, M, L'),
            ('Vestido Camisero Cinturón Ajustable', 'Vestidos', 1099.00, None, 0, 10, 'https://images.unsplash.com/photo-1585487000160-6ebcfceb0d03?w=600', 'Kaki, Blanco', 'S, M, L'),
            ('Vestido Satinado Cut Out Espalda', 'Vestidos', 1299.00, None, 0, 8, 'https://images.unsplash.com/photo-1539109136881-3be0616acf4b?w=600', 'Rojo Vino, Negro', 'XS, S, M'),
            ('Vestido Midi Flores Primavera', 'Vestidos', 849.00, None, 0, 18, 'https://images.unsplash.com/photo-1512436991641-6745cdb1723f?w=600', 'Multicolor', 'S, M, L'),
            ('Vestido Blazer Botones Dorados', 'Vestidos', 1599.00, None, 0, 9, 'https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=600', 'Negro, Blanco', 'S, M, L'),
            ('Vestido Halter Plisado Fiestas', 'Vestidos', 1399.00, None, 0, 11, 'https://images.unsplash.com/photo-1509631179647-0177331693ae?w=600', 'Esmeralda, Negro', 'XS, S, M'),
            ('Vestido Tejido Ajustado Cuello Alto', 'Vestidos', 899.00, None, 0, 14, 'https://images.unsplash.com/photo-1618244972963-dbee1a7edc95?w=600', 'Gris, Camel', 'S, M, L'),

            # TOPS
            ('Top Lino Botones Corto', 'Tops', 489.00, 699.00, 30, 20, 'https://images.unsplash.com/photo-1539109136881-3be0616acf4b?w=600', 'Beige, Negro', 'XS, S, M, L'),
            ('Top Off-Shoulder Olanes Drapeado', 'Tops', 549.00, None, 0, 16, 'https://images.unsplash.com/photo-1502716119720-b23a93e5fe1b?w=600', 'Negro, Blanco', 'XS, S, M'),
            ('Top Corsé Estructurado Varillas', 'Tops', 699.00, None, 0, 14, 'https://images.unsplash.com/photo-1604014237800-1c9102c219da?w=600', 'Blanco, Marfil', 'S, M, L'),
            ('Top Halter Satinado Espalda Descubierta', 'Tops', 499.00, None, 0, 22, 'https://images.unsplash.com/photo-1618244972963-dbee1a7edc95?w=600', 'Verde, Negro', 'XS, S, M'),
            ('Top Básico Algodón Cuello Alto', 'Tops', 349.00, None, 0, 30, 'https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=600', 'Blanco, Negro, Gris', 'XS, S, M, L, XL'),
            ('Top Asimétrico Manga Larga Single Shoulder', 'Tops', 599.00, None, 0, 12, 'https://images.unsplash.com/photo-1582142839970-2b9322773f5f?w=600', 'Chocolate, Negro', 'S, M, L'),
            ('Top Tejido Crop Lurex', 'Tops', 429.00, None, 0, 18, 'https://images.unsplash.com/photo-1583496661160-fb5886a0aaaa?w=600', 'Plata, Bronce', 'XS, S, M'),
            ('Camisa Satinada Oversized Manga Larga', 'Tops', 799.00, None, 0, 15, 'https://images.unsplash.com/photo-1585487000160-6ebcfceb0d03?w=600', 'Perla, Champagne', 'S, M, L'),
            ('Top Encaje Floral Tirantes Ajustables', 'Tops', 399.00, None, 0, 25, 'https://images.unsplash.com/photo-1512436991641-6745cdb1723f?w=600', 'Negro, Nude', 'XS, S, M, L'),
            ('Top Tejido Cuello Bardo Ribbed', 'Tops', 529.00, None, 0, 19, 'https://images.unsplash.com/photo-1506629082955-511b1aa562c8?w=600', 'Marfil, Café', 'S, M, L'),

            # REBAJAS
            ('Blusa Estampada Pata de Gallo', 'Rebajas', 489.00, 699.00, 30, 12, 'https://images.unsplash.com/photo-1583496661160-fb5886a0aaaa?w=600', 'Negro/Blanco', 'S, M, L'),
            ('Leggings Rectos Lino Flex', 'Rebajas', 559.00, 799.00, 30, 10, 'https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=600', 'Rosa Pale, Beige', 'XS, S, M'),
            ('Chaleco Sastre Denim Lavado', 'Rebajas', 629.00, 899.00, 30, 8, 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=600', 'Azul Medio', 'S, M'),
            ('Top Tejido Manga Larga Transparencias', 'Rebajas', 399.00, 599.00, 33, 15, 'https://images.unsplash.com/photo-1618244972963-dbee1a7edc95?w=600', 'Lila, Negro', 'XS, S, M'),
            ('Falda Mini Tablada Escocesa', 'Rebajas', 419.00, 599.00, 30, 14, 'https://images.unsplash.com/photo-1582142839970-2b9322773f5f?w=600', 'Rojo/Negro', 'S, M'),
            ('Vestido Camisero Popelina Manga Corta', 'Rebajas', 699.00, 999.00, 30, 9, 'https://images.unsplash.com/photo-1572804013309-59a88b7e92f1?w=600', 'Azul Marino', 'M, L'),
            ('Pantalón Culotte Tiro Alto', 'Rebajas', 529.00, 759.00, 30, 11, 'https://images.unsplash.com/photo-1506629082955-511b1aa562c8?w=600', 'Terracota', 'S, M, L'),
            ('Blazer Crop Tweed Botones', 'Rebajas', 899.00, 1299.00, 30, 6, 'https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=600', 'Blanco/Negro', 'S, M'),
            ('Top Halter Tejido Calado Summer', 'Rebajas', 299.00, 499.00, 40, 20, 'https://images.unsplash.com/photo-1539109136881-3be0616acf4b?w=600', 'Crudo', 'XS, S, M'),
            ('Falda Midi Satinada Sesgada', 'Rebajas', 599.00, 899.00, 33, 7, 'https://images.unsplash.com/photo-1512436991641-6745cdb1723f?w=600', 'Menta', 'S, M'),

            # CONJUNTOS
            ('Conjunto Sastre Crop Blazer y Shorts', 'Conjuntos', 1699.00, None, 0, 10, 'https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=600', 'Beige, Negro', 'XS, S, M, L'),
            ('Conjunto Lino Top y Pantalón Wide Leg', 'Conjuntos', 1499.00, None, 0, 12, 'https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=600', 'Arena, Blanco', 'S, M, L'),
            ('Set Satinado Camisa y Pantalón Fluido', 'Conjuntos', 1899.00, None, 0, 8, 'https://images.unsplash.com/photo-1585487000160-6ebcfceb0d03?w=600', 'Champagne, Olivo', 'S, M, L'),
            ('Set Tejido Rib Top y Falda Midi', 'Conjuntos', 1299.00, None, 0, 15, 'https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?w=600', 'Camel, Gris', 'XS, S, M'),
            ('Conjunto Biker y Top Deportivo Seamless', 'Conjuntos', 899.00, None, 0, 20, 'https://images.unsplash.com/photo-1506629082955-511b1aa562c8?w=600', 'Negro, Moka', 'XS, S, M, L'),
            ('Set Chaleco Sastre y Pantalón Recto', 'Conjuntos', 1999.00, None, 0, 9, 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=600', 'Gris Jaspe, Marfil', 'S, M, L'),
            ('Conjunto Playero Top Bardo y Falda Maxi', 'Conjuntos', 1399.00, None, 0, 11, 'https://images.unsplash.com/photo-1496747611176-843222e1e57c?w=600', 'Blanco', 'XS, S, M'),
            ('Set Denim Top Corsé y Falda Mini', 'Conjuntos', 1599.00, None, 0, 7, 'https://images.unsplash.com/photo-1582142839970-2b9322773f5f?w=600', 'Azul Claro', 'S, M'),
            ('Conjunto Monocromático Top Halter y Palazzo', 'Conjuntos', 1799.00, None, 0, 14, 'https://images.unsplash.com/photo-1509631179647-0177331693ae?w=600', 'Negro, Rojo', 'XS, S, M, L'),
            ('Set Loungewear Sudadera y Jogger', 'Conjuntos', 1199.00, None, 0, 18, 'https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=600', 'Crema, Verde Melange', 'S, M, L, XL')
        ]
        
        cursor.executemany('''
            INSERT INTO productos (nombre, categoria, precio, precio_original, descuento, stock, imagen, colores, tallas)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', productos)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()