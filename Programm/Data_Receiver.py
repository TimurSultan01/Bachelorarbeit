# Schreibe Lösungen in eine Textdatei

def save_result(model, V, path1, path2, assign, edges, x_size, y_size, gridEdges, objective_value, flow, D, duration, filename="results.txt"):
    """
    Speichert die Ergebnisse (Objektivwert, Knoten, Pfade, Kanten, Knotenplatzierungen, verwendete Gittersegmente)
    in der Textdatei 'results.txt'. Jeder Aufruf hängt einen neuen Ergebnisblock an.

    Parameter:
      - V: Liste der Knoten.
      - path1, path2: Listen, die die Reihenfolge der Knoten in den beiden Pfaden angeben.
      - assign: Dictionary der Knotenplatzierungsvariablen (assign[v, p]).
      - edges: Liste der Kanten (Tupel: (Quelle, Senke, path_id, lokale Kanten-ID)).
      - gridEdges: Liste der gerichteten Gitterkanten (Tupel ((x,y), (x',y'))).
      - objective_value: Der Zielwert (model.ObjVal).
      - flow: Dictionary der Flussvariablen (flow[e, p, q]).
      - D: Liste aller Gitterpunkte.
      - filename: Der Name der Datei, in die die Ergebnisse geschrieben werden (Standard: "results.txt").
    """
    with open(filename, "a") as file:
        file.write("=========================================\n")
        file.write("Ergebnisblock:\n")
        file.write(f"Anzahl der Variablen: {model.NumVars}\n")
        file.write(f"Anzahl der Nebenbedingungen: {model.NumConstrs}\n")
        file.write(f"Anzahl der nicht-nullbaren Koeffizienten: {model.NumNZs}\n")
        file.write(f"Dauer der Modellberechnung: {duration:.4f} Sekunden\n")
        file.write("-" * 50 + "\n")
        file.write(f"Objektivwert: {objective_value}\n")
        file.write(f"Gittergröße: {x_size}, {y_size}\n")
        file.write("\nKnoten (V):\n")
        file.write(str(V) + "\n")

        file.write("\nPfad 1:\n")
        file.write(str(path1) + "\n")
        file.write("Pfad 2:\n")
        file.write(str(path2) + "\n")

        file.write("\nKnotenplatzierungen:\n")
        # Gehe über alle Knoten und alle Gitterpunkte
        for v in V:
            for p in D:
                # Wenn assign[v,p] > 0.5 (also Knoten v an p platziert)
                if assign[v, p].X > 0.5:
                    file.write(f"  Knoten {v} bei {p}\n")

        file.write("\nKanten:\n")
        for e in edges:
            file.write(f"  Kante: {e[0]} -> {e[1]}, Pfad-ID: {e[2]}, lokale ID: {e[3]}\n")

        file.write("\nVerwendete Gittersegmente pro Kante:\n")
        # Für jede Kante e: Alle gridEdges, bei denen flow[e, p, q] aktiv ist
        for e in range(len(edges)):
            used_segments = []
            for (p, q) in gridEdges:
                if flow[e, p, q].X > 0.5:
                    used_segments.append(f"{p} -> {q}")
            if used_segments:
                file.write(f"  Für Kante {e}: " + ", ".join(used_segments) + "\n")
        file.write("=========================================\n\n")
