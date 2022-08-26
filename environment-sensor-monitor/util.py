"""Contains modules for handling serial data from environmental sensor"""

def celcius_to_fahrenheit(temp: float) -> float:
    """Celsius to Freedom Units Converter"""
    return (temp * 9 / 5) + 32


def clean_tty_line(line: str) -> str:
    """Removes any garbage in string from sensor and prepares it for being parsed into JSON"""
    return line.strip().replace("'", '"').replace("\n", " ").replace("\r", "")
