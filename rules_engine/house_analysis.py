# AstroAgent/rules_engine/house_analysis.py

import json
from pathlib import Path

class HouseAnalysis:
    def __init__(self, data_path="data/house_rules"):
        self.data_path = Path(data_path)
        self.house_meanings = self.load_json("houses_meanings.json")
        self.career_rules = self.load_json("career_rules.json")
        self.marriage_rules = self.load_json("marriage_rules.json")
        self.wealth_rules = self.load_json("wealth_rules.json")
        self.spirituality_rules = self.load_json("spirituality_rules.json")

    def load_json(self, filename):
        file_path = self.data_path / filename
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_house_meaning(self, house_number):
        return self.house_meanings.get(str(house_number), "No meaning found")

    def analyze_house(self, house_number, planets_in_house):
        """
        Analyze house with planets present.
        Returns a dict with analysis for career, marriage, wealth, spirituality
        """
        house_number = str(house_number)
        analysis = {}

        # Generic house meaning
        analysis["meaning"] = self.get_house_meaning(house_number)

        # Check positive and negative influence
        analysis["career"] = self.check_planet_effect(house_number, planets_in_house, self.career_rules)
        analysis["marriage"] = self.check_planet_effect(house_number, planets_in_house, self.marriage_rules)
        analysis["wealth"] = self.check_planet_effect(house_number, planets_in_house, self.wealth_rules)
        analysis["spirituality"] = self.check_planet_effect(house_number, planets_in_house, self.spirituality_rules)

        return analysis

    def check_planet_effect(self, house_number, planets_in_house, rules):
        """
        Returns a string describing positive/negative effects based on rules
        """
        if house_number not in rules:
            return "No specific rules"

        pos = [p for p in planets_in_house if p in rules[house_number].get("planets_positive", [])]
        neg = [p for p in planets_in_house if p in rules[house_number].get("planets_negative", [])]

        result = ""
        if pos:
            result += f"Positive influence: {', '.join(pos)}. "
        if neg:
            result += f"Negative influence: {', '.join(neg)}."

        return result.strip() if result else "No significant planetary influence"
