from models import Producto
from difflib import SequenceMatcher

def search_product(item_name, item_price):
    """
    Busca el producto más similar basado en el nombre (`nomproducto`) y el precio (`prventa`) desde la base de datos.

    Args:
        item_name (str): Nombre del item buscado.
        item_price (float): Precio del item buscado.

    Returns:
        dict: El producto más cercano o None si no se encuentra.
    """
    # Obtener todos los productos de la base de datos
    products = Producto.query.all()

    # Convertir los productos a una lista de diccionarios
    product_list = [
        {"idprod": p.idprod, "name": p.nomproducto, "price": p.prventa} for p in products
    ]

    # Usar el algoritmo para encontrar el producto más cercano
    max_similarity = 0
    closest_product = None

    for product in product_list:
        # Calcular la similitud de nombres
        similarity = SequenceMatcher(None, product["name"], item_name).ratio()

        # Si la similitud es mayor al máximo actual
        if similarity > max_similarity:
            max_similarity = similarity
            closest_product = product
        elif similarity == max_similarity:
            # Si hay un empate en similitud, comparar por precio más cercano
            if abs(product["price"] - item_price) < abs(closest_product["price"] - item_price):
                closest_product = product

    return closest_product
