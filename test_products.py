"""
Test the Real Food Score algorithm with real product examples.

These ingredient lists are based on actual products to validate
the scoring algorithm against intuitive expectations.
"""

from scoring import RealFoodScorer
import json


# ============================================================
# TEST PRODUCTS (real ingredient lists)
# ============================================================

TEST_PRODUCTS = [
    # --- EXPECTED: A Grade (Whole foods) ---
    {
        "name": "Fresh Eggs (dozen)",
        "ingredients": "eggs",
        "expected_grade": "A",
    },
    {
        "name": "Plain Greek Yogurt (Fage)",
        "ingredients": "milk, cream, live active cultures",
        "expected_grade": "A",
    },
    {
        "name": "Simple Bread (Whole Foods)",
        "ingredients": "whole wheat flour, water, olive oil, sea salt, yeast",
        "expected_grade": "A",
    },
    {
        "name": "Kerrygold Butter",
        "ingredients": "cream, salt",
        "expected_grade": "A",
    },
    {
        "name": "Baby Carrots",
        "ingredients": "carrots",
        "expected_grade": "A",
    },

    # --- EXPECTED: B Grade (Minimally processed, some additives) ---
    {
        "name": "Dave's Killer Bread",
        "ingredients": "whole wheat flour, water, wheat gluten, cane sugar, oats, sunflower seeds, molasses, sea salt, yeast, cultured wheat flour",
        "expected_grade": "B",
    },
    {
        "name": "Rao's Marinara Sauce",
        "ingredients": "tomatoes, olive oil, onions, salt, garlic, basil, black pepper, oregano",
        "expected_grade": "A",
    },
    {
        "name": "Applegate Uncured Bacon",
        "ingredients": "pork, water, salt, cane sugar, celery powder",
        "expected_grade": "B",
    },

    # --- EXPECTED: C Grade (Processed, multiple flags) ---
    {
        "name": "Heinz Ketchup",
        "ingredients": "tomato concentrate, distilled vinegar, high fructose corn syrup, corn syrup, salt, spice, onion powder, natural flavoring",
        "expected_grade": "C",
    },
    {
        "name": "Skippy Peanut Butter",
        "ingredients": "roasted peanuts, sugar, hydrogenated vegetable oils, salt",
        "expected_grade": "C",
    },

    # --- EXPECTED: D Grade (Heavily processed) ---
    {
        "name": "Oscar Mayer Bologna",
        "ingredients": "mechanically separated chicken, pork, water, corn syrup, contains less than 2% of salt, sodium lactate, flavor, sodium phosphates, autolyzed yeast, sodium diacetate, sodium ascorbate, sodium nitrite, dextrose",
        "expected_grade": "D",
    },
    {
        "name": "Cool Whip",
        "ingredients": "water, hydrogenated vegetable oil, high fructose corn syrup, corn syrup, skim milk, light cream, sodium caseinate, natural and artificial flavor, xanthan and guar gums, polysorbate 60, sorbitan monostearate, beta carotene",
        "expected_grade": "D",
    },

    # --- EXPECTED: F Grade (Ultra-processed) ---
    {
        "name": "Doritos Nacho Cheese",
        "ingredients": "corn, vegetable oil (corn, canola, sunflower), maltodextrin, salt, cheddar cheese, whey, monosodium glutamate, buttermilk, romano cheese, whey protein concentrate, onion powder, corn flour, natural and artificial flavors, dextrose, tomato powder, lactose, spices, artificial color (red 40, yellow 6, yellow 5, blue 1), lactic acid, citric acid, sugar, garlic powder, skim milk, red and green bell pepper powder, disodium inosinate, disodium guanylate",
        "expected_grade": "F",
    },
    {
        "name": "Mountain Dew",
        "ingredients": "carbonated water, high fructose corn syrup, concentrated orange juice, citric acid, natural flavor, sodium benzoate, caffeine, sodium citrate, erythorbic acid, gum arabic, calcium disodium edta, brominated vegetable oil, yellow 5",
        "expected_grade": "F",
    },
    {
        "name": "Pop-Tarts Frosted Strawberry",
        "ingredients": "enriched flour, corn syrup, high fructose corn syrup, dextrose, soybean and palm oil, sugar, bleached wheat flour, strawberry puree concentrate, salt, dried strawberries, dried pears, dried apples, leavening, cornstarch, gelatin, modified wheat starch, xanthan gum, soy lecithin, red 40, caramel color, yellow 6, blue 1",
        "expected_grade": "F",
    },
]


def run_tests():
    """Run all test products through the scorer."""
    scorer = RealFoodScorer()

    print("=" * 70)
    print("REAL FOOD SCORE - PRODUCT ANALYSIS")
    print("Based on realfood.gov 2025 Dietary Guidelines")
    print("=" * 70)
    print()

    results = []
    grade_matches = 0

    for product in TEST_PRODUCTS:
        result = scorer.score_product(product["name"], product["ingredients"])
        result["expected_grade"] = product["expected_grade"]
        result["grade_match"] = result["grade"] == product["expected_grade"]

        if result["grade_match"]:
            grade_matches += 1

        results.append(result)

        # Print summary
        match_icon = "✓" if result["grade_match"] else "✗"
        print(f"{match_icon} {product['name']}")
        print(f"  Score: {result['score']}/100 | Grade: {result['grade']} (expected: {product['expected_grade']})")
        print(f"  Ingredients: {result['ingredient_count']}")
        print(f"  Breakdown: Simplicity={result['breakdown']['ingredient_simplicity']}, "
              f"Clean={result['breakdown']['clean_ingredients']}, "
              f"Whole Foods={result['breakdown']['whole_food_ratio']}")

        if result["flags"]:
            print(f"  Flags: {', '.join(result['flags'])}")

        print()

    # Summary
    print("=" * 70)
    print(f"ACCURACY: {grade_matches}/{len(TEST_PRODUCTS)} grade predictions matched")
    print("=" * 70)

    return results


def score_custom_product():
    """Interactive mode for scoring custom products."""
    scorer = RealFoodScorer()

    print("\n" + "=" * 70)
    print("CUSTOM PRODUCT SCORER")
    print("=" * 70)

    name = input("\nProduct name: ")
    ingredients = input("Ingredient list (comma-separated): ")

    result = scorer.score_product(name, ingredients)

    print("\n" + "-" * 40)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    results = run_tests()

    # Optionally run interactive mode
    # score_custom_product()
