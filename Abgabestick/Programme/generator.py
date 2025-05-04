# Generiere zufällige Testfälle mit n Knoten
import random


def generate_test_cases(num_cases=10):
    scenarios = []

    for _ in range(num_cases):
        # Knoten von 1 bis 5
        V = [1, 2, 3, 4, 5]
        # Zwei zufällige Permutationen von V für path1 und path2
        path1 = random.sample(V, len(V))
        path2 = random.sample(V, len(V))

        # Füge Szenario zur Liste hinzu
        scenarios.append({
            "x_size": 3,
            "y_size": 3,
            "V": V,
            "path1": path1,
            "path2": path2
        })

    return scenarios


# Generiere die Testfälle
test_cases = generate_test_cases(10)

for test_case in test_cases:
    print(str(test_case) + ',')
