# AstroAgent/utils/math_utils.py

def mod360(degrees):
    """Return degrees normalized to 0-360"""
    return degrees % 360

def distance_in_degrees(pos1, pos2):
    """Return angular distance between two positions in degrees"""
    diff = abs(pos1 - pos2)
    return diff if diff <= 180 else 360 - diff

def is_within_orb(pos1, pos2, orb):
    """Check if two positions are within orb degrees"""
    return distance_in_degrees(pos1, pos2) <= orb
