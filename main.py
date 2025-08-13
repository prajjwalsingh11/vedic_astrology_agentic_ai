# AstroAgent/main.py

from rules_engine.analysis import AstrologyAnalysis
import pprint

def main():
    # Example input placeholders (any user can fill this)
    planets_in_houses = {}  # {house_number: [planet1, planet2,...]}
    planets_in_signs = {}   # {planet: sign_number 1-12}
    birth_details = {}      # {'date': 'YYYY-MM-DD', 'time': 'HH:MM', 'latitude': float, 'longitude': float}

    # Ask user to fill input dynamically or via file
    print("Please provide planetary positions in houses (e.g., 1:Sun,Mercury;2:Moon;...)")
    # planets_in_houses = parse_input_somehow()

    print("Please provide planetary positions in signs (e.g., Sun:10,Moon:3,...)")
    # planets_in_signs = parse_input_somehow()

    print("Please provide birth details (date, time, lat, lon)")
    # birth_details = parse_input_somehow()

    # Initialize astrology engine
    astro = AstrologyAnalysis()
    report = astro.full_analysis(planets_in_houses, planets_in_signs, birth_details)

    # Pretty-print the full report
    pprint.pprint(report)

if __name__ == "__main__":
    main()
