# main.py
import simulation
from gui import update_simulation, run_gui, update_grid

def main():
    # Inicializa simulação (posições iniciais, etc.)
    simulation.initialize_simulation()
    # Desenha grade
    update_grid()
    # Começa o loop recursivo
    update_simulation()
    # Inicia interface
    run_gui()

if __name__ == "__main__":
    main()
