from datetime import datetime, timedelta

# Vimshottari Dasha years
VIMSHOTTARI_DASHA_YEARS = {
    "Ketu": 7,
    "Venus": 20,
    "Sun": 6,
    "Moon": 10,
    "Mars": 7,
    "Rahu": 18,
    "Jupiter": 16,
    "Saturn": 19,
    "Mercury": 17
}

# Vimshottari Dasha sequence
DASHA_SEQUENCE = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]

class Dashas:
    """
    Calculate Vimshottari Dasha periods based on Moon Nakshatra at birth
    """
    def __init__(self, birth_date: datetime, moon_nakshatra_index: int = 12):
        self.birth_date = birth_date
        self.moon_nakshatra_index = moon_nakshatra_index  # 0-26 (27 Nakshatras)
        self.dasha_planets = []
        self.dasha_start_dates = []

    def calculate_dashas(self):
        """
        Compute Dasha start and end dates for the sequence
        """
        # Starting planet based on Moon Nakshatra
        starting_index = self.moon_nakshatra_index % 9
        self.dasha_planets = DASHA_SEQUENCE[starting_index:] + DASHA_SEQUENCE[:starting_index]

        current_date = self.birth_date
        self.dasha_start_dates = []

        for planet in self.dasha_planets:
            years = VIMSHOTTARI_DASHA_YEARS[planet]
            start_date = current_date
            end_date = start_date + timedelta(days=int(years * 365.25))
            self.dasha_start_dates.append((planet, start_date, end_date))
            current_date = end_date

        return self.dasha_start_dates

    def get_current_dasha(self, on_date: datetime = None):
        if on_date is None:
            on_date = datetime.now()

        if not self.dasha_start_dates:
            self.calculate_dashas()

        for planet, start, end in self.dasha_start_dates:
            if start <= on_date <= end:
                return {
                    "current_mahadasha": planet,
                    "start_date": start.date(),
                    "end_date": end.date()
                }

        return {
            "current_mahadasha": None,
            "start_date": None,
            "end_date": None
        }

    def print_dashas(self):
        if not self.dasha_start_dates:
            self.calculate_dashas()
        print("=== Vimshottari Dashas ===")
        for planet, start, end in self.dasha_start_dates:
            print(f"{planet}: {start.date()} → {end.date()}")
