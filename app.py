import streamlit as st
from datetime import datetime, date, time as dtime
import re
import requests

from astrology.houses import House
from astrology.planets import PLANETS, normalize_planet_name
from astrology.prompt_builder import build_prompt
from services.llm_client import get_prediction

st.set_page_config(page_title="Agentic Vedic Astrology AI", layout="centered")

st.title("Agentic Vedic Astrology AI Tool")

ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

SIGN_TO_LORD = {
    "Aries": "Mars",
    "Taurus": "Venus",
    "Gemini": "Mercury",
    "Cancer": "Moon",
    "Leo": "Sun",
    "Virgo": "Mercury",
    "Libra": "Venus",
    "Scorpio": "Mars",
    "Sagittarius": "Jupiter",
    "Capricorn": "Saturn",
    "Aquarius": "Saturn",
    "Pisces": "Jupiter"
}

def assign_house_lords(first_house_lord: str) -> list[str]:
    first_house_lord = first_house_lord.lower()
    sign_index = None
    for idx, sign in enumerate(ZODIAC_SIGNS):
        if SIGN_TO_LORD[sign].lower() == first_house_lord:
            sign_index = idx
            break
    if sign_index is None:
        raise ValueError(f"Invalid first house lord: {first_house_lord}")

    house_lords = []
    for i in range(12):
        current_sign = ZODIAC_SIGNS[(sign_index + i) % 12]
        house_lords.append(SIGN_TO_LORD[current_sign])
    return house_lords

def validate_time_string(time_str: str) -> dtime | None:
    """Validate HH:MM 24h format and return datetime.time or None."""
    if not re.match(r"^\d{2}:\d{2}$", time_str.strip()):
        return None
    try:
        hour, minute = map(int, time_str.strip().split(":"))
        if 0 <= hour <= 23 and 0 <= minute <= 59:
            return dtime(hour=hour, minute=minute)
    except Exception:
        return None
    return None

@st.cache_data(show_spinner=False)
def get_countries():
    url = "https://countriesnow.space/api/v0.1/countries/positions"
    resp = requests.get(url)
    if resp.status_code == 200:
        data = resp.json()
        return sorted([c['name'] for c in data['data']])
    return []

@st.cache_data(show_spinner=False)
def get_states(country):
    url = "https://countriesnow.space/api/v0.1/countries/states"
    resp = requests.post(url, json={"country": country})
    if resp.status_code == 200:
        data = resp.json()
        return sorted([s['name'] for s in data['data']['states']])
    return []

@st.cache_data(show_spinner=False)
def get_cities(country, state):
    url = "https://countriesnow.space/api/v0.1/countries/state/cities"
    resp = requests.post(url, json={"country": country, "state": state})
    if resp.status_code == 200:
        data = resp.json()
        return sorted(data['data'])
    return []

# Initialize session state
if "houses_data" not in st.session_state:
    st.session_state.houses_data = [House(number=i+1) for i in range(12)]
if "first_house_lord" not in st.session_state:
    st.session_state.first_house_lord = ""
if "birth_details_verified" not in st.session_state:
    st.session_state.birth_details_verified = False
if "chart_submitted" not in st.session_state:
    st.session_state.chart_submitted = False
if "selected_country" not in st.session_state:
    st.session_state.selected_country = None
if "selected_state" not in st.session_state:
    st.session_state.selected_state = None
if "selected_city" not in st.session_state:
    st.session_state.selected_city = None

tab1, tab2 = st.tabs(["Birth Details Verification", "Question & Prediction"])

with tab1:
    st.header("Step 1: Enter and Verify Birth Details")

    dob = st.date_input(
        "Date of Birth (YYYY-MM-DD)",
        min_value=date(1800, 1, 1),
        max_value=date(2025, 12, 31),
        key="dob"
    )

    time_str = st.text_input(
        "Enter Time of Birth (HH:MM, 24-hour format, e.g. 07:02)",
        placeholder="HH:MM",
        key="time_str"
    )
    validated_time = validate_time_string(time_str)
    if time_str and not validated_time:
        st.error("Invalid time format! Please enter time as HH:MM (24-hour format).")

    # Cascading dropdowns for birth place
    countries = get_countries()
    selected_country = st.selectbox("Select Country", options=["-- Select Country --"] + countries)
    if selected_country != "-- Select Country --":
        states = get_states(selected_country)
        selected_state = st.selectbox("Select State", options=["-- Select State --"] + states)
    else:
        selected_state = "-- Select State --"
    if selected_state != "-- Select State --":
        cities = get_cities(selected_country, selected_state)
        selected_city = st.selectbox("Select City", options=["-- Select City --"] + cities)
    else:
        selected_city = "-- Select City --"

    if selected_country != "-- Select Country --":
        st.session_state.selected_country = selected_country
    else:
        st.session_state.selected_country = None
    if selected_state != "-- Select State --":
        st.session_state.selected_state = selected_state
    else:
        st.session_state.selected_state = None
    if selected_city != "-- Select City --":
        st.session_state.selected_city = selected_city
    else:
        st.session_state.selected_city = None

    if st.session_state.selected_country and st.session_state.selected_state and st.session_state.selected_city:
        st.info(f"Selected Birth Place: {st.session_state.selected_city}, {st.session_state.selected_state}, {st.session_state.selected_country}")
    else:
        st.info("Please select complete birth place (Country, State, City).")

    st.subheader("Select 1st House Lord (Lagna Lord)")
    first_lord_input = st.selectbox(
        "Choose 1st House Lord:",
        options=PLANETS,
        index=0,
        key="first_house_lord_select"
    )
    st.session_state.first_house_lord = normalize_planet_name(first_lord_input)

    if st.button("Verify and Save Chart"):
        if not validated_time:
            st.error("Please enter a valid time of birth before verifying.")
        elif not (st.session_state.selected_country and st.session_state.selected_state and st.session_state.selected_city):
            st.error("Please select your birth place completely before verifying.")
        else:
            st.session_state.birth_details_verified = True
            st.success("Birth details and 1st house lord saved and verified.")

with tab2:
    if not st.session_state.birth_details_verified:
        st.warning("Please verify birth details in the 'Birth Details Verification' tab first.")
    else:
        st.header("Step 2: Enter Planets in Houses")

        try:
            house_lords = assign_house_lords(st.session_state.first_house_lord)
        except ValueError as e:
            st.error(str(e))
            st.stop()

        def input_planets_for_house(house_number: int):
            planets_present = st.multiselect(
                label=f"Planets present in House {house_number} (leave empty if none):",
                options=PLANETS,
                default=[],
                key=f"planets_in_house_{house_number}"
            )
            return [normalize_planet_name(p) for p in planets_present]

        for i in range(12):
            planets_in_house = input_planets_for_house(i + 1)
            st.session_state.houses_data[i].number = i + 1
            st.session_state.houses_data[i].lord = house_lords[i]
            st.session_state.houses_data[i].planets = planets_in_house

        if st.button("Submit Chart Data"):
            st.session_state.chart_submitted = True
            st.success("Chart data submitted successfully.")

        if st.session_state.chart_submitted:
            st.markdown("### Chart Summary:")
            for house in st.session_state.houses_data:
                planets_str = ", ".join(house.planets) if house.planets else "None"
                st.write(f"House {house.number}: Lord = **{house.lord}**, Planets = {planets_str}")

            question = st.text_area("Ask your astrology question here:", height=100)

            if st.button("Get Prediction"):
                if question.strip() == "":
                    st.error("Please enter a question.")
                else:
                    with st.spinner("Generating prediction..."):
                        prompt = build_prompt(st.session_state.houses_data, question)
                        prediction = get_prediction(prompt)
                    st.markdown("### AI Prediction:")
                    st.write(prediction)
