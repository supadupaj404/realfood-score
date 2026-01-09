"""
Ingredient classification database.

These lists operationalize the realfood.gov guidelines into
searchable/matchable categories.
"""

# ============================================================
# FLAGGED INGREDIENTS (to avoid per guidelines)
# ============================================================

ADDED_SUGARS = {
    # Direct sugars
    "sugar", "cane sugar", "brown sugar", "raw sugar", "turbinado sugar",
    "powdered sugar", "confectioners sugar", "invert sugar", "coconut sugar",
    "demerara sugar", "muscovado sugar", "panela", "jaggery", "sucanat",
    "organic sugar", "evaporated cane juice", "cane juice crystals",

    # Syrups
    "high fructose corn syrup", "hfcs", "corn syrup", "maple syrup",
    "agave syrup", "agave nectar", "rice syrup", "brown rice syrup",
    "golden syrup", "malt syrup", "refiner's syrup", "sorghum syrup",
    "tapioca syrup", "glucose syrup", "glucose-fructose syrup",
    "isoglucose", "carob syrup", "yacon syrup",

    # -ose endings (chemical sugars)
    "glucose", "fructose", "dextrose", "sucrose", "maltose", "lactose",
    "galactose", "trehalose", "isomaltulose", "polydextrose",

    # Concentrates and extracts
    "fruit juice concentrate", "grape juice concentrate",
    "apple juice concentrate", "pear juice concentrate",
    "date syrup", "date paste", "honey",
    "concentrated fruit juice", "fruit juice from concentrate",

    # Other forms
    "molasses", "blackstrap molasses", "caramel", "dextrin", "maltodextrin",
    "barley malt", "malt extract", "ethyl maltol", "crystalline fructose",
    "florida crystals", "d-ribose", "mannose", "tagatose",
}

INDUSTRIAL_OILS = {
    # Seed/vegetable oils (industrial extraction)
    "vegetable oil", "soybean oil", "canola oil", "rapeseed oil",
    "corn oil", "sunflower oil", "safflower oil", "cottonseed oil",
    "grapeseed oil", "rice bran oil", "peanut oil", "sesame oil",

    # Hydrogenated variants (trans fats)
    "hydrogenated oil", "partially hydrogenated oil",
    "hydrogenated vegetable oil", "partially hydrogenated soybean oil",
    "hydrogenated cottonseed oil", "hydrogenated palm oil",
    "shortening", "margarine", "interesterified oil",

    # Blends and generic terms
    "vegetable oil blend", "frying oil", "cooking oil",
    "oil blend", "seed oil", "refined oil",

    # Specific industrial variants
    "high oleic sunflower oil", "high oleic canola oil",
    "expeller pressed canola oil", "refined soybean oil",
    "brominated vegetable oil", "bvo",  # RFK specifically targets this
}

# Oils generally considered acceptable under "real food" guidelines
ACCEPTABLE_FATS = {
    "olive oil", "extra virgin olive oil", "avocado oil",
    "coconut oil", "butter", "ghee", "lard", "tallow", "duck fat",
    "palm oil",  # controversial but not industrial-extracted
}

ARTIFICIAL_PRESERVATIVES = {
    # BHA/BHT family (antioxidants)
    "bha", "butylated hydroxyanisole", "bht", "butylated hydroxytoluene",
    "tbhq", "tertiary butylhydroquinone", "propyl gallate",

    # Benzoates
    "sodium benzoate", "potassium benzoate", "benzoic acid",
    "benzyl benzoate",

    # Sorbates
    "potassium sorbate", "sodium sorbate", "sorbic acid",
    "calcium sorbate",

    # Sulfites (allergen)
    "sodium sulfite", "sodium bisulfite", "sodium metabisulfite",
    "potassium bisulfite", "sulfur dioxide", "sulfites",
    "potassium metabisulfite",

    # Nitrates/Nitrites (processed meats)
    "sodium nitrate", "sodium nitrite", "potassium nitrate",
    "potassium nitrite", "celery powder",  # Hidden nitrate source

    # Propionates
    "calcium propionate", "sodium propionate", "propionic acid",

    # EDTA family
    "edta", "disodium edta", "calcium disodium edta",
    "tetrasodium edta",

    # Parabens
    "methylparaben", "propylparaben", "ethylparaben",

    # Other preservatives
    "sodium erythorbate", "erythorbic acid", "natamycin",
    "nisin", "lysozyme", "hexamine",
}

ARTIFICIAL_FLAVORS = {
    "artificial flavor", "artificial flavors", "artificial flavoring",
    "artificially flavored", "natural and artificial flavors",
    "flavor enhancer", "msg", "monosodium glutamate",
    "disodium inosinate", "disodium guanylate", "autolyzed yeast extract",
}

ARTIFICIAL_COLORS = {
    # FD&C Red dyes
    "red 40", "red no. 40", "allura red", "fd&c red 40", "e129",
    "red 3", "erythrosine", "fd&c red 3", "e127",
    "red 2", "amaranth", "e123",

    # FD&C Yellow dyes
    "yellow 5", "tartrazine", "fd&c yellow 5", "e102",
    "yellow 6", "sunset yellow", "fd&c yellow 6", "e110",

    # FD&C Blue dyes
    "blue 1", "brilliant blue", "fd&c blue 1", "e133",
    "blue 2", "indigo carmine", "fd&c blue 2", "e132",

    # FD&C Green dyes
    "green 3", "fast green", "fd&c green 3", "e143",

    # Caramel color (often industrially produced with ammonia)
    "caramel color", "caramel coloring", "e150", "e150a", "e150b",
    "e150c", "e150d", "class iv caramel",

    # Titanium dioxide (whitening, banned in EU)
    "titanium dioxide", "e171",

    # Other synthetic colors
    "citrus red 2", "orange b", "carbon black",

    # Generic terms
    "artificial color", "artificial colors", "color added",
    "certified color", "dye", "synthetic color", "fd&c colors",
    "lake", "aluminum lake",  # Lake = insoluble dye
}

REFINED_GRAINS = {
    "enriched flour", "enriched wheat flour", "bleached flour",
    "bleached wheat flour", "white flour", "all-purpose flour",
    "enriched bleached flour", "semolina", "durum flour",
    "white rice", "white rice flour", "corn starch", "modified corn starch",
    "modified food starch", "modified starch",
}

# ============================================================
# WHOLE FOODS (recognizable, encouraged)
# ============================================================

WHOLE_FOODS = {
    # Proteins - Meat
    "chicken", "beef", "pork", "lamb", "turkey", "duck", "venison",
    "bison", "veal", "goat", "rabbit", "chicken breast", "ground beef",
    "steak", "bacon", "ham", "sausage",

    # Proteins - Seafood
    "fish", "salmon", "tuna", "cod", "halibut", "tilapia", "trout",
    "sardines", "anchovies", "mackerel", "shrimp", "prawns", "crab",
    "lobster", "scallops", "mussels", "clams", "oysters", "squid",

    # Proteins - Eggs
    "eggs", "egg", "egg whites", "egg yolks", "whole eggs",

    # Dairy
    "milk", "whole milk", "cream", "heavy cream", "half and half",
    "butter", "cheese", "cheddar", "mozzarella", "parmesan", "feta",
    "yogurt", "greek yogurt", "cottage cheese", "sour cream",
    "cream cheese", "ricotta", "gouda", "swiss cheese", "brie",
    "whey", "buttermilk", "kefir",

    # Vegetables
    "tomato", "tomatoes", "onion", "onions", "garlic", "carrot", "carrots",
    "celery", "bell pepper", "peppers", "broccoli", "spinach", "kale",
    "lettuce", "cabbage", "zucchini", "squash", "potato", "potatoes",
    "sweet potato", "mushrooms", "mushroom", "corn", "peas", "beans",
    "green beans", "cucumber", "cauliflower", "asparagus", "eggplant",
    "artichoke", "beets", "brussels sprouts", "bok choy", "arugula",
    "radish", "turnip", "parsnip", "leek", "shallot", "scallion",
    "green onion", "jalapeno", "serrano", "poblano", "habanero",

    # Fruits
    "apple", "apples", "banana", "bananas", "orange", "oranges",
    "lemon", "lemons", "lime", "limes", "berries", "strawberries",
    "blueberries", "raspberries", "blackberries", "cranberries",
    "grapes", "mango", "pineapple", "papaya", "guava", "passion fruit",
    "peach", "peaches", "pear", "pears", "watermelon", "avocado",
    "cantaloupe", "honeydew", "kiwi", "pomegranate", "fig", "dates",
    "plum", "apricot", "cherry", "cherries", "grapefruit", "tangerine",
    "clementine", "coconut", "raisins", "prunes",

    # Whole grains
    "whole wheat", "whole grain", "oats", "rolled oats", "steel cut oats",
    "brown rice", "wild rice", "quinoa", "barley", "buckwheat", "millet",
    "whole wheat flour", "oat flour", "farro", "spelt", "amaranth",
    "teff", "sorghum", "rye", "whole rye",

    # Nuts and seeds
    "almonds", "walnuts", "pecans", "cashews", "peanuts", "pistachios",
    "macadamia", "hazelnuts", "brazil nuts", "pine nuts",
    "sunflower seeds", "pumpkin seeds", "chia seeds", "flax seeds",
    "flaxseed", "sesame seeds", "hemp seeds", "poppy seeds",

    # Legumes
    "black beans", "kidney beans", "chickpeas", "garbanzo beans",
    "lentils", "pinto beans", "navy beans", "cannellini beans",
    "lima beans", "edamame", "split peas", "black eyed peas",

    # Herbs (fresh and dried)
    "basil", "oregano", "thyme", "rosemary", "sage", "mint", "parsley",
    "cilantro", "dill", "chives", "tarragon", "marjoram", "bay leaf",
    "bay leaves", "lemongrass", "chervil",

    # Spices
    "salt", "sea salt", "kosher salt", "pepper", "black pepper",
    "white pepper", "cumin", "paprika", "smoked paprika", "cinnamon",
    "turmeric", "ginger", "nutmeg", "cloves", "allspice", "cardamom",
    "coriander", "fennel", "anise", "star anise", "mustard seed",
    "cayenne", "chili powder", "curry powder", "garam masala",
    "saffron", "vanilla", "vanilla extract", "vanilla bean",

    # Simple condiments/ingredients
    "water", "olive oil", "extra virgin olive oil", "avocado oil",
    "coconut oil", "vinegar", "apple cider vinegar", "balsamic vinegar",
    "red wine vinegar", "white wine vinegar", "rice vinegar",
    "lemon juice", "lime juice", "tomato paste", "mustard",
    "dijon mustard", "tamari", "coconut aminos", "fish sauce",

    # Cocoa/chocolate (unsweetened)
    "cocoa", "cocoa powder", "cacao", "cacao nibs", "unsweetened chocolate",
}

# ============================================================
# ADDITIONAL FLAGGED CATEGORIES
# ============================================================

ARTIFICIAL_SWEETENERS = {
    # Common artificial sweeteners
    "aspartame", "sucralose", "saccharin", "acesulfame potassium",
    "acesulfame k", "ace-k", "neotame", "advantame",

    # Sugar alcohols (less problematic but still processed)
    "erythritol", "xylitol", "sorbitol", "mannitol", "maltitol",
    "isomalt", "lactitol", "hydrogenated starch hydrolysate",

    # Branded names
    "splenda", "equal", "sweet'n low", "nutrasweet",

    # Stevia extracts (debatable - highly processed form)
    "stevia extract", "reb a", "rebaudioside",
}

EMULSIFIERS_STABILIZERS = {
    # Common emulsifiers (may affect gut microbiome)
    "soy lecithin", "lecithin", "sunflower lecithin",
    "mono and diglycerides", "monoglycerides", "diglycerides",
    "polysorbate 60", "polysorbate 80", "polysorbate 20",
    "sorbitan monostearate", "sodium stearoyl lactylate",
    "datem", "diacetyl tartaric acid ester",

    # Gums and thickeners
    "xanthan gum", "guar gum", "locust bean gum", "carob bean gum",
    "gellan gum", "carrageenan", "agar", "pectin",
    "cellulose gum", "carboxymethyl cellulose", "methylcellulose",

    # Starches
    "modified corn starch", "modified food starch", "modified starch",
    "modified tapioca starch", "resistant starch",
}


def classify_ingredient(name: str) -> dict:
    """
    Classify a single ingredient against our databases.
    Returns classification flags.
    """
    name_lower = name.lower().strip()

    return {
        "name": name,
        "is_added_sugar": any(sugar in name_lower for sugar in ADDED_SUGARS),
        "is_industrial_oil": any(oil in name_lower for oil in INDUSTRIAL_OILS),
        "is_artificial_preservative": any(p in name_lower for p in ARTIFICIAL_PRESERVATIVES),
        "is_artificial_flavor": any(f in name_lower for f in ARTIFICIAL_FLAVORS),
        "is_artificial_color": any(c in name_lower for c in ARTIFICIAL_COLORS),
        "is_refined_grain": any(g in name_lower for g in REFINED_GRAINS),
        "is_whole_food": any(wf in name_lower for wf in WHOLE_FOODS),
        "is_acceptable_fat": any(f in name_lower for f in ACCEPTABLE_FATS),
        "is_artificial_sweetener": any(s in name_lower for s in ARTIFICIAL_SWEETENERS),
        "is_emulsifier": any(e in name_lower for e in EMULSIFIERS_STABILIZERS),
    }


def parse_ingredient_list(ingredient_string: str) -> list[dict]:
    """
    Parse a comma-separated ingredient list and classify each.
    Handles common formats like "ingredient (sub-ingredient, sub-ingredient)"
    """
    import re

    # Remove parenthetical sub-ingredients for now (simplification)
    cleaned = re.sub(r'\([^)]*\)', '', ingredient_string)

    # Split by comma
    ingredients = [i.strip() for i in cleaned.split(',') if i.strip()]

    return [classify_ingredient(ing) for ing in ingredients]
