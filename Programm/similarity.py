# Generiere zufällige Testfälle mit x-gleichen adjazenten Knoten
import random


def count_common_adj_nodes(path1, path2):
    def extract_edges(path):
        return [frozenset((path[i], path[i + 1])) for i in range(len(path) - 1)]

    edges1 = set(extract_edges(path1))
    edges2 = set(extract_edges(path2))
    return len(edges1 & edges2)


def generate_hamiltonian_paths(V, common_edges_target, num_cases=10):
    """
        Generiere 'num_cases' Paare von PFade auf der Knotenmenge V
        mit genau x gleichen adjazenten Kanten

        Returns:
        - Liste von Tuple (path1, path2) mit Länge num_cases
        """
    test_cases = []
    while len(test_cases) < num_cases:
        path1 = V[:]
        random.shuffle(path1)
        for _ in range(100):  # Try multiple shuffles for path2
            path2 = V[:]
            random.shuffle(path2)
            common = count_common_adj_nodes(path1, path2)
            if common == common_edges_target:
                test_cases.append((path1[:], path2[:]))
                break
    return test_cases


# Parameters
V = list(range(1, 11))
x = 5
num_cases = 12

# Generate and print test cases
cases = generate_hamiltonian_paths(V, x, num_cases)
for i, (p1, p2) in enumerate(cases, 1):
    print(f"Case {i}:")
    print(f"path1: {p1}")
    print(f"path2: {p2}")
    print()
