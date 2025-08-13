# AstroAgent/charts/natal_chart.py

from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import const

from config import PLANETS, HOUSES

class NatalChart:
    def __init__(self, birth_date, birth_time, timezone, latitude, longitude):
        """
        birth_date: 'YYYY-MM-DD'
        birth_time: 'HH:MM'
        timezone: e.g. '+05:30'
        latitude: float
        longitude: float
        """
        self.birth_date = birth_date
        self.birth_time = birth_time
        self.timezone = timezone
        self.latitude = latitude
        self.longitude = longitude
        self.chart = self._generate_chart()
        self.planet_positions = self._get_planet_positions()
        self.house_positions = self._get_house_positions()

    def _generate_chart(self):
        dt = Datetime(f"{self.birth_date} {self.birth_time}", self.timezone)
        pos = GeoPos(self.latitude, self.longitude)
        chart = Chart(dt, pos)
        return chart

    def _get_planet_positions(self):
        positions = {}
        for planet in PLANETS:
            try:
                p = self.chart.get(planet)
                positions[planet] = {
                    "sign": p.sign,
                    "longitude": float(p.lon),
                    "house": int(p.house)
                }
            except Exception as e:
                positions[planet] = {"error": str(e)}
        return positions

    def _get_house_positions(self):
        houses = {}
        for i in range(1, 13):
            try:
                house = self.chart.get(const.HOUSES[i-1])
                houses[f"{i}th House"] = {
                    "sign": house.sign,
                    "cuspal_degree": float(house.lon)
                }
            except Exception as e:
                houses[f"{i}th House"] = {"error": str(e)}
        return houses

    def print_chart(self):
        print("=== Planet Positions ===")
        for planet, info in self.planet_positions.items():
            print(f"{planet}: Sign={info.get('sign')}, House={info.get('house')}, Longitude={info.get('longitude'):.2f}")
        print("\n=== House Cusps ===")
        for house, info in self.house_positions.items():
            print(f"{house}: Sign={info.get('sign')}, Cuspal Degree={info.get('cuspal_degree'):.2f}")

