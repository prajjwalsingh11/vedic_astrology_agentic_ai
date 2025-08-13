# AstroAgent/rules_engine/explanation_layer.py

from config import PLANETS, HOUSES, YOGAS
from utils.logger import setup_logger

logger = setup_logger("ExplanationLayer")

class ExplanationLayer:
    """
    Converts raw astrology analysis into human-readable astrological interpretations.
    """

    def __init__(self):
        pass

    def interpret_planetary_strengths(self, planetary_report):
        """
        Converts planetary strengths dict into readable sentences.
        """
        lines = []
        for planet, strength in planetary_report.items():
            if strength == "strong":
                lines.append(f"{planet} is well-placed and provides positive influence.")
            elif strength == "weak":
                lines.append(f"{planet} is weak or debilitated; challenges may arise.")
            else:
                lines.append(f"{planet} has neutral influence.")
        return "\n".join(lines)

    def interpret_yogas(self, yogas_report):
        """
        Converts detected yogas list into human-readable descriptions.
        """
        lines = []
        for yoga in yogas_report:
            if yoga in YOGAS:
                lines.append(f"{yoga} is present in the chart, which brings special results.")
            else:
                lines.append(f"{yoga} is detected.")
        return "\n".join(lines)

    def interpret_dashas(self, dashas_report):
        """
        Converts current Dasha info into readable form.
        """
        mahadasha = dashas_report.get("Mahadasha", "Unknown")
        antardasha = dashas_report.get("Antardasha", "Unknown")
        return f"Current Mahadasha: {mahadasha}, Antardasha: {antardasha}"

    def interpret_house_analysis(self, house_report):
        """
        Converts house-specific analysis (career, marriage, wealth, spirituality)
        into readable form.
        """
        lines = []
        for key, desc in house_report.items():
            lines.append(f"{key.capitalize()}: {desc}")
        return "\n".join(lines)

    def generate_full_report(self, full_analysis_dict):
        """
        Takes the unified dict from AstrologyAnalysis.full_analysis() and
        returns a readable astrology report.
        """
        report_sections = []

        if "planetary_strengths" in full_analysis_dict:
            report_sections.append("=== Planetary Strengths ===")
            report_sections.append(self.interpret_planetary_strengths(full_analysis_dict["planetary_strengths"]))

        if "yogas" in full_analysis_dict:
            report_sections.append("\n=== Yogas ===")
            report_sections.append(self.interpret_yogas(full_analysis_dict["yogas"]))

        if "dashas" in full_analysis_dict:
            report_sections.append("\n=== Current Dasha ===")
            report_sections.append(self.interpret_dashas(full_analysis_dict["dashas"]))

        if "house_analysis" in full_analysis_dict:
            report_sections.append("\n=== House Analysis ===")
            report_sections.append(self.interpret_house_analysis(full_analysis_dict["house_analysis"]))

        return "\n".join(report_sections)
