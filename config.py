# config.py
import math

G = 1.0  # Constante gravitacional

SUN_MASS = 1000.0
MERCURY_MASS = 50.0
VENUS_MASS = 80.0
EARTH_MASS = 100.0
MARS_MASS = 0.0
MOON_MASS = 0.0
PLUTO_MASS = 0.0022

orbital_parameters = {
    "Mercury": {
        "semi_major_axis": 100.0,
        "eccentricity": 0.2056,
        "mass": MERCURY_MASS,
        "color": "gray",
        "radius": 5
    },
    "Venus": {
        "semi_major_axis": 200.0,
        "eccentricity": 0.0067,
        "mass": VENUS_MASS,
        "color": "orange",
        "radius": 8
    },
    "Earth": {
        "semi_major_axis": 300.0,
        "eccentricity": 0.0167,
        "mass": EARTH_MASS,
        "color": "blue",
        "radius": 8
    },
    "Mars": {
        "semi_major_axis": 400.0,
        "eccentricity": 0.0934,
        "mass": MARS_MASS,
        "color": "red",
        "radius": 7
    },
    "Moon": {
        "semi_major_axis": 40.0,
        "eccentricity": 0.0549,
        "mass": MOON_MASS,
        "color": "lightgray",
        "radius": 3
    },
    "Pluto": {
        "semi_major_axis": 5906.4,
        "eccentricity": 0.2488,
        "mass": PLUTO_MASS,
        "color": "white",
        "radius": 4
    }
}

zoom_factor = 1.0
CANVAS_WIDTH, CANVAS_HEIGHT = 1920, 1080
center_x = CANVAS_WIDTH // 2
center_y = CANVAS_HEIGHT // 2

sun_display_radius = 50
