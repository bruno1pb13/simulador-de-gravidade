import math
import tkinter as tk

G = 1.0 # CONSTANTE GRAVITACIONAL


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
        "radius": 4,
    }
}

orbital_state = {}

zoom_factor = 1.0
CANVAS_WIDTH, CANVAS_HEIGHT = 1920, 1080
center_x = CANVAS_WIDTH // 2
center_y = CANVAS_HEIGHT // 2

window = tk.Tk()
window.title("Simulação de Órbitas Elípticas")
canvas = tk.Canvas(window, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="black")
canvas.pack()

orbit_trails = { body: [] for body in orbital_parameters.keys() }

def update_grid():
    global zoom_factor
    canvas.delete("grid")
    base_spacing = 50
    spacing = base_spacing * zoom_factor

    for x in range(0, CANVAS_WIDTH, int(spacing)):
        canvas.create_line(x, 0, x, CANVAS_HEIGHT, fill="gray", tags="grid")

    for y in range(0, CANVAS_HEIGHT, int(spacing)):
        canvas.create_line(0, y, CANVAS_WIDTH, y, fill="gray", tags="grid")

    canvas.tag_lower("grid")


def adjust_zoom(event):
    global zoom_factor, orbit_trails

    def clean_trails():
        for body in orbit_trails.keys():
            orbit_trails[body] = []


    if event.delta > 0:
        zoom_factor *= 1.1
        clean_trails()

    elif event.delta < 0:
        zoom_factor /= 1.1
        clean_trails()

    display_sun_radius = sun_display_radius * zoom_factor
    canvas.coords(canvas_objects["Sun"],
                  center_x - display_sun_radius, center_y - display_sun_radius,
                  center_x + display_sun_radius, center_y + display_sun_radius)

    update_grid()

    # Atualiza a posição dos objetos no canvas conforme o novo zoom
    for body in orbital_state.keys():
        body_radius = orbital_parameters.get(body, {}).get("radius", sun_display_radius) * zoom_factor
        if body == "Sun":
            continue
        else:
            body_inclination = math.radians(orbital_parameters.get(body, {}).get("inclination", 0))
            z_offset = orbital_state[body]["pos_x"] * math.sin(body_inclination)
            canvas_x = center_x + orbital_state[body]["pos_x"] * zoom_factor
            canvas_y = center_y - (orbital_state[body]["pos_y"] + z_offset) * zoom_factor
            canvas.coords(canvas_objects[body],
                          canvas_x - body_radius, canvas_y - body_radius,
                          canvas_x + body_radius, canvas_y + body_radius)



# Inicializa as posições e velocidades
for body, params in orbital_parameters.items():
    semi_major_axis = params["semi_major_axis"]
    eccentricity = params["eccentricity"]
    body_inclination = math.radians(params.get("inclination", 0))

    if body == "Moon":

        earth_pos_x = orbital_state["Earth"]["pos_x"]
        earth_pos_y = orbital_state["Earth"]["pos_y"]
        perigee_distance = semi_major_axis * (1 - eccentricity)
        pos_x = earth_pos_x + perigee_distance
        pos_y = earth_pos_y
        
        # Velocidade relativa da Lua em relação à Terra no perigeu
        relative_velocity = math.sqrt(G * EARTH_MASS * (1 + eccentricity) /
                                      (semi_major_axis * (1 - eccentricity)))
        vel_x = 0.0
        vel_y = orbital_state["Earth"]["vel_y"] + relative_velocity
        z_offset = 0.0
    else:
        perihelion_distance = semi_major_axis * (1 - eccentricity)
        pos_x = perihelion_distance
        pos_y = 0.0
        perihelion_velocity = math.sqrt(G * SUN_MASS *
                                        ((2 / perihelion_distance) - (1 / semi_major_axis)))
        vel_x = 0.0
        vel_y = perihelion_velocity
        z_offset = pos_x * math.sin(body_inclination)

    orbital_state[body] = {
        "pos_x": pos_x,
        "pos_y": pos_y + z_offset,
        "vel_x": vel_x,
        "vel_y": vel_y
    }

update_grid()

canvas_objects = {}
sun_display_radius = 50
canvas_objects["Sun"] = canvas.create_oval(
    center_x - sun_display_radius, center_y - sun_display_radius,
    center_x + sun_display_radius, center_y + sun_display_radius,
    fill="yellow"
)

for body, params in orbital_parameters.items():
    color = params["color"]
    body_radius = params["radius"]
    canvas_x = center_x + orbital_state[body]["pos_x"] * zoom_factor
    canvas_y = center_y - orbital_state[body]["pos_y"] * zoom_factor
    canvas_objects[body] = canvas.create_oval(
        canvas_x - body_radius, canvas_y - body_radius,
        canvas_x + body_radius, canvas_y + body_radius,
        fill=color
    )

canvas.bind("<MouseWheel>", adjust_zoom)

delta_time = 1.0  # Intervalo de tempo por frame da simulação
current_time = 0


simulation_data = {body: {"time": [], "velocity": [], "distance_sun": []} for body in orbital_parameters.keys()}
if "Moon" in orbital_parameters:
    simulation_data["Moon"]["distance_earth"] = []  # Armazena distância da Lua à Terra




def update_simulation():
    global current_time
    current_time += delta_time


    for planet in ["Mercury", "Venus", "Earth", "Mars", "Pluto"]:
        pos_x = orbital_state[planet]["pos_x"]
        pos_y = orbital_state[planet]["pos_y"]
        planet_params = orbital_parameters[planet]
        body_inclination = math.radians(planet_params.get("inclination", 0))
        distance_to_sun = math.sqrt(pos_x ** 2 + pos_y ** 2)
        acceleration_x = -G * SUN_MASS * (pos_x / (distance_to_sun ** 3))
        acceleration_y = -G * SUN_MASS * (pos_y / (distance_to_sun ** 3))
        orbital_state[planet]["vel_x"] += acceleration_x * delta_time
        orbital_state[planet]["vel_y"] += acceleration_y * delta_time

        velocity = math.sqrt(orbital_state[planet]["vel_x"] ** 2 + orbital_state[planet]["vel_y"] ** 2)

        simulation_data[planet]["time"].append(current_time)
        simulation_data[planet]["velocity"].append(velocity)
        simulation_data[planet]["distance_sun"].append(distance_to_sun)

    # Atualiza a Lua considerando a atração do Sol e da Terra
    moon_pos_x = orbital_state["Moon"]["pos_x"]
    moon_pos_y = orbital_state["Moon"]["pos_y"]
    earth_pos_x = orbital_state["Earth"]["pos_x"]
    earth_pos_y = orbital_state["Earth"]["pos_y"]

    distance_moon_sun = math.sqrt(moon_pos_x ** 2 + moon_pos_y ** 2)
    acceleration_moon_sun_x = -G * SUN_MASS * (moon_pos_x / (distance_moon_sun ** 3))
    acceleration_moon_sun_y = -G * SUN_MASS * (moon_pos_y / (distance_moon_sun ** 3))

    delta_x = earth_pos_x - moon_pos_x
    delta_y = earth_pos_y - moon_pos_y
    distance_moon_earth = math.sqrt(delta_x ** 2 + delta_y ** 2)
    acceleration_moon_earth_x = G * EARTH_MASS * (delta_x / (distance_moon_earth ** 3))
    acceleration_moon_earth_y = G * EARTH_MASS * (delta_y / (distance_moon_earth ** 3))

    total_acceleration_moon_x = acceleration_moon_sun_x + acceleration_moon_earth_x
    total_acceleration_moon_y = acceleration_moon_sun_y + acceleration_moon_earth_y

    orbital_state["Moon"]["vel_x"] += total_acceleration_moon_x * delta_time
    orbital_state["Moon"]["vel_y"] += total_acceleration_moon_y * delta_time

    velocity_moon = math.sqrt(orbital_state["Moon"]["vel_x"] ** 2 + orbital_state["Moon"]["vel_y"] ** 2)

    simulation_data["Moon"]["time"].append(current_time)
    simulation_data["Moon"]["velocity"].append(velocity_moon)
    simulation_data["Moon"]["distance_sun"].append(distance_moon_sun)
    simulation_data["Moon"]["distance_earth"].append(distance_moon_earth)


    # Atualiza posições e reposiciona os objetos no canvas
    for body in orbital_state.keys():
        orbital_state[body]["pos_x"] += orbital_state[body]["vel_x"] * delta_time
        orbital_state[body]["pos_y"] += orbital_state[body]["vel_y"] * delta_time

        body_inclination = math.radians(orbital_parameters.get(body, {}).get("inclination", 0))
        z_offset = orbital_state[body]["pos_x"] * math.sin(body_inclination)

        if body == "Sun":
            default_radius = orbital_parameters.get(body, {}).get("radius", sun_display_radius)
            canvas.coords(
                canvas_objects[body],
                center_x - (default_radius * zoom_factor), center_y - (default_radius * zoom_factor),
                center_x + (default_radius * zoom_factor), center_y + (default_radius * zoom_factor)
            )
        else:

            canvas_x = center_x + orbital_state[body]["pos_x"] * zoom_factor
            canvas_y = center_y - (orbital_state[body]["pos_y"] + z_offset) * zoom_factor
            body_radius = orbital_parameters[body]["radius"] * zoom_factor
            canvas.coords(
                canvas_objects[body],
                canvas_x - body_radius, canvas_y - body_radius,
                canvas_x + body_radius, canvas_y + body_radius
            )

            orbit_trails[body].append((canvas_x, canvas_y))
            if len(orbit_trails[body]) > 1000:
                orbit_trails[body].pop(0)

            canvas.delete(f"trail_{body}")

            if len(orbit_trails[body]) > 1:
                coords = []
                for point in orbit_trails[body]:
                    coords.extend(point)
                canvas.create_line(coords, fill=orbital_parameters[body].get("color", "white"),
                                   tags=f"trail_{body}")

    window.after(10, update_simulation)




update_simulation()
window.mainloop()
