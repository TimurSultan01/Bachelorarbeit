import gurobipy as gp
from gurobipy import GRB


def create_model(n, num_nodes, edges):
    # Erstelle ein Modell
    model = gp.Model()

    # Binärvariablen für Knotenpositionen (G)
    G = model.addVars(num_nodes, n, n, vtype=GRB.BINARY, name="G")

    # Binärvariablen für Punkte auf den Kanten (P)
    P = model.addVars(len(edges), n, n, vtype=GRB.BINARY, name="P")

    # Binärvariablen für Verbindungen zwischen benachbarten Punkten (F)
    F = model.addVars(len(edges), n, n, n, n, vtype=GRB.BINARY, name="F")

    # Nebenbedingungen:
    # 1. Knoten müssen auf genau einem Punkt liegen
    for m in range(num_nodes):
        model.addConstr(sum(G[m, i, j] for i in range(n) for j in range(n)) == 1, name=f"OneNode_{m}")

    # 2. Start- und Endpunkte für jede Kante (basierend auf den Kantenpaaren)
    for idx, (start, end) in enumerate(edges):
        model.addConstr(sum(P[idx, i, j] * G[start, i, j] for i in range(n) for j in range(n)) == 1,
                        name=f"Start_{idx}")
        model.addConstr(sum(P[idx, i, j] * G[end, i, j] for i in range(n) for j in range(n)) == 1, name=f"End_{idx}")

    # 3. Flussgleichung für Kanten
    for idx, (start, end) in enumerate(edges):
        for i in range(n):
            for j in range(n):
                incoming = sum(
                    F[idx, i1, j1, i, j] for i1 in range(n) for j1 in range(n) if abs(i - i1) + abs(j - j1) == 1)
                outgoing = sum(
                    F[idx, i, j, i2, j2] for i2 in range(n) for j2 in range(n) if abs(i - i2) + abs(j - j2) == 1)
                model.addConstr(incoming == outgoing, name=f"Flow_{idx}_{i}_{j}")

    # 4. Keine Überlagerung von Knoten und Kanten
    for i in range(n):
        for j in range(n):
            model.addConstr(sum(P[k, i, j] for k in range(len(edges))) + sum(G[m, i, j] for m in range(num_nodes)) <= 1,
                            name=f"NoOverlap_{i}_{j}")

    # 5. Verbindungen nur zwischen benachbarten Punkten
    for idx, (start, end) in enumerate(edges):
        for i in range(n):
            for j in range(n):
                for i2 in range(n):
                    for j2 in range(n):
                        if abs(i - i2) + abs(j - j2) == 1:
                            model.addConstr(F[idx, i, j, i2, j2] <= P[idx, i, j],
                                            name=f"Connection_{idx}_{i}_{j}_{i2}_{j2}")
                            model.addConstr(F[idx, i, j, i2, j2] <= P[idx, i2, j2],
                                            name=f"Connection_{idx}_{i2}_{j2}_{i}_{j}")

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
    # Gittergröße n und Anzahl der Knoten und Kanten
    n = 3
    num_nodes = 3  # 3 Knoten
    edges = [(0, 1), (1, 2), (0, 2)]  # Kanten zwischen den Knoten definieren

    # Modell erstellen
    model, G, P, F = create_model(n, num_nodes, edges)

    # Optimieren
    model.optimize()

    if model.status == GRB.OPTIMAL:
        # Lösung anzeigen
        display_solution(model, G, P, F, n, num_nodes, edges)
    else:
        print("Keine optimale Lösung gefunden.")


if __name__ == "__main__":
    main()
