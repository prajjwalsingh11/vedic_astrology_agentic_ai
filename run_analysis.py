# run_analysis.py

from rules_engine.analysis import AstrologyAnalysis
from datetime import datetime
from pprint import pprint

try:
    import swisseph as swe
except ImportError:
    swe = None
    print("pyswisseph not installed. Planetary positions will use demo values.")

try:
    from geopy.geocoders import Nominatim
except ImportError:
    Nominatim = None
    print("geopy not installed. Latitude/Longitude will use demo values.")


def get_lat_lon(city_name):
    if Nominatim is None or not city_name.strip():
        return 0.0, 0.0
    geolocator = Nominatim(user_agent="astroagent")
    location = geolocator.geocode(city_name)
    if location:
        return location.latitude, location.longitude
    else:
        print(f"Could not find city '{city_name}', using demo coordinates.")
        return 0.0, 0.0


def compute_planet_positions(birth_datetime, latitude=0.0, longitude=0.0):
    """
    Return a tuple: (planets_in_houses_dict, planets_with_signs_dict)
    Uses Swiss Ephemeris if available, else returns demo values.
    """
    planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
    planets_in_houses = {}
    planets_with_signs = {}

    if swe is None:
        # Demo values
        planets_in_houses = {
            "1st House": ["Sun", "Mercury", "Venus"],
            "3rd House": ["Moon", "Mars"],
            "7th House": ["Jupiter"],
            "8th House": ["Ketu"]
        }
        planets_with_signs = {
            "Sun": "Gemini",
            "Moon": "Virgo",
            "Mars": "Virgo",
            "Mercury": "Cancer",
            "Jupiter": "Capricorn",
            "Venus": "Cancer",
            "Saturn": "Pisces",
            "Rahu": "Leo",
            "Ketu": "Aquarius"
        }
        return planets_in_houses, planets_with_signs

    # Compute Julian Day
    jd_ut = swe.julday(
        birth_datetime.year,
        birth_datetime.month,
        birth_datetime.day,
        birth_datetime.hour + birth_datetime.minute / 60.0
    )

    # Get positions for each planet
    for planet in planets:
        if planet == "Rahu":
            planet_id = swe.MEAN_NODE
        elif planet == "Ketu":
            planet_id = swe.MEAN_NODE
        else:
            planet_id = getattr(swe, planet.upper())

        lon = swe.calc_ut(jd_ut, planet_id)[0][0] % 360
        sign_index = int(lon // 30)
        sign_name = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo",
                     "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"][sign_index]

        planets_with_signs[planet] = sign_name

        # Compute house
        if latitude is not None and longitude is not None:
            # Using Placidus, can expand later
            cusps, ascmc = swe.houses(jd_ut, latitude, longitude)
            house_num = 1
            for i, cusp in enumerate(cusps, 1):
                if lon < cusp:
                    house_num = i
                    break
            house_name = f"{house_num}th House"
        else:
            house_name = "1st House"

        planets_in_houses.setdefault(house_name, []).append(planet)

    return planets_in_houses, planets_with_signs


if __name__ == "__main__":
    # Get user input
    birth_date_input = input("Enter your birth date (YYYY-MM-DD): ")
    birth_time_input = input("Enter birth time (HH:MM) 24h format: ")
    birth_city = input("Enter your birth city: ")

    hour, minute = map(int, birth_time_input.split(":"))
    year, month, day = map(int, birth_date_input.split("-"))
    birth_datetime = datetime(year, month, day, hour, minute)

    latitude, longitude = get_lat_lon(birth_city)

    planets_in_houses, planets_with_signs = compute_planet_positions(birth_datetime, latitude, longitude)

    # Initialize analysis
    astro = AstrologyAnalysis(
        data_path="data",
        birth_date=birth_datetime,
        birth_city=birth_city
    )

    # Run full analysis
    report = astro.full_analysis(planets_in_houses, planets_with_signs)

    # Print
    print("\n========== ASTROLOGY REPORT ==========\n")
    pprint(report)
    print("\n======================================\n")
