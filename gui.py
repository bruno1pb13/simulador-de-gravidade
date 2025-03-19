import tkinter as tk
import math

import config
import simulation


window = tk.Tk()
window.title("Simulação de Órbitas Elípticas")

control_frame = tk.Frame(window)
control_frame.pack(side=tk.TOP, fill=tk.X)

def on_pause_click():
    simulation.toggle_pause_simulation()
    if simulation.paused:
        btn_pause.config(text="Retomar")
    else:
        btn_pause.config(text="Pausar")

btn_pause = tk.Button(control_frame, text="Pausar", command=on_pause_click)
btn_pause.pack(side=tk.LEFT, padx=5, pady=5)

def on_restart_click():
    simulation.restart_simulation()
    for b in orbit_trails:
        orbit_trails[b] = []
    update_grid()
    btn_pause.config(text="Pausar")

btn_restart = tk.Button(control_frame, text="Reiniciar", command=on_restart_click)
btn_restart.pack(side=tk.LEFT, padx=5, pady=5)

canvas = tk.Canvas(window, width=config.CANVAS_WIDTH, height=config.CANVAS_HEIGHT, bg="black")
canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


speed_var = tk.DoubleVar(value=0.0)

def on_speed_change(new_value):
    # new_value é string; converte para float
    speed = float(new_value)
    # Define na simulação
    simulation.time_scale = speed

speed_label = tk.Label(control_frame, text="Velocidade:")
speed_label.pack(side=tk.LEFT)

speed_scale = tk.Scale(
    control_frame,
    from_=-5.0,
    to=5.0,
    resolution=.1,
    orient=tk.HORIZONTAL,
    variable=speed_var,
    command=on_speed_change
)
speed_scale.pack(side=tk.LEFT, padx=5)

# { nome_corpo: id_do_canvas }
canvas_objects = {}

orbit_trails = {body: [] for body in config.orbital_parameters}

# ------------------------------------------------------------------

def update_grid():

    canvas.delete("grid")
    base_spacing = 50
    spacing = base_spacing * config.zoom_factor

    for x in range(0, config.CANVAS_WIDTH, int(spacing)):
        canvas.create_line(x, 0, x, config.CANVAS_HEIGHT, fill="gray", tags="grid")
    for y in range(0, config.CANVAS_HEIGHT, int(spacing)):
        canvas.create_line(0, y, config.CANVAS_WIDTH, y, fill="gray", tags="grid")

    canvas.tag_lower("grid")


def adjust_zoom(event):

    def clean_trails():
        for b in orbit_trails:
            orbit_trails[b] = []

    if event.delta > 0:
        config.zoom_factor *= 1.1
    else:
        config.zoom_factor /= 1.1

    clean_trails()

    update_grid()

    draw_scene()

canvas.bind("<MouseWheel>", adjust_zoom)

def draw_scene():

    sun_radius_scaled = config.sun_display_radius * config.zoom_factor

    canvas.coords(
        canvas_objects["Sun"],
        config.center_x - sun_radius_scaled,
        config.center_y - sun_radius_scaled,
        config.center_x + sun_radius_scaled,
        config.center_y + sun_radius_scaled
    )

    for body, state in simulation.orbital_state.items():
        if body == "Sun":
            continue

        pos_x = state["pos_x"]
        pos_y = state["pos_y"]

        # Cálculo de inclinação (pseudo-3D)
        inclination_deg = config.orbital_parameters.get(body, {}).get("inclination", 0)
        inclination = math.radians(inclination_deg)
        z_offset = pos_x * math.sin(inclination)

        screen_x = config.center_x + pos_x * config.zoom_factor
        screen_y = config.center_y - (pos_y + z_offset) * config.zoom_factor

        r_original = config.orbital_parameters[body]["radius"]
        r_scaled = r_original * config.zoom_factor

        canvas.coords(
            canvas_objects[body],
            screen_x - r_scaled, screen_y - r_scaled,
            screen_x + r_scaled, screen_y + r_scaled
        )

        orbit_trails[body].append((screen_x, screen_y))
        if len(orbit_trails[body]) > 1000:
            orbit_trails[body].pop(0)

        canvas.delete(f"trail_{body}")
        if len(orbit_trails[body]) > 1:
            coords = []
            for pt in orbit_trails[body]:
                coords.extend(pt)
            color = config.orbital_parameters[body]["color"]
            canvas.create_line(coords, fill=color, tags=f"trail_{body}")


def update_simulation():
    simulation.update_physics()
    draw_scene()
    window.after(10, update_simulation)


sun_radius_scaled = config.sun_display_radius * config.zoom_factor

canvas_objects["Sun"] = canvas.create_oval(
    config.center_x - sun_radius_scaled,
    config.center_y - sun_radius_scaled,
    config.center_x + sun_radius_scaled,
    config.center_y + sun_radius_scaled,
    fill="yellow"
)

for body, params in config.orbital_parameters.items():
    color = params["color"]
    radius = params["radius"]
    obj_id = canvas.create_oval(
        config.center_x - radius,
        config.center_y - radius,
        config.center_x + radius,
        config.center_y + radius,
        fill=color
    )
    canvas_objects[body] = obj_id


def run_gui():
    window.mainloop()
