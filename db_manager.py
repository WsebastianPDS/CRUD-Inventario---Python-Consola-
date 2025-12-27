# ENTREGA DE TRABAJO FINAL: BD - Inventario de Artículos
# Alumno: William Sebastian Pinto Da Silva
# DNI: 42.615.614

import sqlite3 # Importamos el módulo necesario para trabajar con bases de datos SQLite.

DB_NAME = 'inventario.db' # Nombre del archivo donde guardaremos todos los datos de nuestro inventario.

def conectar(): # Establece la conexión con la base de datos.
    try:
        conn = sqlite3.connect(DB_NAME) # Intentamos conectar a nuestro archivo DB_NAME (lo crea si no existe).
        return conn # Si todo sale bien, devolvemos el objeto de conexión para usarlo.
    except sqlite3.Error as e:
        print(f"Error al conectar con la base de datos: {e}") # Capturamos y mostramos el error si la conexión falla.
        return None # Devolvemos None si no pudimos conectar.

def crear_tabla(): # Crea la tabla 'productos' si no existe, con todas las columnas requeridas.
    conn = conectar() # Llamamos a la función para obtener la conexión.
    if conn:
        cursor = conn.cursor() # Creamos un cursor, que es el que ejecuta los comandos SQL.
        try:
            # Definición de la tabla 'productos'
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS productos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,   -- La clave única para cada artículo, se genera sola.
                    nombre TEXT NOT NULL,                  -- El nombre del producto, no puede estar vacío.
                    descripcion TEXT,                      -- Una descripción más larga.
                    cantidad INTEGER NOT NULL,             -- El stock disponible, debe ser un número entero.
                    precio REAL NOT NULL,                  -- El precio, acepta decimales (REAL).
                    categoria TEXT                         -- La categoría a la que pertenece el artículo.
                );
            """)
            conn.commit() # Guardamos los cambios de la estructura en el archivo de la base de datos.
            print("Tabla 'productos' creada con éxito.")
        except sqlite3.Error as e:
            print(f"Error al crear la tabla: {e}") # Error si la sintaxis SQL falla.
        finally:
            conn.close() # Siempre cerramos la conexión para liberar el archivo.


# --- FUNCIONES CRUD (CREATE, READ, UPDATE, DELETE) ---

crear_tabla()

def insertar_producto(nombre, descripcion, cantidad, precio, categoria): # Inserta un nuevo producto en la tabla 'productos'.
    conn = conectar() # Abrimos la conexión.
    if conn:
        cursor = conn.cursor() # Obtenemos el cursor.
        try:
            # Sentencia SQL de inserción con '?' como marcadores de posición para seguridad.
            sql = """
                INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria) 
                VALUES (?, ?, ?, ?, ?);
            """
            cursor.execute(sql, (nombre, descripcion, cantidad, precio, categoria)) # Ejecutamos el comando con los datos en una tupla.
            conn.commit() # Confirmamos la transacción para que el producto se guarde.
            return True # Indicamos que la inserción fue exitosa.
        except sqlite3.Error as e:
            print(f"Error al insertar el producto: {e}") # Si hay un error de DB (ej. no cumple NOT NULL).
            return False # Indicamos que falló.
        finally:
            conn.close() # Cerramos la conexión.

def buscar_productos_por_nombre(nombre_buscar): # Busca productos por una coincidencia parcial en el nombre.
    conn = conectar() # Abrimos la conexión.
    if conn:
        cursor = conn.cursor() # Obtenemos el cursor.
        try:
            # Buscamos por el ID exacto.
            sql = "SELECT id, nombre, descripcion, cantidad, precio, categoria FROM productos WHERE nombre LIKE ?;"
            cursor.execute(sql, ('%' + nombre_buscar + '%',)) 
            productos = cursor.fetchall() # Traemos todos los resultados en forma de lista de tuplas.
            return productos # Devolvemos la lista de productos encontrados.
        except sqlite3.Error as e:
            print(f"Error al buscar productos: {e}") 
            return [] # Devolvemos una lista vacía si falla.
        finally: 
            conn.close() # Cerramos la conexión.

def seleccionar_todos_productos(): # Recupera todos los productos de la tabla 'productos'.
    conn = conectar() # Abrimos la conexión.
    if conn:
        cursor = conn.cursor() # Obtenemos el cursor.
        try:
            # Seleccionamos todas las columnas.
            cursor.execute("SELECT id, nombre, descripcion, cantidad, precio, categoria FROM productos ORDER BY id ASC")
            productos = cursor.fetchall()
            return productos # Devolvemos la lista completa de productos.
        except sqlite3.Error as e: 
            print(f"Error al recuperar productos: {e}") 
            return [] # Devolvemos una lista vacía si falla.
        finally: 
            conn.close() # Cerramos la conexión.

# Función para eliminar un producto
def eliminar_producto_por_id(producto_id): # Elimina un producto de la tabla 'productos' usando su ID.
    conn = conectar()  # Abrimos la conexión.
    if conn:
        cursor = conn.cursor() # Obtenemos el cursor.
        try:
            # DELETE por ID es el requisito de la entrega final.
            cursor.execute("DELETE FROM productos WHERE id = ?", (producto_id,))
            conn.commit() # Confirmamos la transacción.
            return cursor.rowcount > 0 # Retorna True si se eliminó al menos una fila.
        except sqlite3.Error as e: 
            print(f"Error al eliminar el producto: {e}")
            return False # Indicamos que falló.
        finally:
            conn.close() # Cerramos la conexión.

# Función para actualizar un producto (UPDATE)
def actualizar_producto_por_id(producto_id, nombre, descripcion, cantidad, precio, categoria): # Actualiza todos los campos de un producto específico por su ID.
    conn = conectar() # Abrimos la conexión.
    if conn: 
        cursor = conn.cursor() # Obtenemos el cursor.
        try:
            # UPDATE con todos los campos.
            sql = """
                UPDATE productos 
                SET nombre = ?, descripcion = ?, cantidad = ?, precio = ?, categoria = ? 
                WHERE id = ?;
            """
            cursor.execute(sql, (nombre, descripcion, cantidad, precio, categoria, producto_id)) # Ejecutamos el comando con los datos en una tupla.
            conn.commit() # Confirmamos la transacción.
            return cursor.rowcount > 0 # Retorna True si se actualizó al menos una fila.
        except sqlite3.Error as e: 
            print(f"Error al actualizar el producto: {e}")
            return False # Indicamos que falló.
        finally:
            conn.close() # Cerramos la conexión.

# Función para el reporte por cantidad (SELECT con WHERE)
def reporte_por_cantidad_minima(limite): # Genera un reporte de productos con cantidad menor o igual al límite.
    conn = conectar() # Abrimos la conexión.
    if conn:
        cursor = conn.cursor() # Obtenemos el cursor.
        try:
            # Filtramos por la columna 'cantidad' <= al límite.
            sql = "SELECT id, nombre, descripcion, cantidad, precio, categoria FROM productos WHERE cantidad <= ? ORDER BY cantidad ASC;"
            cursor.execute(sql, (limite,)) 
            productos = cursor.fetchall() # Traemos todos los resultados en forma de lista de tuplas.
            return productos # Devolvemos la lista de productos encontrados.
        except sqlite3.Error as e:
            print(f"Error al generar reporte: {e}") 
            return [] # Devolvemos una lista vacía si falla.
        finally:
            conn.close()    

def obtener_producto_por_id(producto_id): #Obtiene un producto específico de la tabla 'productos' por su ID
    conn = conectar() # Abrimos la conexión.
    if conn:
        cursor = conn.cursor() # Obtenemos el cursor.
        try:
            # Seleccionamos todas las columnas para el ID dado.
            sql = "SELECT nombre, descripcion, cantidad, precio, categoria FROM productos WHERE id = ?;" 
            cursor.execute(sql, (producto_id,)) 
            producto = cursor.fetchone() # Usamos fetchone() para obtener un solo resultado
            return producto # Devolvemos la tupla del producto encontrado o None si no existe.
        except sqlite3.Error as e: 
            print(f"Error al obtener producto: {e}") 
            return None # Devolvemos None si falla.
        finally: 
            conn.close() # Cerramos la conexión.

def resetear_ids(): # Elimina todos los productos y reinicia el contador de IDs.
    conn = conectar() # Abrimos la conexión.
    if conn:
        cursor = conn.cursor() # Obtenemos el cursor.
        try:
            # Eliminamos todos los registros y reseteamos el AUTOINCREMENT
            cursor.execute("DELETE FROM productos;")  # Borra todos los registros
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='productos';")  # Resetea IDs
            conn.commit() # Confirmamos la transacción.
            return True # Indicamos que la operación fue exitosa.
        except sqlite3.Error as e:
            print(f"Error al resetear los IDs: {e}")
            return False # Indicamos que falló.
        finally:
            conn.close() # Cerramos la conexión.

