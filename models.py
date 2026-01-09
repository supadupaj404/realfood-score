"""
Data models for the Real Food Score algorithm.

Based on criteria from realfood.gov (2025 Dietary Guidelines)
"""

from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class ProcessingLevel(Enum):
    """NOVA-inspired processing classification"""
    UNPROCESSED = 1          # Fresh fruits, vegetables, eggs, raw meat
    MINIMALLY_PROCESSED = 2  # Frozen veg, dried beans, plain yogurt
    PROCESSED = 3            # Canned vegetables, cheese, cured meats
    ULTRA_PROCESSED = 4      # Industrial formulations with additives


@dataclass
class Ingredient:
    """Single ingredient with classification metadata"""
    name: str
    is_added_sugar: bool = False
    is_industrial_oil: bool = False
    is_artificial_flavor: bool = False
    is_artificial_preservative: bool = False
    is_artificial_color: bool = False
    is_refined_grain: bool = False
    is_whole_food: bool = False  # Recognizable as food


@dataclass
class FoodProduct:
    """A food product to be scored"""
    name: str
    ingredients: list[Ingredient] = field(default_factory=list)
    brand: Optional[str] = None
    category: Optional[str] = None

    @property
    def ingredient_count(self) -> int:
        return len(self.ingredients)

    @property
    def flagged_ingredient_count(self) -> int:
        """Count ingredients that violate real food principles"""
        return sum(1 for i in self.ingredients if (
            i.is_added_sugar or
            i.is_industrial_oil or
            i.is_artificial_flavor or
            i.is_artificial_preservative or
            i.is_artificial_color
        ))

    @property
    def whole_food_ratio(self) -> float:
        """Percentage of ingredients that are recognizable whole foods"""
        if not self.ingredients:
            return 0.0
        whole_count = sum(1 for i in self.ingredients if i.is_whole_food)
        return whole_count / len(self.ingredients)


@dataclass
class ScoreResult:
    """The output of the scoring algorithm"""
    product_name: str
    total_score: float           # 0-100, higher is better
    grade: str                   # A, B, C, D, F

    # Component scores (0-100 each)
    ingredient_count_score: float
    flagged_ingredients_score: float
    whole_food_score: float

    # Flags for display
    flags: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "product": self.product_name,
            "score": round(self.total_score, 1),
            "grade": self.grade,
            "breakdown": {
                "ingredient_simplicity": round(self.ingredient_count_score, 1),
                "clean_ingredients": round(self.flagged_ingredients_score, 1),
                "whole_food_ratio": round(self.whole_food_score, 1),
            },
            "flags": self.flags,
            "recommendations": self.recommendations
        }
