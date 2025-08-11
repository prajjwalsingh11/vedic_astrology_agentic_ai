from typing import List
from astrology.houses import House
from astrology.planets import PLANETS, PLANET_EXALTATION_SIGNS, PLANET_DEBILITATION_SIGNS, get_aspected_houses

def build_prompt(houses_data: List[House], user_question: str) -> str:
    """
    Builds a detailed prompt string to send to the LLM based on house and planet info.
    Includes exaltation/debilitation and aspects.
    """
    prompt_lines = []
    prompt_lines.append("You are an expert Vedic astrologer AI.")
    prompt_lines.append("The user has provided the following birth chart data:")
    prompt_lines.append("")

    for house in houses_data:
        planets_str = ", ".join(house.planets) if house.planets else "No planets"
        prompt_lines.append(f"House {house.number}: Lord is {house.lord}, Planets present: {planets_str}")

        # Add exaltation/debilitation info for planets in house
        for planet in house.planets:
            exalted = PLANET_EXALTATION_SIGNS.get(planet, "Unknown")
            debilitated = PLANET_DEBILITATION_SIGNS.get(planet, "Unknown")
            prompt_lines.append(f"  - {planet} is exalted in {exalted} and debilitated in {debilitated}")

        # Aspects of planets in this house
        for planet in house.planets:
            asp_houses = get_aspected_houses(planet, house.number)
            asp_houses_str = ", ".join(str(h) for h in asp_houses)
            prompt_lines.append(f"  - {planet} aspects houses: {asp_houses_str}")

    prompt_lines.append("")
    prompt_lines.append("Answer the following user question based on this chart and your knowledge of Vedic astrology:")
    prompt_lines.append(f"Question: {user_question}")
    prompt_lines.append("Provide detailed and reasoned astrological prediction referencing the planets, houses, aspects, exaltation, and debilitation.")

    return "\n".join(prompt_lines)
