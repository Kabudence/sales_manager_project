import re
from difflib import SequenceMatcher
from models import Producto


def normalize_text(text):
    """Convierte el texto a minúsculas y elimina espacios extra."""
    return " ".join(text.lower().strip().split())


def custom_tokenize(text):
    """
    Tokeniza el texto extrayendo palabras y dividiendo tokens compuestos que contienen
    indicadores de género ('varon' o 'mujer').
    """
    tokens = re.findall(r'\w+', text.lower())
    refined_tokens = []
    for token in tokens:
        # Si el token contiene 'varon' y no es exactamente 'varon'
        if 'varon' in token and token != 'varon':
            # Si termina en 'varon', separamos el prefijo
            if token.endswith('varon'):
                prefix = token[:-5]
                if prefix:
                    refined_tokens.append(prefix)
                refined_tokens.append('varon')
            else:
                refined_tokens.append(token)
        # Caso similar para 'mujer'
        elif 'mujer' in token and token != 'mujer':
            if token.endswith('mujer'):
                prefix = token[:-5]
                if prefix:
                    refined_tokens.append(prefix)
                refined_tokens.append('mujer')
            else:
                refined_tokens.append(token)
        else:
            refined_tokens.append(token)
    return refined_tokens


def calculate_score(item_name, product_name):
    """
    Calcula un puntaje combinando:
      - Similitud global (SequenceMatcher)
      - Comparación basada en tokens (con tokenización personalizada)
      - Penalización en caso de discrepancia de género
    """
    # Normalizar los textos
    norm_item = normalize_text(item_name)
    norm_product = normalize_text(product_name)

    # Tokenización personalizada
    item_tokens = set(custom_tokenize(norm_item))
    product_tokens = set(custom_tokenize(norm_product))

    # Detección de palabras clave de género
    gender_keywords = {"varon", "mujer"}
    item_gender = gender_keywords.intersection(item_tokens)
    product_gender = gender_keywords.intersection(product_tokens)

    # Penalización si ambos indican género pero no coinciden
    gender_penalty = 0
    if item_gender and product_gender and item_gender != product_gender:
        gender_penalty = 0.2  # ajuste según tus necesidades

    # Puntaje basado en tokens
    matches = item_tokens & product_tokens
    extra = product_tokens - item_tokens
    match_ratio = len(matches) / len(item_tokens) if item_tokens else 0
    penalty = len(extra) / len(product_tokens) if product_tokens else 0
    token_score = (0.8 * match_ratio) - (0.2 * penalty)

    # Similitud global usando SequenceMatcher
    overall_ratio = SequenceMatcher(None, norm_item, norm_product).ratio()

    # Combinamos ambos métodos y aplicamos la penalización por género
    final_score = 0.5 * overall_ratio + 0.5 * token_score - gender_penalty
    return final_score


def search_product(item_name, item_price):
    """
    Busca el producto más similar basándose en el nombre y el precio.
    Se utiliza la función robusta de cálculo de score.
    """
    norm_item_name = normalize_text(item_name)

    # Obtener productos de la base de datos y normalizar sus nombres
    products = Producto.query.all()
    product_list = [
        {
            "idprod": p.idprod,
            "name": normalize_text(p.nomproducto),
            "price": p.prventa,
            "cost": p.pr_costo
        }
        for p in products
    ]

    max_score = float('-inf')
    closest_product = None

    for product in product_list:
        score = calculate_score(norm_item_name, product["name"])

        if score > max_score:
            max_score = score
            closest_product = product
        elif score == max_score:
            # En caso de empate, se selecciona el que tenga precio más cercano
            if abs(product["price"] - item_price) < abs(closest_product["price"] - item_price):
                closest_product = product

    return closest_product
