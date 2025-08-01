# bilde das lineare ganzzählige Optimimierungsmodell

import gurobipy as gp
from gurobipy import GRB, quicksum

# Definiere Knotenmenge
# V = [1, 2, 3, 4, 5...]

# Zwei Pfade auf derselben Knotenmenge:
# Pfad 1: 1 -> 2 -> 3 -> 5 -> 4
# path1 = [1, 2, 3, 5, 4]


def create_ilp_formula(x_size, y_size, V, path1, path2):
    # 1. Preparations

    # Definiere den Gitterbereich: x von 0 bis 5, y von 0 bis 5
    Xmin, Xmax = 0, x_size
    Ymin, Ymax = 0, y_size

    # Erzeuge die Menge D der Gitterpunkte:
    D = [(x, y) for x in range(Xmin, Xmax + 1) for y in range(Ymin, Ymax + 1)]

    # Erzeuge gerichtete Gitterkanten.
    gridEdges = []
    for (x, y) in D:
        if (x + 1, y) in D:
            gridEdges.append(((x, y), (x + 1, y)))
        if (x - 1, y) in D:
            gridEdges.append(((x, y), (x - 1, y)))
        if (x, y + 1) in D:
            gridEdges.append(((x, y), (x, y + 1)))
        if (x, y - 1) in D:
            gridEdges.append(((x, y), (x, y - 1)))

    # Erzeuge eine Liste der Kanten für beide Pfade.
    # Jede Kante wird als Tupel (Quelle, Ziel, Pfad-ID, lokale Kanten-ID) definiert.
    edges = []
    for i in range(len(path1) - 1):
        edges.append((path1[i], path1[i + 1], 1, i))
    for i in range(len(path2) - 1):
        edges.append((path2[i], path2[i + 1], 2, i))

    # 2. Variabeln für das Modell aufbauen

    model = gp.Model("SimultaneousEmbedding")

    # 2.1.1: Variablen für Knotenplatzierungen
    # Variable assign[v, p] = 1, wenn Knoten v auf Gitterpunkt p platziert wird.
    assign = {}
    for v in V:
        for p in D:
            assign[v, p] = model.addVar(vtype=GRB.BINARY, name=f"assign_{v}_{p}")

    # 2.1.2: Flussvariablen für jede Kante und jede gerichtete Gitterkante
    # Variable flow[e, p, q] = 1, wenn im Pfad der Kantenfluss e das Gittersegment von p nach q genutzt wird.
    flow = {}
    for e in range(len(edges)):
        for (p, q) in gridEdges:
            flow[e, p, q] = model.addVar(vtype=GRB.BINARY, name=f"flow_{e}_{p}_{q}")

    # Aktualisiere das Modell, um die Variablen einzubinden
    model.update()

    # 3. Nebenbedingungen (Constraints)

    # 3.1: Jeder Knoten muss auf genau einem Gitterpunkt platziert werden.
    for v in V:
        model.addConstr(quicksum(assign[v, p] for p in D) == 1, name=f"vertex_assign_{v}")

    # 3.2: Kein Gitterpunkt darf von mehr als einem Knoten belegt werden.
    for p in D:
        model.addConstr(quicksum(assign[v, p] for v in V) <= 1, name=f"gridpoint_unique_{p}")

    # 3.3: Flusserhaltung für jeden Kantenfluss an jedem Gitterpunkt.
    # Für eine Kante e = (u, v, ...):
    #   - An dem Gitterpunkt, wo u platziert wird, muss der Fluss +1 betragen.
    #   - An dem Gitterpunkt, wo v platziert wird, muss der Fluss -1 betragen.
    #   - An allen anderen Punkten muss der Fluss 0 betragen.
    for e in range(len(edges)):
        source, sink, path_id, edge_id = edges[e]
        for p in D:
            # Summe der ausgehenden Flüsse von p für Kantenfluss e:
            out_flow = quicksum(flow[e, p, q] for (pp, q) in gridEdges if pp == p)
            # Summe der eingehenden Flüsse bei p für Kantenfluss e:
            in_flow = quicksum(flow[e, q, p] for (q, pp) in gridEdges if pp == p)
            # Flusserhaltung: Der Unterschied (out_flow - in_flow) muss gleich
            # (assign[source, p] - assign[sink, p]) sein.
            model.addConstr(out_flow - in_flow == assign[source, p] - assign[sink, p],
                            name=f"flow_conservation_e{e}_p{p}")

    # Big-M-Konstante (hier 2, da maximal 2 Flusseinheiten durch einen Zwischenpunkt fließen können)
    M = 2

    # 3.4: Ein Fluss darf nicht über einen Gitterpunkt verlaufen, an dem ein anderer Knoten
    # (der nicht der Quell- oder Zielknoten dieser Kante ist) platziert wurde.
    for e in range(len(edges)):
        source, sink, path_id, edge_id = edges[e]
        for p in D:
            # Betrachte jeden Knoten w, der NICHT der Quell- oder Zielknoten von e ist.
            for w in V:
                if w != source and w != sink:
                    # Summiere alle Flüsse (sowohl ausgehend als auch eingehend) an p für Kantenfluss e.
                    flow_sum = (quicksum(flow[e, p, q] for (p2, q) in gridEdges if p2 == p) +
                                quicksum(flow[e, q, p] for (q, p2) in gridEdges if p2 == p))
                    # Falls an p ein unerlaubter Knoten w liegt (assign[w, p] == 1),
                    # muss flow_sum gleich 0 sein (kein Durchlaufen).
                    model.addConstr(
                        flow_sum <= M * (1 - assign[w, p]),
                        name=f"no_pass_through_e{e}_p{p}_w{w}"
                    )

    # Bestimme die in den Kanten auftretenden Pfad-IDs
    path_ids = set(e[2] for e in edges)

    # 3.5: Aggregierte Nebenbedingung: Verhindern, dass mehrere Kanten des gleichen Pfades denselben
    # Gitterpunkt benutzen, falls dieser nicht als Knoten zugewiesen ist.
    for r in path_ids:
        for p in D:
            # Aggregierter Fluss an p über alle Kanten des Pfades r:
            aggregated_flow = quicksum(
                # Für alle Kanten e, die zu Pfad r gehören:
                quicksum(flow[e, q, p] for (q, pp) in gridEdges if pp == p)
                +
                quicksum(flow[e, p, q] for (pp, q) in gridEdges if pp == p)
                for e in range(len(edges)) if edges[e][2] == r
            )
            # Linke Seite 0 oder 2 erlaubt, falls p als Zwischenpunkt durchlaufen wird von diesem Pfad,
            # ein eingehender und ein ausgehnder Fluss
            model.addConstr(
                aggregated_flow <= 2,
                name=f"agg_no_self_cross_path{r}_p{p}"
            )

    # 5. Zielfunktion

    # Ziel: Minimierung der Gesamtzahl der benutzten Gittersegmente.
    # Das entspricht der Summe aller flow-Variablen.
    model.setObjective(quicksum(flow[e, p, q] for e in range(len(edges)) for (p, q) in gridEdges), GRB.MINIMIZE)

    model.optimize()
    objective_value = model.ObjVal

    # Rückgabe der wichtigsten Modellkomponenten zur weiteren Verarbeitung
    return model, assign, flow, edges, gridEdges, D, objective_value
