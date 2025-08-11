from typing import List, Dict

# Canonical planet names in capitalized form
PLANETS = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]

def normalize_planet_name(name: str) -> str:
    name = name.strip().lower()
    for p in PLANETS:
        if p.lower() == name:
            return p
    raise ValueError(f"Invalid planet name: {name}")

# Exaltation and debilitation signs by planet (Vedic astrology standard)
PLANET_EXALTATION_SIGNS = {
    "Sun": "Aries",
    "Moon": "Taurus",
    "Mars": "Capricorn",
    "Mercury": "Virgo",
    "Jupiter": "Cancer",
    "Venus": "Pisces",
    "Saturn": "Libra",
    "Rahu": "Taurus",  # Sometimes debated but common approach
    "Ketu": "Scorpio",
}

PLANET_DEBILITATION_SIGNS = {
    "Sun": "Libra",
    "Moon": "Scorpio",
    "Mars": "Cancer",
    "Mercury": "Pisces",
    "Jupiter": "Capricorn",
    "Venus": "Virgo",
    "Saturn": "Aries",
    "Rahu": "Scorpio",
    "Ketu": "Taurus",
}

# Planet aspects: dictionary of planet -> list of aspects (in house offsets)
PLANET_ASPECTS = {
    "Mars": [4, 7, 8],      # 4th, 7th, 8th
    "Jupiter": [5, 7, 9],   # 5th, 7th, 9th
    "Saturn": [3, 7, 10],   # 3rd, 7th, 10th
    "Rahu": [5, 7, 9],      # 5th, 7th, 9th
    "Ketu": [5, 7, 9],      # 5th, 7th, 9th
    "Sun": [7],
    "Moon": [7],
    "Mercury": [7],
    "Venus": [7],
}

# Status for planets — for future extension
class PlanetStatus:
    def __init__(self, name: str, exalted_sign: str, debilitated_sign: str):
        self.name = name
        self.exalted_sign = exalted_sign
        self.debilitated_sign = debilitated_sign

def get_aspected_houses(planet: str, current_house: int) -> List[int]:
    """
    Calculate which houses are aspected by the planet given its position (house number 1-12).
    House numbers are 1-based and anticlockwise.
    Returns list of house numbers (1-12).
    """
    if planet not in PLANET_ASPECTS:
        return []
    aspects = PLANET_ASPECTS[planet]
    result = []
    for offset in aspects:
        # anticlockwise houses, so (current_house + offset -1) % 12 + 1
        asp_house = ((current_house + offset - 1) % 12) + 1
        result.append(asp_house)
    return result
