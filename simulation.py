# simulation.py
import math
from config import (
    G, SUN_MASS, EARTH_MASS,
    orbital_parameters
)

# Estado geral
orbital_state = {}
simulation_data = {}

delta_time = 1.0
time_scale = 1.0

current_time = 0
paused = False

def initialize_simulation():

    global orbital_state, simulation_data, current_time, paused
    current_time = 0
    paused = False
    orbital_state.clear()
    simulation_data.clear()

    # Planetas (menos Lua)
    for body, params in orbital_parameters.items():
        if body == "Moon":
            continue

        a = params["semi_major_axis"]
        e = params["eccentricity"]
        inclination_deg = params.get("inclination", 0)
        inclination = math.radians(inclination_deg)

        # Posição (periélio)
        perihelion_dist = a * (1 - e)
        pos_x = perihelion_dist
        pos_y = 0.0

        # Velocidade no periélio
        vel = math.sqrt(G * SUN_MASS * ((2 / perihelion_dist) - (1 / a)))
        vel_x = 0.0
        vel_y = vel

        z_offset = pos_x * math.sin(inclination)

        orbital_state[body] = {
            "pos_x": pos_x,
            "pos_y": pos_y + z_offset,
            "vel_x": vel_x,
            "vel_y": vel_y
        }

    # Lua (depende da Terra)
    if "Moon" in orbital_parameters:
        body = "Moon"
        params = orbital_parameters["Moon"]
        a = params["semi_major_axis"]
        e = params["eccentricity"]
        inclination_deg = params.get("inclination", 0)
        inclination = math.radians(inclination_deg)

        earth_x = orbital_state["Earth"]["pos_x"]
        earth_y = orbital_state["Earth"]["pos_y"]
        perigee_dist = a * (1 - e)

        pos_x = earth_x + perigee_dist
        pos_y = earth_y

        # Velocidade relativa Lua x Terra
        rel_vel = math.sqrt(G * EARTH_MASS * (1 + e) / (a * (1 - e)))

        vel_x = 0.0
        vel_y = orbital_state["Earth"]["vel_y"] + rel_vel
        z_offset = 0.0

        orbital_state[body] = {
            "pos_x": pos_x,
            "pos_y": pos_y + z_offset,
            "vel_x": vel_x,
            "vel_y": vel_y
        }

    for body in orbital_parameters.keys():
        simulation_data[body] = {
            "time": [],
            "velocity": [],
            "distance_sun": []
        }
    if "Moon" in simulation_data:
        simulation_data["Moon"]["distance_earth"] = []

def update_physics():
    global current_time, paused
    if paused:
        return

    effective_dt = delta_time * time_scale

    current_time += effective_dt

    # Planetas em torno do Sol
    for planet in ["Mercury", "Venus", "Earth", "Mars", "Pluto"]:
        pos_x = orbital_state[planet]["pos_x"]
        pos_y = orbital_state[planet]["pos_y"]
        dist_sun = math.sqrt(pos_x**2 + pos_y**2)

        acc_x = -G * SUN_MASS * (pos_x / (dist_sun**3))
        acc_y = -G * SUN_MASS * (pos_y / (dist_sun**3))

        orbital_state[planet]["vel_x"] += acc_x * effective_dt
        orbital_state[planet]["vel_y"] += acc_y * effective_dt

        speed = math.sqrt(
            orbital_state[planet]["vel_x"]**2 +
            orbital_state[planet]["vel_y"]**2
        )
        simulation_data[planet]["time"].append(current_time)
        simulation_data[planet]["velocity"].append(speed)
        simulation_data[planet]["distance_sun"].append(dist_sun)

    # Lua sofre atração do Sol e da Terra
    moon_x = orbital_state["Moon"]["pos_x"]
    moon_y = orbital_state["Moon"]["pos_y"]
    earth_x = orbital_state["Earth"]["pos_x"]
    earth_y = orbital_state["Earth"]["pos_y"]

    dist_moon_sun = math.sqrt(moon_x**2 + moon_y**2)
    acc_moon_sun_x = -G * SUN_MASS * (moon_x / dist_moon_sun**3)
    acc_moon_sun_y = -G * SUN_MASS * (moon_y / dist_moon_sun**3)

    dx = earth_x - moon_x
    dy = earth_y - moon_y
    dist_moon_earth = math.sqrt(dx**2 + dy**2)

    acc_moon_earth_x = G * EARTH_MASS * (dx / dist_moon_earth**3)
    acc_moon_earth_y = G * EARTH_MASS * (dy / dist_moon_earth**3)

    total_acc_x = acc_moon_sun_x + acc_moon_earth_x
    total_acc_y = acc_moon_sun_y + acc_moon_earth_y

    orbital_state["Moon"]["vel_x"] += total_acc_x * effective_dt
    orbital_state["Moon"]["vel_y"] += total_acc_y * effective_dt

    speed_moon = math.sqrt(
        orbital_state["Moon"]["vel_x"]**2 +
        orbital_state["Moon"]["vel_y"]**2
    )
    simulation_data["Moon"]["time"].append(current_time)
    simulation_data["Moon"]["velocity"].append(speed_moon)
    simulation_data["Moon"]["distance_sun"].append(dist_moon_sun)
    simulation_data["Moon"]["distance_earth"].append(dist_moon_earth)

    # Integrar posição
    for body in orbital_state.keys():
        orbital_state[body]["pos_x"] += orbital_state[body]["vel_x"] * effective_dt
        orbital_state[body]["pos_y"] += orbital_state[body]["vel_y"] * effective_dt

def toggle_pause_simulation():
    global paused
    paused = not paused

def restart_simulation():
    initialize_simulation()
