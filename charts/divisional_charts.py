# AstroAgent/charts/divisional_charts.py

from flatlib.chart import Chart
from flatlib import const
from flatlib import ephem
from config import PLANETS, DIVISIONAL_CHARTS

class DivisionalCharts:
    def __init__(self, natal_chart):
        """
        natal_chart: instance of NatalChart
        """
        self.natal_chart = natal_chart
        self.divisional_positions = {}

    def get_divisional_chart(self, division='D9'):
        """
        Compute divisional chart planet positions.
        Supported: D9, D10, D24
        """
        if division not in DIVISIONAL_CHARTS:
            raise ValueError(f"{division} not supported")

        self.divisional_positions[division] = {}

        for planet in PLANETS:
            planet_info = self.natal_chart.planet_positions.get(planet)
            if not planet_info or 'error' in planet_info:
                self.divisional_positions[division][planet] = {"error": "Planet not available"}
                continue

            # Get longitude from natal chart
            lon = planet_info['longitude']

            # Compute divisional longitude
            divisional_lon = self._compute_divisional_longitude(lon, division)
            # Determine sign and degree in divisional chart
            sign_index = int(divisional_lon // 30) % 12
            degree_in_sign = divisional_lon % 30

            self.divisional_positions[division][planet] = {
                "longitude": divisional_lon,
                "sign": sign_index,  # 0-Aries, 1-Taurus, etc.
                "degree": degree_in_sign
            }

        return self.divisional_positions[division]

    def _compute_divisional_longitude(self, lon, division):
        """
        Computes the planet's longitude in the divisional chart.
        Uses classical method: divide each sign into n parts based on division.
        """
        if division == 'D9':
            # Navamsa: 1 sign = 9 parts → each 3°20'
            part_size = 3 + 20/60  # degrees
            divisional_lon = (lon // part_size) * part_size % 360
        elif division == 'D10':
            # Dasamsa: 1 sign = 10 parts → each 3°
            part_size = 3  # degrees
            divisional_lon = (lon // part_size) * part_size % 360
        elif division == 'D24':
            # Siddhamsa: 1 sign = 24 parts → each 1°15'
            part_size = 1 + 15/60
            divisional_lon = (lon // part_size) * part_size % 360
        else:
            divisional_lon = lon  # fallback
        return divisional_lon

    def print_divisional_chart(self, division='D9'):
        chart = self.divisional_positions.get(division)
        if not chart:
            chart = self.get_divisional_chart(division)

        print(f"=== {division} Planet Positions ===")
        for planet, info in chart.items():
            if 'error' in info:
                print(f"{planet}: {info['error']}")
            else:
                print(f"{planet}: Sign={info['sign']}, Degree={info['degree']:.2f}, Longitude={info['longitude']:.2f}")
