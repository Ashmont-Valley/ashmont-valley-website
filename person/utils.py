from decimal import Decimal

def coord(point, start, size):
    if isinstance(start, tuple):
        start = to_degrees(*start)
    return (abs(Decimal(start)) - abs(point)) * 60 * 60 * Decimal(size)

def to_degrees(degrees, minutes, seconds):
    degrees = Decimal(degrees)
    degrees += Decimal(minutes) / 60
    degrees += Decimal(seconds) / 3600
    return degrees

def to_minutes(degrees):
    """Convert decimal latt/long to seconds/minutes"""
    minutes = abs(degrees) % 1 * 60
    seconds = minutes % 1 * 60
    return (int(degrees), int(minutes), seconds)

