# AstroAgent/config.py

# List of planets
PLANETS = [
    "Sun", "Moon", "Mars", "Mercury", "Jupiter", 
    "Venus", "Saturn", "Rahu", "Ketu"
]

# Zodiac signs
ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

# Houses
HOUSES = [
    "1st House", "2nd House", "3rd House", "4th House", "5th House", "6th House",
    "7th House", "8th House", "9th House", "10th House", "11th House", "12th House"
]

# Divisional charts
DIVISIONAL_CHARTS = {
    "D1": "Rasi / Natal chart",
    "D9": "Navamsa chart",
    "D10": "Dasamsa chart (Career)",
    "D12": "Dwadashamsa chart (Parents)",
    "D24": "Siddhamsa chart (Education / Skills)"
}

# Yogas to detect (starter)
YOGAS = [
    "Neech Bhanga Raj Yoga",
    "Raj Yoga",
    "Dhana Yoga",
    "Parivartana Yoga",
    "Chandra-Mangal Yoga",
    "Gaja-Kesari Yoga"
]

# Default orb for aspect calculations (in degrees)
ASPECT_ORB = 6  # +/- degrees allowed for conjunction/opposition/aspects

# Vimshottari Dasha sequence and years
VIMSHOTTARI_DASHA = {
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

# Logging level
LOG_LEVEL = "INFO"
