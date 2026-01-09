"""
Barcode/UPC lookup integration using Open Food Facts API.

Open Food Facts is a free, open database of food products with:
- Ingredient lists
- Nutrition data
- Product images
- Barcode/UPC lookups

API Docs: https://wiki.openfoodfacts.org/API
"""

import urllib.request
import urllib.parse
import json
from typing import Optional
from scoring import RealFoodScorer


# Open Food Facts API base URL
OFF_API_BASE = "https://world.openfoodfacts.org/api/v2"


def lookup_barcode(barcode: str) -> Optional[dict]:
    """
    Look up a product by barcode/UPC using Open Food Facts.

    Args:
        barcode: UPC, EAN, or other barcode number

    Returns:
        Product data dict or None if not found
    """
    # Clean barcode (remove spaces, dashes)
    barcode = barcode.replace(" ", "").replace("-", "")

    url = f"{OFF_API_BASE}/product/{barcode}.json"

    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "RealFoodScore/1.0 (demo app)"}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())

            if data.get("status") != 1:
                return None

            product = data.get("product", {})

            return {
                "barcode": barcode,
                "name": product.get("product_name", "Unknown Product"),
                "brand": product.get("brands", ""),
                "ingredients_text": product.get("ingredients_text", ""),
                "ingredients_list": [
                    ing.get("text", "")
                    for ing in product.get("ingredients", [])
                ],
                "image_url": product.get("image_url", ""),
                "nutriscore": product.get("nutriscore_grade", ""),
                "nova_group": product.get("nova_group", ""),  # 1-4 processing level
                "categories": product.get("categories", ""),
            }

    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise
    except Exception as e:
        print(f"Error looking up barcode {barcode}: {e}")
        return None


def search_products(query: str, page: int = 1, page_size: int = 10) -> list[dict]:
    """
    Search for products by name.

    Args:
        query: Search term
        page: Page number (1-indexed)
        page_size: Results per page

    Returns:
        List of product summaries
    """
    params = urllib.parse.urlencode({
        "search_terms": query,
        "page": page,
        "page_size": page_size,
        "json": 1,
    })

    url = f"https://world.openfoodfacts.org/cgi/search.pl?{params}"

    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "RealFoodScore/1.0 (demo app)"}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())

            products = []
            for p in data.get("products", []):
                products.append({
                    "barcode": p.get("code", ""),
                    "name": p.get("product_name", "Unknown"),
                    "brand": p.get("brands", ""),
                    "ingredients_text": p.get("ingredients_text", ""),
                    "image_url": p.get("image_small_url", ""),
                })

            return products

    except Exception as e:
        print(f"Error searching products: {e}")
        return []


def score_barcode(barcode: str) -> Optional[dict]:
    """
    Look up a barcode and return Real Food Score.

    Args:
        barcode: UPC/EAN barcode

    Returns:
        Score result with product info, or None if not found
    """
    product = lookup_barcode(barcode)

    if not product:
        return None

    # Get ingredients - prefer structured list, fall back to text
    ingredients = product.get("ingredients_text", "")
    if not ingredients and product.get("ingredients_list"):
        ingredients = ", ".join(product["ingredients_list"])

    if not ingredients:
        return {
            "product": product,
            "error": "No ingredient data available for this product"
        }

    # Score the product
    scorer = RealFoodScorer()
    result = scorer.score_product(product["name"], ingredients)

    # Add product metadata
    result["product_info"] = {
        "barcode": product["barcode"],
        "brand": product["brand"],
        "image_url": product["image_url"],
        "nova_group": product["nova_group"],  # Compare our score to NOVA
        "nutriscore": product["nutriscore"],
    }

    return result


# ============================================================
# CLI for testing
# ============================================================

if __name__ == "__main__":
    import sys

    print("=" * 60)
    print("REAL FOOD SCORE - BARCODE LOOKUP")
    print("Using Open Food Facts database")
    print("=" * 60)

    if len(sys.argv) > 1:
        # Barcode provided as argument
        barcode = sys.argv[1]
    else:
        # Interactive mode
        barcode = input("\nEnter barcode (or product name to search): ").strip()

    # Check if it's a barcode (all digits) or search query
    if barcode.isdigit():
        print(f"\nLooking up barcode: {barcode}...")
        result = score_barcode(barcode)

        if result is None:
            print("Product not found in database.")
        elif "error" in result:
            print(f"Found: {result['product']['name']}")
            print(f"Error: {result['error']}")
        else:
            print(f"\nProduct: {result['product']}")
            if result.get('product_info', {}).get('brand'):
                print(f"Brand: {result['product_info']['brand']}")

            s = result['scores']
            print(f"\n  MAHA (RFK):  {s['rfk']['score']:5.1f} ({s['rfk']['grade']})")
            print(f"  Guideline:  {s['guideline']['score']:5.1f} ({s['guideline']['grade']})")
            print(f"  Practical:  {s['practical']['score']:5.1f} ({s['practical']['grade']})")

            if result.get('product_info', {}).get('nova_group'):
                print(f"\n  NOVA Group: {result['product_info']['nova_group']} (for comparison)")

            if result['flags']:
                print(f"\n  Flags: {', '.join(result['flags'])}")
    else:
        print(f"\nSearching for: {barcode}...")
        products = search_products(barcode, page_size=5)

        if not products:
            print("No products found.")
        else:
            print(f"\nFound {len(products)} products:\n")
            for i, p in enumerate(products, 1):
                print(f"  {i}. {p['name']} ({p['brand']})")
                print(f"     Barcode: {p['barcode']}")
                if p['ingredients_text']:
                    preview = p['ingredients_text'][:60] + "..." if len(p['ingredients_text']) > 60 else p['ingredients_text']
                    print(f"     Ingredients: {preview}")
                print()
