from ILP_Formula import create_ilp_formula
from View_Solution import plot_solution
from Data_Receiver import save_result

if __name__ == "__main__":
    # Beispielwerte:
    x_size = 5
    y_size = 4
    V = [1, 2, 3, 4, 5, 6]
    path1 = [1, 2, 4, 6]
    path2 = [1, 3, 5, 6]

    model, assign, flow, edges, gridEdges, D, objective_value = create_ilp_formula(x_size, y_size, V, path1, path2)
    # save_result(V, path1, path2, assign, edges, x_size, y_size, gridEdges, objective_value, flow, D, filename="results.txt")
    plot_solution(D, assign, flow, gridEdges, edges, V)
