from ILP_Formula import create_ilp_formula
from View_Solution import plot_solution
from Data_Receiver import save_result
import time

if __name__ == "__main__":
    # Beispielwerte:
    x_size = 5
    y_size = 5
    V = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    path1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    path2 = [1, 3, 5, 6, 4, 7, 9, 8, 10, 2]
    start_time = time.time()
    model, assign, flow, edges, gridEdges, D, objective_value = create_ilp_formula(x_size, y_size, V, path1, path2)
    end_time = time.time()
    duration = end_time - start_time
    save_result(model, V, path1, path2, assign, edges, x_size, y_size, gridEdges, objective_value, flow, D, duration, filename="results.txt")
    plot_solution(D, assign, flow, gridEdges, edges, V)
