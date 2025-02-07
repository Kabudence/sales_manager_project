from models import Producto
from difflib import SequenceMatcher

def normalize_text(text):
    """ Convierte el texto a minúsculas y elimina espacios extra """
    return " ".join(text.lower().strip().split())

def calculate_score(item_name, product_name):
    """
    Calcula un puntaje basado en la coincidencia de palabras y penaliza palabras adicionales.
    """
    item_words = set(item_name.split())  # Palabras del nombre buscado
    product_words = set(product_name.split())  # Palabras del producto

    matches = item_words & product_words  # Palabras en común
    extra_words = product_words - item_words  # Palabras adicionales en el producto

    # Porcentaje de palabras coincidentes respecto al total buscado
    match_ratio = len(matches) / len(item_words)

    # Penalizar palabras adicionales (cuantas más palabras adicionales, menor el puntaje)
    penalty = len(extra_words) / len(product_words)

    # Puntaje total: 80% palabras coincidentes - 20% penalización por palabras adicionales
    final_score = (0.8 * match_ratio) - (0.2 * penalty)
    return final_score

def search_product(item_name, item_price):
    """
    Busca el producto más similar basado en el nombre (`nomproducto`) y el precio (`prventa`).

    Args:
        item_name (str): Nombre del item buscado.
        item_price (float): Precio del item buscado.

    Returns:
        dict: El producto más cercano o None si no se encuentra.
    """
    # Normalizar el nombre de búsqueda
    item_name = normalize_text(item_name)

    # Obtener todos los productos de la base de datos
    products = Producto.query.all()

    # Convertir los productos a una lista de diccionarios incluyendo `pr_costo`
    product_list = [
        {
            "idprod": p.idprod,
            "name": normalize_text(p.nomproducto),  # Normalizar nombres de productos
            "price": p.prventa,
            "cost": p.pr_costo
        }
        for p in products
    ]

    # Variables para almacenar el producto más similar
    max_score = float('-inf')
    closest_product = None

    for product in product_list:
        # Calcular puntaje de coincidencia
        score = calculate_score(item_name, product["name"])

        # Si el puntaje es mayor al máximo actual
        if score > max_score:
            max_score = score
            closest_product = product
        elif score == max_score:
            # Si hay empate, priorizar el precio más cercano
            if abs(product["price"] - item_price) < abs(closest_product["price"] - item_price):
                closest_product = product

    return closest_product
