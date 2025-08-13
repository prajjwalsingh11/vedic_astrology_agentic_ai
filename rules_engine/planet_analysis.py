# AstroAgent/rules_engine/planet_analysis.py

import json
from pathlib import Path

class PlanetAnalysis:
    def __init__(self, data_path="data/planetary_rules"):
        self.data_path = Path(data_path)
        self.planet_strength = self.load_json("planet_strength.json")
        self.planet_meanings = self.load_json("planet_meanings.json")
        self.aspect_rules = self.load_json("aspects_rules.json")

    def load_json(self, filename):
        file_path = self.data_path / filename
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_planet_meaning(self, planet):
        return self.planet_meanings.get(planet, "No meaning found")

    def get_planet_strength(self, planet, sign=None):
        """
        Returns dict with exalted, debilitated, own_sign
        Optional: check if planet is strong in given sign
        """
        strength = self.planet_strength.get(planet, {})
        if sign is not None:
            if sign == strength.get("exalted"):
                return f"{planet} is exalted in this sign"
            elif sign == strength.get("debilitated"):
                return f"{planet} is debilitated in this sign"
            elif sign in strength.get("own_sign", []):
                return f"{planet} is in its own sign"
            else:
                return f"{planet} is neutral in this sign"
        return strength

    def get_aspect_influence(self, planet, other_planet):
        """
        Check aspect influence rules
        """
        rules = self.aspect_rules.get(planet, {})
        for aspect_type, planets_list in rules.items():
            if other_planet in planets_list:
                return f"{planet} has {aspect_type} aspect on {other_planet}"
        return f"No significant aspect of {planet} on {other_planet}"
