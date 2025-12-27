# ENTREGA DE TRABAJO FINAL: CRUD - Inventario de Artículos
# Alumno: William Sebastian Pinto Da Silva
# DNI: 42.615.614

# Importamos todas las funciones necesarias del gestor de base de datos.
from db_manager import (
    crear_tabla, # Función para asegurar que la tabla existe.
    insertar_producto, # Función para agregar un nuevo producto.
    seleccionar_todos_productos, # Función para mostrar la lista completa.
    buscar_productos_por_nombre, # Función de búsqueda opcional.
    eliminar_producto_por_id, # Función para borrar por ID.
    actualizar_producto_por_id, # Función para modificar un producto.
    reporte_por_cantidad_minima, # Función para generar el reporte de stock.
    obtener_producto_por_id, # Función clave para la lógica de actualización.
    resetear_ids # Función oculta para utilidad (borrar todo).
) 

crear_tabla() # Llamamos a esta función al iniciar para que la base de datos esté lista.
ancho = 90 # Defino el ancho que voy a usar para centrar títulos y formatear la tabla.

# ENCABEZADO 
def encabezado():
    print("\n" * 1) # Salto de línea.
    titulo = " CRUD - Inventario de Artículos " # Titulo.
    print("=" * ancho) # Línea superior.
    print(titulo.center(ancho)) # Centra el título.
    subrayado_titulo = "=" * len(titulo) # Subrayado del título.
    print(subrayado_titulo.center(ancho)) # Subrayado centrado.
    print("\n" * 1) # Salto de línea.
encabezado()

# MENÚ DE OPCIONES.
# Uso de ljust() y rjust() para alinear los textos a izquierda/derecha.
def menu():
    menu = " Menú de opciones " # declaro el menú.
    print(menu.center(ancho)) # Centro el menú.
    subrayado_menu = "-" * len(menu) # Subrayado del menú.
    print(subrayado_menu.center(ancho)) # Subrayado centrado.
    print("\n" * 1) # Salto de línea.
    # Se agregaron las opciones de Actualizar y Reporte.
    print("1. Agregar artículo".ljust(30) + "2. Mostrar artículos".center(30) + "3. Buscar artículo".rjust(30))
    print("4. Actualizar artículo".ljust(30) + "5. Eliminar artículo".center(30) + "6. Reporte stock  ".rjust(30)) 
    print("\n" * 1) # Salto de línea.
    print("7. Salir".center(ancho)) # Opción para salir.
    print("*. ⚠️  ¡Reiniciar base de datos! ⚠️".center(ancho))
    print("=" * ancho) # Línea inferior.


# ====================================================================
# FUNCIONALIDADES DEL INVENTARIO (Lógica de interfaz y validaciones)
# ====================================================================

# Función 1: Agregar artículos (CREATE).
def agregar_articulos():
    print("\n" * 1) # Salto de línea.

    # 1. Recopilación y Validación de Nombre (Obligatorio).
    nombre = input("📂​  Ingrese el nombre del artículo (Obligatorio): ").capitalize().strip()
    if not nombre:
        print("\n" * 1)
        print("❌  ¡Error!: El nombre del artículo no puede estar vacío. ⚠️​")
        return # Sale de la función si el nombre es vacío
        
    # 2. Recopilación de Descripción y Categoría.
    descripcion = input("📝  Ingrese la descripción del artículo: ").capitalize().strip()
    categoria = input("🗂️​  Ingrese la categoría del artículo: ").capitalize().strip()
    
    # 3. Recopilación y Validación de Cantidad (Debe ser un número entero >= 0).
    try:
        cantidad = int(input("📦  Ingrese la cantidad disponible (Obligatorio): ")) # Lo combertimos en entero
        if cantidad < 0:
            print("\n" * 1)
            print("❌  ¡Error!: La cantidad no puede ser negativa. ⚠️​")
            return
    except ValueError:
        print("\n" * 1)
        print("❌  ¡Error!: La cantidad debe ser un número entero. ⚠️​")
        return # Si no es un número, mostramos error.
        
    # 4. Recopilación y Validación de Precio
    try:
        precio = float(input("💵​​  Ingrese el precio del artículo (Obligatorio): ")) # El precio en BD es REAL (float).
        if precio <= 0:
            print("\n" * 1)
            print("❌  ¡Error!: El precio debe ser un número positivo. ⚠️​")
            return
    except ValueError:
        print("\n" * 1)
        print("❌  ¡Error!: El precio debe ser un número. ⚠️​")
        return
        
    # 5. Insertar en la Base de Datos
    if insertar_producto(nombre, descripcion, cantidad, precio, categoria):
        print("\n" * 1) # Salto de línea.
        print(f"✅  El artículo '{nombre}' fue agregado con éxito a la base de datos.") # Confirma que el artículo fue agregado.
    else:
        print("\n" * 1)
        print("❌  Error desconocido al intentar agregar el artículo.")


# Función 2: Mostrar artículos (READ completo, con formato tabular).
def mostrar_articulos(productos=None):
    # Si no se pasan productos (Opción 2), los obtenemos todos de la BD.
    if productos is None:
        productos = seleccionar_todos_productos()

    if not productos: # Si la lista de productos está vacía.
        print("\n" * 1) # Salto de línea.
        print("❌  No hay artículos registrados en la base de datos.") # Indica que no hay artículos.
    else:
        print("\n" * 1)
        print("📝  Lista de artículos registrados:".center(ancho)) 
        print("=" * ancho) 
        
    # Definición de anchos fijos para las columnas (Ajustados para ancho=90)
        ANCHO_ID = 4
        ANCHO_NOMBRE = 20
        ANCHO_DESCRIPCION = 25
        ANCHO_CANTIDAD = 10
        ANCHO_PRECIO = 16
        ANCHO_CATEGORIA = 19
        
        # 1. Imprimir encabezados de la tabla
        header = (
            "ID".ljust(ANCHO_ID) + 
            "NOMBRE".ljust(ANCHO_NOMBRE) + 
            "DESCRIPCIÓN".ljust(ANCHO_DESCRIPCION) +
            "CANTIDAD".center(ANCHO_CANTIDAD) + 
            "PRECIO".rjust(ANCHO_PRECIO) + "    " +
            "CATEGORÍA".ljust(ANCHO_CATEGORIA) 
        )
        print(header) # Imprime el encabezado.
        print("-" * ancho) 

        # 2. Imprimir cada fila de datos
        for producto in productos:
            id, nombre, descripcion, cantidad, precio, categoria = producto
            
            precio_str = f"${precio:.2f}" # Formateamos el precio a 2 decimales con símbolo de dólar.

            fila = ( 
                str(id).ljust(ANCHO_ID) + 
                nombre[:ANCHO_NOMBRE].ljust(ANCHO_NOMBRE) + 
                descripcion[:ANCHO_DESCRIPCION].ljust(ANCHO_DESCRIPCION) + 
                str(cantidad).center(ANCHO_CANTIDAD) + 
                precio_str.rjust(ANCHO_PRECIO) + "    " +
                categoria[:ANCHO_CATEGORIA].ljust(ANCHO_CATEGORIA) 
            )
            print(fila)
            
        print("=" * ancho)
        print(f"Total de artículos: {len(productos)}") # Muestra el total de artículos listados.


# Función 3: Buscar artículos (READ por nombre).
def buscar_articulos(): 
    print("\n" * 1) # Salto de línea.
    nombre_buscar = input("🔍  Ingrese el nombre del artículo que desea buscar: ").capitalize().strip() 
    
    if not nombre_buscar: # Validación de entrada vacía.
        print("⚠️  Ingrese un criterio de búsqueda válido.")
        return # Sale si el criterio está vacío.

    encontrados = buscar_productos_por_nombre(nombre_buscar) # Llamamos a la función del gestor de BD.

    if encontrados: # Si encontró coincidencias.
        print("\n 🗃️  Resultados de la búsqueda:") 
        mostrar_articulos(encontrados)  # Reutilizamos la función de mostrar artículos.
    else:
        print("\n" * 1)
        print(f"❌  No se encontraron artículos que coincidan con '{nombre_buscar}'.") # Mensaje si no hay coincidencias.


# Función 4: Actualizar artículo (UPDATE). (Nueva funcionalidad)
def actualizar_articulos():
    print("\n" * 1)
    mostrar_articulos() # Mostramos la lista para que el usuario elija el ID.
    
    try:
        producto_id = int(input("✏️  Ingrese el ID del artículo que desea actualizar: ")) # Pedimos el ID a actualizar
    except ValueError: 
        print("⚠️  ¡Ingrese un ID válido! (número entero).")
        return # Sale si el ID no es un número.
        
    # Obtener el producto actual de la base de datos
    datos_actuales = obtener_producto_por_id(producto_id) # Usamos la función del gestor de BD.
    
    if datos_actuales is None:
        print(f"❌  No se encontró el artículo con ID {producto_id}.") 
        return # Sale si el ID no existe.

    # Desempaquetar los datos actuales para usarlos como valores por defecto
    nombre_actual, descripcion_actual, cantidad_actual, precio_actual, categoria_actual = datos_actuales
    
    print("\n" * 1)
    print("Ingrese los nuevos valores (deje en blanco para mantener el anterior): ") # Instrucciones.

    # 1. Recopilar Nombre y Texto
    # Si el input está vacío, mantiene el valor actual.
    nombre_nuevo = input(f"Nuevo Nombre (Actual: {nombre_actual}): ").capitalize().strip() or nombre_actual # Mantiene el actual si está vacío.
    descripcion_nueva = input(f"Nueva Descripción (Actual: {descripcion_actual}): ").capitalize().strip() or descripcion_actual # Mantiene el actual si está vacío.
    categoria_nueva = input(f"Nueva Categoría (Actual: {categoria_actual}): ").capitalize().strip() or categoria_actual # Mantiene el actual si está vacío.
    
    # 2. Manejo de Cantidad y Precio con validación
    try:
        cantidad_input = input(f"Nueva Cantidad (Actual: {cantidad_actual}): ") # Pedimos la nueva cantidad
        cantidad_nueva = int(cantidad_input) if cantidad_input else cantidad_actual # Mantenemos el actual si está vacío, sino convertimos a entero.
        
        if cantidad_nueva < 0:
            print("❌  ¡Error!: La cantidad no puede ser negativa. ⚠️​") # Validación de cantidad
            return
            
        precio_input = input(f"Nuevo Precio (Actual: {precio_actual}): ") # Pedimos el nuevo precio
        precio_nuevo = float(precio_input) if precio_input else precio_actual # Mantenemos el actual si está vacío, sino convertimos a float.
        
        if precio_nuevo <= 0:
            print("❌  ¡Error!: El precio debe ser positivo. ⚠️​")
            return
            
    except ValueError:
        print("⚠️  ¡Error!: La cantidad o el precio deben ser números.")
        return

    # 3. Llamar a la función de actualización de la BD con los nuevos valores
    if actualizar_producto_por_id(producto_id, nombre_nuevo, descripcion_nueva, cantidad_nueva, precio_nuevo, categoria_nueva):
        print("\n" * 1)
        print(f"✅  El artículo con ID {producto_id} fue actualizado correctamente.") # Confirma la actualización.
    else:
        print("\n" * 1)
        print(f"❌  Error desconocido al intentar actualizar el artículo con ID {producto_id}.") # Si falla la actualización.


# Función 5: Eliminar artículos (DELETE por ID).
def eliminar_articulos():
    mostrar_articulos() # Primero muestra los artículos existentes (por ID).
    
    try:
        print("\n" * 1) # Salto de línea.
        producto_id = int(input("🗑️  Ingrese el ID del artículo que desea eliminar: ")) # Pedimos el ID
        
        if eliminar_producto_por_id(producto_id): # Llamamos a la función de la BD para eliminar por ID.
            print("\n" * 1) # Salto de línea.
            print(f"🗑️ ✅  El artículo con ID {producto_id} fue eliminado correctamente.") # Confirma la eliminación.
        else:
            print("\n" * 1) # Salto de línea 
            print(f"❌  ¡ID inválido!, no se encontró el artículo con ID {producto_id}.") # Si el ID no existe devolvemos error.
            
    except ValueError:
        print("⚠️  ¡Ingrese un número válido para el ID! ⚠️​") # Si el usuario ingresa algo que no es un número.


# Función 6: Reporte por Cantidad (Stock Bajo).
def generar_reporte_stock():
    print("\n" * 1)
    
    try:
        limite = int(input("📊  Ingrese el límite de stock: "))
        if limite < 0:
            print("⚠️  El límite de stock no puede ser negativo.")
            return
    except ValueError:
        print("⚠️  ¡Ingrese un número válido! ⚠️​")
        return

    productos_bajo_stock = reporte_por_cantidad_minima(limite)  # Obtenemos los productos que cumplen el criterio.
    
    if productos_bajo_stock:
        print("\n REPORTE DE ARTÍCULOS CON STOCK BAJO ".center(ancho))
        print(f"Mostrando artículos con cantidad menor o igual a {limite}:".center(ancho))
        mostrar_articulos(productos_bajo_stock) # Usamos la función de mostrar para listar el reporte.
    else:
        print("\n" * 1)
        print("✅  ¡Buen trabajo! No se encontraron artículos con stock bajo el límite especificado.")

# BUCLE PRINCIPAL DEL MENÚ

while True: # Bucle infinito del menú hasta que el usuario decida salir.
    menu() # Imprimimos el menú en cada ciclo.
    print("\n" * 1) # Salto de línea.
    opcion = input("Seleccione una opción: ") # Le pedimos al usuario que elija.

    if opcion == "1": # Opción para CREAR.
        agregar_articulos()
    elif opcion == "2": # Opción para LEER (Mostrar todo).
        mostrar_articulos()
    elif opcion == "3": # Opción para LEER (Buscar).
        buscar_articulos()
    elif opcion == "4": # Opción para ACTUALIZAR.
        actualizar_articulos()
    elif opcion == "5": # Opción para ELIMINAR.
        eliminar_articulos()
    elif opcion == "6": # Opción para REPORTE.
        generar_reporte_stock()
    elif opcion == "7": # Opción para salir del programa.
        print("\n" * 1) # Salto de línea.
        print("Saliendo del sistema... ⌛")
        break # Rompe el bucle y finaliza el programa.
    elif opcion == "*": # Opción secreta para reiniciar la base de datos (DELETE ALL).
        confirm = input("⚠️  Esto eliminará TODOS los artículos y reseteará los IDs. ¿Confirmar? (s/n): ").lower()
        if confirm == "s":
            if resetear_ids():
                print("✅  Base de datos vaciada y IDs reiniciados correctamente.")
            else:
                print("❌  Error al intentar reiniciar la base de datos.")
        else:
            print("Operación cancelada.")
    else:
        print("\n" * 1) # Salto de línea 
        print("⚠️ ¡Opción no válida!⚠️  , intente nuevamente...") # Mensaje de error si la opción no existe. devolvemos error.
        print("\n" + "=" * ancho + "\n") # Separador para la próxima iteración del menú.