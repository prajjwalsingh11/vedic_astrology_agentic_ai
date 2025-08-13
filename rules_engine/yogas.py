# AstroAgent/rules_engine/yogas.py

import json
from pathlib import Path

class Yogas:
    def __init__(self, data_path="data/house_rules"):
        """
        data_path: folder containing yoga rules JSON
        Example files: 'yogas.json'
        """
        self.data_path = Path(data_path)
        self.yoga_rules = self.load_json("yogas.json")

    def load_json(self, filename):
        file_path = self.data_path / filename
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def detect_yogas(self, planets_in_houses):
        """
        Detect yogas based on planets in houses
        planets_in_houses: dict {house_number: [planet1, planet2,...]}
        Returns a list of detected yogas
        """
        detected = []

        for yoga_name, rules in self.yoga_rules.items():
            # Each yoga rule contains a list of conditions
            conditions = rules.get("conditions", [])

            for condition in conditions:
                if self.check_condition(condition, planets_in_houses):
                    detected.append(yoga_name)
                    break  # Yoga detected, no need to check other conditions

        return detected

    def check_condition(self, condition, planets_in_houses):
        """
        Check if a single yoga condition is satisfied
        Example condition: {"house": 1, "planets": ["Mars", "Sun"]}
        Can be extended for multiple types of rules (e.g., lord combinations, aspects)
        """
        house = str(condition.get("house"))
        required_planets = condition.get("planets", [])

        planets_here = planets_in_houses.get(int(house), [])

        # Check if all required planets are present in the house
        if all(p in planets_here for p in required_planets):
            return True
        return False
