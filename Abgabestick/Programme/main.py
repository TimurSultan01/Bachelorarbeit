# Beispielaufruf
from ILP_Formula import create_ilp_formula
from View_Solution import plot_solution
from Data_Receiver import save_result
import time

if __name__ == "__main__":
    # Beispielwerte
    x_size = 4
    y_size = 4
    V = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    path1 = [3, 10, 6, 7, 5, 4, 8, 1, 2, 9]
    path2 = [4, 5, 7, 9, 3, 6, 2, 8, 1, 10]
    start_time = time.time()
    model, assign, flow, edges, gridEdges, D, obj = create_ilp_formula(x_size, y_size, V, path1, path2)
    end_time = time.time()
    duration = end_time - start_time
    save_result(model, V, path1, path2, assign, edges, x_size, y_size, gridEdges, obj,
                flow, D, duration, filename="result.txt")
    plot_solution(D, assign, flow, gridEdges, edges, V)
