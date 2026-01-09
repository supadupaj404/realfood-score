# Real Food Score

Quantitative scoring algorithm based on realfood.gov 2025 Dietary Guidelines, calibrated to RFK Jr.'s MAHA priorities.

## Quick Start

```bash
cd /Users/jeremystevenson/CodeProjects/Experiments/realfood-score

# Open the web UI
open index.html

# Run Python tests
python test_products.py

# Score a product via CLI
python -c "from scoring import score; print(score('Test', 'chicken, rice, olive oil'))"

# Look up a barcode
python barcode.py 049000006346
```

## Architecture

```
├── index.html       # Web UI with barcode lookup (Open Food Facts API)
├── scoring.py       # Three-tier scoring algorithm (RFK/Guideline/Practical)
├── ingredients.py   # 558 classified ingredients database
├── barcode.py       # Barcode/UPC lookup via Open Food Facts
├── models.py        # Data models
├── test_products.py # Test suite with 15 real products
└── api.py           # Simple HTTP API server
```

## Three-Tier Scoring System

| Tier | Label | Philosophy |
|------|-------|------------|
| **RFK** | MAHA Score | Based on RFK Jr.'s stated priorities: Dyes > Oils > Preservatives |
| **Guideline** | Official Standard | Strict interpretation of realfood.gov text |
| **Practical** | Better Choice | Consumer-friendly "better than alternatives" framing |

## Scoring Formula

```
Total Score = (
    ingredient_count_score × 0.25 +    # Fewer = better
    flagged_ingredients_score × 0.50 + # Penalties for bad stuff
    whole_food_ratio × 0.25            # Reward recognizable foods
)
```

## Ingredient Database (558 items)

| Category | Count | Examples |
|----------|-------|----------|
| Added Sugars | 67 | HFCS, dextrose, maltodextrin |
| Industrial Oils | 33 | Soybean, canola, BVO |
| Preservatives | 43 | BHA, sodium benzoate, nitrites |
| Artificial Colors | 54 | Red 40, Yellow 5, caramel color |
| Artificial Sweeteners | 23 | Aspartame, sucralose |
| Emulsifiers | 29 | Polysorbate 80, carrageenan |
| Whole Foods | 273 | Meats, vegetables, nuts, spices |

## RFK Priority Calibration

Based on his public statements and actions:
- **Dyes**: -35 points (held CEO meetings demanding removal)
- **Seed Oils**: -30 points (calls them "most harmful")
- **Preservatives**: -18 points (GRAS reform push)
- **Sugar**: -20 points (mentioned but not signature issue)

Sources:
- food-safety.com/articles/10227 (dye CEO meetings)
- hhs.gov/press-room/revising-gras-pathway (GRAS reform)

## API Usage

```bash
# Start server
python api.py

# Score a product
curl "localhost:8000/score?name=Test&ingredients=eggs,butter,salt"
```

## Barcode Lookup

```python
from barcode import score_barcode

result = score_barcode("049000006346")  # Coca-Cola
print(result['scores']['rfk'])  # MAHA score
```

## Next Steps

- [ ] Mobile app with camera barcode scanning
- [ ] Browser extension for grocery sites
- [ ] Restaurant menu integration
- [ ] USDA FoodData Central integration for nutrition data
- [ ] Historical tracking ("your diet score over time")
