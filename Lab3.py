import time
import numpy as np
from Utilities.DataPreprocess import parse_data, create_dist_function, create_clusters_from_tree
from Utilities.Plot import draw_scatter
from Algorithms.lab3 import random_groups, run_algorithm, count_costs
from Lab1 import create_n_trees_kruskal, create_n_trees_prim



def time_measure(func, args_for_func):
    """
    :param func:
    :param args_for_func:
    :return: time in seconds
    """
    start = time.time()
    func(*args_for_func)
    end = time.time()
    return end - start


def run_measurements(data, dist_matrix, neighbourhood, steps_for_time_measurements=1, method="none"):
    dist_1 = np.copy(dist_matrix)
    costs_greedy = []
    times_measurements = []
    best_cost = 1000
    best_clusters = []
    clusters = None
    # draw_scatter(data, clusters, False)
    np.random.seed(0)
    for i in range(steps_for_time_measurements):
        clusters = random_groups(data.shape[0])
        measurement = time_measure(run_algorithm, (clusters, dist_1, neighbourhood, method))
        times_measurements.append(measurement)
        cost = sum(count_costs(clusters, dist_1, 20))/20
        # print("Koszt dla iteracji " + str(i) + ": " + str(cost))
        if cost < best_cost:
            best_cost = cost
            best_clusters = clusters
        costs_greedy.append(cost)
        # draw_scatter(data, clusters, True)

    print(f"Najmniejszy koszt dla lokalnego przeszukiwania w wersji stromej ({method})  wynosi {min(costs_greedy)}, "
          f"największy {max(costs_greedy)}, średni {sum(costs_greedy)/len(costs_greedy)}.")
    print(f"Pomiary czasu dla {steps_for_time_measurements} kroków dla algorytmu stromej to "
          f"min: {min(times_measurements)} sekund, max: {max(times_measurements)} sekund i "
          f"avg: {sum(times_measurements) / len(times_measurements)} sekund.\n")
    draw_scatter(data, best_clusters, True)


def run():
    neighbourhood = 50  #radius of neighbourhood
    data = parse_data("data/objects20_06.data")
    dist_matrix = create_dist_function(data, lambda x1, x2: np.linalg.norm(x1 - x2))
    run_measurements(data, dist_matrix, neighbourhood, 1, method="none")
    run_measurements(data, dist_matrix, neighbourhood, 1, method="cache")
    run_measurements(data, dist_matrix, neighbourhood, 1, method="candidates")
    run_measurements(data, dist_matrix, neighbourhood, 1, method="candidates_with_cache")


if "__main__" == __name__:
    run()
