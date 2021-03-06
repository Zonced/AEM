import time

from Algorithms.lab2_new import run_algorithm_greedy, run_algorithm_steepest, random_groups, cost_function
from Utilities.DataPreprocess import parse_data, create_dist_function, create_clusters_from_tree
from Utilities.Plot import draw_scatter
from Lab1 import create_n_trees_kruskal, create_n_trees_prim


import numpy as np


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


def run_measurements(data, dist_matrix, neighbourhood_radius, steps_for_time_measurements=50, option="prim"):
    greedy_times_measurements = []
    steepest_times_measurements = []
    greedy_measurements = []
    steepest_measurements = []
    dist = np.copy(dist_matrix)
    best_greedy = 10000
    best_clusters_greedy = []
    best_steepest = 10000
    best_clusters_steepest = []
    costs_greedy = []
    costs_steepest = []
    clusters_before_greedy = []
    clusters_before_steepest = []

    for i in range(steps_for_time_measurements):
        clusters = np.ones(len(data), dtype=np.int32) * (-1)

        if option == "prim":
            result = create_n_trees_prim(data, dist_matrix, 20, 1)
            clusters = create_clusters_from_tree(data, result)
        elif option == "kruskal":
            result = create_n_trees_kruskal(data, dist_matrix, 20, 1)
            clusters = create_clusters_from_tree(data, result)
        elif option == "random":
            clusters = random_groups(data.shape[0])

        greedy_clusters = np.copy(clusters)
        steepest_clusters = np.copy(clusters)

        measurement = time_measure(run_algorithm_greedy, (greedy_clusters, dist, neighbourhood_radius))
        greedy_times_measurements.append(measurement)
        greedy_cost = cost_function(dist_matrix, greedy_clusters)[0]
        greedy_measurements.append(greedy_cost)
        costs_greedy.append(greedy_cost)
        if greedy_cost < best_greedy:
            best_greedy = greedy_cost
            best_clusters_greedy = greedy_clusters
            clusters_before_greedy = clusters

        measurement = time_measure(run_algorithm_steepest, (steepest_clusters, dist, neighbourhood_radius))
        steepest_times_measurements.append(measurement)
        steepest_cost = cost_function(dist_matrix, steepest_clusters)[0]
        steepest_measurements.append(steepest_cost)
        costs_steepest.append(steepest_cost)
        if steepest_cost < best_steepest:
            best_steepest = steepest_cost
            best_clusters_steepest = steepest_clusters
            clusters_before_steepest = clusters

    print(f"Greedy cost min:{min(greedy_measurements)}, max:{max(greedy_measurements)}, avg: {sum(greedy_measurements) / len(greedy_measurements)}")
    print(f"Greedy Time min:{min(greedy_times_measurements)}, max:{max(greedy_times_measurements)}, avg: {sum(greedy_times_measurements) / len(greedy_times_measurements)}")

    print(f"Steepest cost min:{min(steepest_measurements)}, max:{max(steepest_measurements)}, avg: {sum(steepest_measurements) / len(steepest_measurements)}")
    print(f"Steepest Time min:{min(steepest_times_measurements)}, max:{max(steepest_times_measurements)}, avg: {sum(steepest_times_measurements) / len(steepest_times_measurements)}")

    draw_scatter(data, best_clusters_greedy, True)
    draw_scatter(data, best_clusters_steepest, True)
    draw_scatter(data, clusters_before_greedy, False)
    draw_scatter(data, clusters_before_steepest, False)


def run():
    neighbourhood = 50  # radius of neighbourhood
    data = parse_data("data/objects20_06.data")
    dist_matrix = create_dist_function(data, lambda x1, x2: np.linalg.norm(x1 - x2))
    print("Prim")
    run_measurements(data, dist_matrix, neighbourhood, 100, "prim")
    print("Kruskal")
    run_measurements(data, dist_matrix, neighbourhood, 100, "kruskal")
    print("Random")
    run_measurements(data, dist_matrix, neighbourhood, 100, "random",)


if "__main__" == __name__:
    run()
