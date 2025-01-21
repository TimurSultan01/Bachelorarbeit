import gurobipy as gp
from gurobipy import GRB


def create_simple_model():
    n = 3  # Gittergröße (z. B. 3x3)
    num_nodes = 2
    edges = [(0, 1)]  # Kante zwischen Knoten 0 und Knoten 1

    # Erstelle ein Modell
    model = gp.Model()

    # Binärvariablen für Knotenpositionen (G)
    G = model.addVars(num_nodes, n, n, vtype=GRB.BINARY, name="G")

    # Binärvariablen für Kantenpunkte (P)
    P = model.addVars(len(edges), n, n, vtype=GRB.BINARY, name="P")

    # Binärvariablen für Flüsse (F)
    F = model.addVars(len(edges), n, n, n, n, vtype=GRB.BINARY, name="F")

    # 1. Knoten müssen auf genau einem Punkt liegen
    for m in range(num_nodes):
        model.addConstr(sum(G[m, i, j] for i in range(n) for j in range(n)) == 1, name=f"OneNode_{m}")

    # 2. Start- und Endpunkte für jede Kante
    for idx, (start, end) in enumerate(edges):
        model.addConstr(sum(P[idx, i, j] * G[start, i, j] for i in range(n) for j in range(n)) == 1,
                        name=f"Start_{idx}")
        model.addConstr(sum(P[idx, i, j] * G[end, i, j] for i in range(n) for j in range(n)) == 1, name=f"End_{idx}")

    # 3. Keine Überlagerung von Knoten und Kanten
    for i in range(n):
        for j in range(n):
            model.addConstr(sum(P[k, i, j] for k in range(len(edges))) + sum(G[m, i, j] for m in range(num_nodes)) <= 1,
                            name=f"NoOverlap_{i}_{j}")

    return model, G, P, F


def display_solution(model, G, P, F, n, num_nodes, edges):
    print("Solution:")
    for m in range(num_nodes):
        for i in range(n):
            for j in range(n):
                if G[m, i, j].x > 0.5:
                    print(f"Knoten {m} befindet sich bei ({i},{j})")

    for idx, (start, end) in enumerate(edges):
        print(f"Kante {idx}: von Knoten {start} nach Knoten {end}")
        for i in range(n):
            for j in range(n):
                if P[idx, i, j].x > 0.5:
                    print(f"  Kante {idx} hat Punkt ({i},{j})")
        for i in range(n):
            for j in range(n):
                for i2 in range(n):
                    for j2 in range(n):
                        if F[idx, i, j, i2, j2].x > 0.5:
                            print(f"  Verbindung von ({i},{j}) nach ({i2},{j2})")


def main():
    # Einfaches Modell mit 2 Knoten und 1 Kante
    model, G, P, F = create_simple_model()

    # Optimieren
    model.optimize()

    if model.status == GRB.OPTIMAL:
        # Lösung anzeigen
        display_solution(model, G, P, F, 3, 2, [(0, 1)])
    else:
        print("Keine optimale Lösung gefunden.")


if __name__ == "__main__":
    main()
