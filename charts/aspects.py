# AstroAgent/rules_engine/aspects.py

from config import PLANETS, SIGNS

# Vedic aspects: 1-7th, 5th, 9th, etc. For simplicity, we'll start with classical aspects
VEDIC_ASPECTS = {
    "Sun": [7],       # Full aspect: 7th house from planet
    "Moon": [7],
    "Mars": [4, 7, 8], # 4th, 7th, 8th aspects
    "Mercury": [7],
    "Jupiter": [5, 7, 9], # 5th, 7th, 9th aspects
    "Venus": [7],
    "Saturn": [3, 7, 10], # 3rd, 7th, 10th aspects
    "Rahu": [7],
    "Ketu": [7]
}


class Aspects:
    def __init__(self, planet_positions):
        """
        planet_positions: dictionary of planet → {"sign": 0-11, "degree": float, "house": int}
        """
        self.planet_positions = planet_positions
        self.aspect_table = {}  # planet → list of planets it aspects

    def compute_aspects(self):
        self.aspect_table = {planet: [] for planet in PLANETS}

        for p1 in PLANETS:
            sign1 = self.planet_positions[p1]["sign"]
            for p2 in PLANETS:
                if p1 == p2:
                    continue
                sign2 = self.planet_positions[p2]["sign"]
                distance = (sign2 - sign1) % 12
                for aspect in VEDIC_ASPECTS.get(p1, []):
                    if distance == (aspect % 12):
                        self.aspect_table[p1].append(p2)

        return self.aspect_table

    def print_aspects(self):
        if not self.aspect_table:
            self.compute_aspects()
        print("=== Planetary Aspects ===")
        for planet, aspects in self.aspect_table.items():
            print(f"{planet} aspects: {', '.join(aspects) if aspects else 'None'}")
