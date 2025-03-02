# GUI for solutions
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')


def plot_solution(D, assign, flow, gridEdges, edges, V):
    """
    Zeichnet das Gitter, die Knoten und die von den Pfaden belegten Gitterkanten.
    Ein Gittersegment wird in Blau gezeichnet, wenn nur Pfad 1 es nutzt,
    in Rot, wenn nur Pfad 2 es nutzt, und in Lila, wenn beide Pfade es nutzen.

    Parameter:
      - D: Liste aller Gitterpunkte (Tupel (x, y))
      - assign: Dictionary der Knotenplatzierungsvariablen (assign[v, p])
      - flow: Dictionary der Flussvariablen (flow[e, p, q])
      - gridEdges: Liste der erlaubten gerichteten Gitterkanten (Tupel ((x, y), (x', y')))
      - edges: Liste der Kanten (Tupel: (Quelle, Senke, path_id, lokale Kanten-ID))
      - V: Liste der Knoten
    """
    # Bestimme Gittergrenzen
    xs = [p[0] for p in D]
    ys = [p[1] for p in D]
    xmin, xmax = min(xs) - 0.5, max(xs) + 0.5
    ymin, ymax = min(ys) - 0.5, max(ys) + 0.5

    fig, ax = plt.subplots(figsize=(8, 8))

    # Zeichne Gitterlinien (Hintergrund)
    for x in range(min(xs), max(xs) + 1):
        ax.plot([x, x], [ymin, ymax], color='lightgray', lw=1)
    for y in range(min(ys), max(ys) + 1):
        ax.plot([xmin, xmax], [y, y], color='lightgray', lw=1)

    # Zeichne Knoten: An den Gitterpunkten, an denen Knoten platziert sind,
    # wird ein schwarzer Kreis (mit Knotennummer in weiß) gezeichnet.
    for v in V:
        for p in D:
            if assign[v, p].X > 0.5:
                ax.scatter(p[0], p[1], s=200, c='black', zorder=5)
                ax.text(p[0], p[1], str(v), color='white', ha='center', va='center', zorder=6)

    # Erstelle ein Dictionary ungerichteter Kanten.
    # Für jedes gerichtete Segment (p, q) in gridEdges definieren wir einen Schlüssel,
    # der die Kante als sortiertes Tupel repräsentiert.
    undirected_edges = {}
    for (p, q) in gridEdges:
        key = tuple(sorted([p, q]))
        undirected_edges[key] = key

    # Setze einen Toleranzwert, um numerische Rundungsfehler abzufangen
    tol = 0.5

    # Für jede ungerichtete Kante (also jedes Segment) ermitteln wir, ob es von Pfad 1, Pfad 2 oder beiden verwendet wird.
    for key in undirected_edges:
        p, q = key  # Diese Reihenfolge ist willkürlich (sortiert), aber ausreichend
        use_path1 = False
        use_path2 = False

        # Durchlaufe alle Kanten (Flusskommoditäten)
        for e in range(len(edges)):
            # Prüfe beide Richtungen: (p,q) und (q,p)
            if flow[e, p, q].X >= tol or flow[e, q, p].X >= tol:
                if edges[e][2] == 1:
                    use_path1 = True
                elif edges[e][2] == 2:
                    use_path2 = True

        # Bestimme die Farbe anhand der Benutzung:
        if use_path1 and use_path2:
            color = 'purple'
        elif use_path1:
            color = 'blue'
        elif use_path2:
            color = 'red'
        else:
            continue  # Dieses Segment wird von keinem Pfad verwendet.

        # Zeichne das Segment als Linie
        ax.plot([p[0], q[0]], [p[1], q[1]], color=color, lw=3, zorder=3)

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_aspect('equal')
    ax.set_title("Simultaneous Embedding Visualisierung (Richtungsunabhängig)")
    plt.show()
