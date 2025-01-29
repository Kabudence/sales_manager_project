from services.products_service import search_product

# Datos del item buscado
item_name = "JGO MUEBLE REX (WILDER) + 01 MESA V"
item_price = 1269.07

# Ejecutar la búsqueda
result = search_product(item_name, item_price)

# Mostrar el resultado
if result:
    print(f"Producto encontrado: {result}")
else:
    print("No se encontró un producto similar.")
