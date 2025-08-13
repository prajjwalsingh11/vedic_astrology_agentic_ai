# AstroAgent/rules_engine/analysis.py

from rules_engine.house_analysis import HouseAnalysis
from rules_engine.planet_analysis import PlanetAnalysis
from rules_engine.yogas import Yogas
from rules_engine.dashas import Dashas
from datetime import datetime
from utils.geocode_utils import get_lat_lon  # helper to fetch latitude/longitude from city

class AstrologyAnalysis:
    def __init__(self, data_path="data", birth_date=None, birth_city=None):
        """
        birth_date: datetime object
        birth_city: string for latitude/longitude
        """
        self.birth_date = birth_date or datetime(1997, 7, 11, 7, 2)
        self.birth_city = birth_city or "Varanasi"

        # Get latitude and longitude
        latitude, longitude = get_lat_lon(self.birth_city)

        # Initialize modules
        self.house_analyzer = HouseAnalysis(data_path=f"{data_path}/house_rules")
        self.planet_analyzer = PlanetAnalysis(data_path=f"{data_path}/planetary_rules")
        self.yogas = Yogas(data_path=f"{data_path}/house_rules")

        # Dashas only needs birth_date now (no moon_nakshatra_index required)
        self.dashas = Dashas(birth_date=self.birth_date)

    def analyze_career(self, planets_in_houses):
        return {h: self.house_analyzer.analyze_house(h, p).get("career") for h, p in planets_in_houses.items()}

    def analyze_marriage(self, planets_in_houses):
        return {h: self.house_analyzer.analyze_house(h, p).get("marriage") for h, p in planets_in_houses.items()}

    def analyze_wealth(self, planets_in_houses):
        return {h: self.house_analyzer.analyze_house(h, p).get("wealth") for h, p in planets_in_houses.items()}

    def analyze_spirituality(self, planets_in_houses):
        return {h: self.house_analyzer.analyze_house(h, p).get("spirituality") for h, p in planets_in_houses.items()}

    def analyze_planet_strengths(self, planets_with_signs):
        return {pl: self.planet_analyzer.get_planet_strength(pl, sign) for pl, sign in planets_with_signs.items()}

    def analyze_aspects(self, planets_with_signs):
        aspects_report = []
        planets = list(planets_with_signs.keys())
        for i in range(len(planets)):
            for j in range(i+1, len(planets)):
                influence = self.planet_analyzer.get_aspect_influence(planets[i], planets[j])
                if "No significant" not in influence:
                    aspects_report.append(influence)
        return aspects_report

    def analyze_yogas(self, planets_in_houses):
        return self.yogas.detect_yogas(planets_in_houses)

    def analyze_dashas(self):
        return self.dashas.get_current_dasha()

    def full_analysis(self, planets_in_houses, planets_with_signs):
        return {
            "career": self.analyze_career(planets_in_houses),
            "marriage": self.analyze_marriage(planets_in_houses),
            "wealth": self.analyze_wealth(planets_in_houses),
            "spirituality": self.analyze_spirituality(planets_in_houses),
            "planet_strengths": self.analyze_planet_strengths(planets_with_signs),
            "aspects": self.analyze_aspects(planets_with_signs),
            "yogas": self.analyze_yogas(planets_in_houses),
            "current_dasha": self.analyze_dashas()
        }
