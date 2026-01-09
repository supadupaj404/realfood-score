"""
Real Food Score Algorithm

Scoring system based on realfood.gov 2025 Dietary Guidelines.
Converts qualitative "real food" principles into quantitative scores.

DUAL SCORING SYSTEM:
- Guideline Score: Strict, matches realfood.gov literally
- Practical Score: Consumer-friendly, acknowledges "better choices"

Score Range: 0-100 (higher = more aligned with real food guidelines)
Grade Scale: A (90+), B (80-89), C (70-79), D (60-69), F (<60)
"""

from dataclasses import dataclass
from enum import Enum
from ingredients import parse_ingredient_list, ACCEPTABLE_FATS


class ScoringMode(Enum):
    GUIDELINE = "guideline"  # Strict: what the government says
    PRACTICAL = "practical"  # Lenient: real-world "better choices"


@dataclass
class ScoreWeights:
    """
    Configurable weights for score components.
    Adjust these to tune the algorithm's priorities.
    """
    ingredient_count: float = 0.25      # 25% - simpler is better
    flagged_ingredients: float = 0.50   # 50% - biggest penalty for bad stuff
    whole_food_ratio: float = 0.25      # 25% - reward recognizable foods


# ============================================================
# PENALTY CONFIGURATION - This is where business logic lives
# ============================================================

@dataclass
class PenaltyConfig:
    """
    Penalty values for flagged ingredients.
    GUIDELINE mode uses strict penalties.
    PRACTICAL mode uses these reduced values.
    """
    # First occurrence penalties
    added_sugar_first: int = 25
    added_sugar_additional: int = 5
    industrial_oil_first: int = 20
    industrial_oil_additional: int = 5
    preservative_first: int = 15
    preservative_additional: int = 5
    artificial_flavor: int = 15
    artificial_color_first: int = 15
    artificial_color_additional: int = 3
    refined_grain: int = 10


# ============================================================
# THREE SCORING TIERS
# ============================================================

# GUIDELINE: Strict interpretation of realfood.gov text
GUIDELINE_PENALTIES = PenaltyConfig()

# RFK: Calibrated to RFK Jr.'s stated priorities
# - Dyes are his #1 target (CEO meetings, state bans)
# - Seed oils are personal crusade ("most harmful")
# - Sugars mentioned but not signature issue
# Sources:
#   - food-safety.com/articles/10227 (dye CEO meetings)
#   - hhs.gov/press-room/revising-gras-pathway (GRAS reform)
#   - axios.com/2026/01/07/rfk-kennedy-food-nutrition-guidelines-milk
RFK_PENALTIES = PenaltyConfig(
    added_sugar_first=20,            # High but not his top priority
    added_sugar_additional=4,
    industrial_oil_first=30,         # VERY HIGH - his personal crusade
    industrial_oil_additional=8,     # Each additional oil hits hard
    preservative_first=18,           # High - part of GRAS reform push
    preservative_additional=5,
    artificial_flavor=20,            # High - "artificial" is a trigger word
    artificial_color_first=35,       # HIGHEST - his #1 actionable target
    artificial_color_additional=8,   # Multiple dyes = disaster score
    refined_grain=8,                 # Lower priority for him
)

# PRACTICAL: Consumer-friendly "better choice" framing
PRACTICAL_PENALTIES = PenaltyConfig(
    added_sugar_first=12,            # Reduced: acknowledge "less bad" sugars
    added_sugar_additional=3,
    industrial_oil_first=10,         # Reduced: common in "healthy" products
    industrial_oil_additional=3,
    preservative_first=8,            # Reduced: some preservation is practical
    preservative_additional=3,
    artificial_flavor=10,
    artificial_color_first=15,       # Still notable but not crushing
    artificial_color_additional=3,
    refined_grain=5,                 # Reduced: alternatives not always available
)


class RealFoodScorer:
    """
    Scores food products against real food guidelines.
    Supports dual scoring: GUIDELINE (strict) and PRACTICAL (lenient).
    """

    def __init__(self, weights: ScoreWeights = None):
        self.weights = weights or ScoreWeights()

    def score_ingredient_count(self, count: int) -> float:
        """
        Score based on number of ingredients.
        Fewer ingredients = higher score.

        Thresholds (based on "few ingredients" guidance):
        - 1-5 ingredients: 100 (excellent)
        - 6-10 ingredients: 80-95 (good)
        - 11-15 ingredients: 60-75 (moderate)
        - 16-20 ingredients: 40-55 (concerning)
        - 21+ ingredients: 0-35 (ultra-processed territory)
        """
        if count <= 5:
            return 100
        elif count <= 10:
            return 100 - (count - 5) * 4  # 96, 92, 88, 84, 80
        elif count <= 15:
            return 80 - (count - 10) * 4  # 76, 72, 68, 64, 60
        elif count <= 20:
            return 60 - (count - 15) * 4  # 56, 52, 48, 44, 40
        else:
            return max(0, 40 - (count - 20) * 2)

    def score_flagged_ingredients(
        self,
        ingredients: list[dict],
        penalties_config: PenaltyConfig = None
    ) -> tuple[float, list[str]]:
        """
        Score based on presence of flagged ingredients.
        Each flag category reduces score based on penalty config.

        Returns (score, list_of_flags)
        """
        if not ingredients:
            return 100, []

        p = penalties_config or GUIDELINE_PENALTIES
        flags = []
        penalties = 0

        # Count violations by category
        added_sugars = sum(1 for i in ingredients if i.get("is_added_sugar"))
        industrial_oils = sum(1 for i in ingredients if i.get("is_industrial_oil"))
        artificial_preservatives = sum(1 for i in ingredients if i.get("is_artificial_preservative"))
        artificial_flavors = sum(1 for i in ingredients if i.get("is_artificial_flavor"))
        artificial_colors = sum(1 for i in ingredients if i.get("is_artificial_color"))
        refined_grains = sum(1 for i in ingredients if i.get("is_refined_grain"))

        # Apply penalties (cumulative) using config values
        if added_sugars:
            penalties += p.added_sugar_first + (added_sugars - 1) * p.added_sugar_additional
            flags.append(f"Contains {added_sugars} added sugar(s)")

        if industrial_oils:
            penalties += p.industrial_oil_first + (industrial_oils - 1) * p.industrial_oil_additional
            flags.append(f"Contains {industrial_oils} industrial oil(s)")

        if artificial_preservatives:
            penalties += p.preservative_first + (artificial_preservatives - 1) * p.preservative_additional
            flags.append(f"Contains {artificial_preservatives} artificial preservative(s)")

        if artificial_flavors:
            penalties += p.artificial_flavor
            flags.append("Contains artificial flavors")

        if artificial_colors:
            penalties += p.artificial_color_first + (artificial_colors - 1) * p.artificial_color_additional
            flags.append(f"Contains {artificial_colors} artificial color(s)")

        if refined_grains:
            penalties += p.refined_grain
            flags.append("Contains refined grains")

        return max(0, 100 - penalties), flags

    def score_whole_food_ratio(self, ingredients: list[dict]) -> float:
        """
        Score based on percentage of recognizable whole food ingredients.
        Higher ratio of whole foods = higher score.
        """
        if not ingredients:
            return 0

        # Count whole foods (also count acceptable fats as positive)
        whole_count = sum(
            1 for i in ingredients
            if i.get("is_whole_food") or i.get("is_acceptable_fat")
        )

        ratio = whole_count / len(ingredients)
        return ratio * 100

    def calculate_grade(self, score: float) -> str:
        """Convert numeric score to letter grade."""
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"

    def generate_recommendations(self, flags: list[str], grade: str) -> list[str]:
        """Generate actionable recommendations based on flags."""
        recommendations = []

        if any("added sugar" in f.lower() for f in flags):
            recommendations.append("Look for unsweetened alternatives")

        if any("industrial oil" in f.lower() for f in flags):
            recommendations.append("Choose products with olive oil, butter, or avocado oil")

        if any("artificial" in f.lower() for f in flags):
            recommendations.append("Seek products with simple, recognizable ingredients")

        if any("refined grain" in f.lower() for f in flags):
            recommendations.append("Choose whole grain versions when available")

        if grade in ["D", "F"]:
            recommendations.append("Consider whole food alternatives to this product")

        return recommendations

    def _calculate_score(
        self,
        ingredients: list[dict],
        penalties_config: PenaltyConfig
    ) -> tuple[float, float, float, float, list[str]]:
        """Calculate scores with given penalty config."""
        count_score = self.score_ingredient_count(len(ingredients))
        flagged_score, flags = self.score_flagged_ingredients(ingredients, penalties_config)
        whole_food_score = self.score_whole_food_ratio(ingredients)

        total_score = (
            count_score * self.weights.ingredient_count +
            flagged_score * self.weights.flagged_ingredients +
            whole_food_score * self.weights.whole_food_ratio
        )

        return total_score, count_score, flagged_score, whole_food_score, flags

    def score_product(self, product_name: str, ingredient_string: str) -> dict:
        """
        Main scoring method - returns THREE SCORE TIERS.

        Args:
            product_name: Name of the product
            ingredient_string: Comma-separated ingredient list

        Returns:
            Dictionary with guideline, RFK, and practical scores
        """
        # Parse and classify ingredients
        ingredients = parse_ingredient_list(ingredient_string)

        # Calculate GUIDELINE score (strict textual interpretation)
        g_total, g_count, g_flagged, g_whole, flags = self._calculate_score(
            ingredients, GUIDELINE_PENALTIES
        )
        g_grade = self.calculate_grade(g_total)

        # Calculate RFK score (his stated priority hierarchy)
        r_total, r_count, r_flagged, r_whole, _ = self._calculate_score(
            ingredients, RFK_PENALTIES
        )
        r_grade = self.calculate_grade(r_total)

        # Calculate PRACTICAL score (lenient consumer framing)
        p_total, p_count, p_flagged, p_whole, _ = self._calculate_score(
            ingredients, PRACTICAL_PENALTIES
        )
        p_grade = self.calculate_grade(p_total)

        recommendations = self.generate_recommendations(flags, g_grade)

        return {
            "product": product_name,
            "ingredient_count": len(ingredients),

            # THREE-TIER SCORING SYSTEM
            "scores": {
                "rfk": {
                    "score": round(r_total, 1),
                    "grade": r_grade,
                    "label": "MAHA Score",
                    "description": "Based on RFK Jr.'s stated priorities (dyes, seed oils, additives)"
                },
                "guideline": {
                    "score": round(g_total, 1),
                    "grade": g_grade,
                    "label": "Official Standard",
                    "description": "Strict alignment with realfood.gov text"
                },
                "practical": {
                    "score": round(p_total, 1),
                    "grade": p_grade,
                    "label": "Better Choice",
                    "description": "Compared to typical alternatives"
                },
            },

            # Legacy fields for compatibility
            "score": round(g_total, 1),
            "grade": g_grade,

            "breakdown": {
                "ingredient_simplicity": round(g_count, 1),
                "clean_ingredients_rfk": round(r_flagged, 1),
                "clean_ingredients_guideline": round(g_flagged, 1),
                "clean_ingredients_practical": round(p_flagged, 1),
                "whole_food_ratio": round(g_whole, 1),
            },
            "flags": flags,
            "recommendations": recommendations,
            "ingredients_analyzed": [
                {
                    "name": i["name"],
                    "whole_food": i.get("is_whole_food", False),
                    "flagged": any([
                        i.get("is_added_sugar"),
                        i.get("is_industrial_oil"),
                        i.get("is_artificial_preservative"),
                        i.get("is_artificial_flavor"),
                        i.get("is_artificial_color"),
                    ])
                }
                for i in ingredients
            ]
        }


# Convenience function
def score(product_name: str, ingredients: str) -> dict:
    """Quick scoring function."""
    scorer = RealFoodScorer()
    return scorer.score_product(product_name, ingredients)


if __name__ == "__main__":
    # Quick test
    result = score(
        "Test Product",
        "whole wheat flour, water, olive oil, salt, yeast"
    )
    print(f"Score: {result['score']} ({result['grade']})")
