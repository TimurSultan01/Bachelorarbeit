# Tests ausführen und dokumentieren
from ILP_Formula import create_ilp_formula
from Data_Receiver import save_result
import time

# Definiere verschiedene Szenarien mit Gittergrößen, Knoten und Pfaden
scenarios = [
    {"x_size": 5, "y_size": 5,
     "V": [1, 2, 3, 4, 5],
     "path1": [1, 2, 3, 4],
     "path2": [1, 3, 5]},

    {"x_size": 5, "y_size": 4,
     "V": [1, 2, 3, 4, 5, 6],
     "path1": [1, 2, 4, 6],
     "path2": [1, 3, 5, 6]}
]

# Iteriere über die verschiedenen Szenarien
for i, scenario in enumerate(scenarios):

    # Berechne die ILP-Lösung für das aktuelle Szenario
    start_time = time.time()
    model, assign, flow, edges, gridEdges, D, objective_value = create_ilp_formula(
        scenario["x_size"], scenario["y_size"],
        scenario["V"], scenario["path1"], scenario["path2"]
    )
    end_time = time.time()
    duration = end_time - start_time
    # Speichere die Ergebnisse in einer Datei
    save_result(model, scenario["V"], scenario["path1"], scenario["path2"], assign, edges, scenario["x_size"], scenario["y_size"], gridEdges, objective_value, flow, D, duration)
