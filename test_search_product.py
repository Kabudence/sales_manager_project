from app import create_app  # Importar la aplicación Flask
from services.products_service import search_product

# Crea la aplicación Flask
app = create_app()

# Datos del item buscado
item_name = "SET CUNA NIÑA"
item_price = 500


# Ejecutar la búsqueda dentro del contexto de la aplicación
with app.app_context():
    result = search_product(item_name, item_price)

    # Mostrar el resultado
    if result:
        print(f"Producto encontrado: {result}")
    else:
        print("No se encontró un producto similar.")
