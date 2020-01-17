from src.model.population2 import Population
from matplotlib import pyplot
ga_function = None


def ga(fnc, axis=2, options=None, callback=None):
    if options is None:
        options = {}
    opt = {
        "pop_size": 100,
        "max_iter": 100,
        "lower_bound": -10,
        "upper_bound": 10,
        "find_max": 0,
        "prints": 1,
        "average_result": None,
        "best_result": None,
        "similarity": 50,
        "selection": "Roulette Wheel",
        "pairing": "Fittest",
        "crossover": "Two point",
        "crossover_fraction": 0.8,
        "intermediate_offset": 1,
        "mutation": "Gauss",
        "mutation_intensity": 0.8,
        "mutation_intensity_final": 0.01,
        "elitism": 0.2,
        "fitness_remapping": "Rank Scaling"
    }
    opt.update(options)
    pop_size = opt["pop_size"]
    max_iter = opt["max_iter"]
    lower_bound = opt["lower_bound"]
    upper_bound = opt["upper_bound"]
    selection = opt["selection"]
    pairing = opt["pairing"]
    crossover = opt["crossover"]
    crossover_fraction = opt["crossover_fraction"]
    mutation = opt["mutation"]
    mutate_intensity_initial = opt["mutation_intensity"]
    mutate_intensity_final = opt["mutation_intensity_final"]
    elitism = opt["elitism"]
    intermediate_offset = opt["intermediate_offset"]
    fitness_remapping = opt["fitness_remapping"]

    average = []
    best = []
    comment = "End of iterations"  # Default comment if not overridden

    # Inverting parameters for fining max
    if opt["find_max"] == 1:
        global ga_function
        ga_function = fnc
        fnc = invert_function
        if opt["best_result"]:
            opt["best_result"] *= -1
        if opt["average_result"]:
            opt["average_result"] *= -1

    # Initial Population
    pop = Population(pop_size, axis, lower_bound, upper_bound, fnc)
    if options["prints"] == 1:
        print(pop)
    best_results = []
    stop = False
    for i in range(max_iter):
        best.append(pop.get_min())

        if opt["average_result"] is not None:
            average.append(pop.get_average())
            if average[-1] < opt["average_result"]:
                comment = "Terminated in " + str(i + 1) + ". iteration. Found average result."
                stop = True
                break

        if opt["best_result"] is not None:
            if best[-1] < opt["best_result"]:
                comment = "Terminated in " + str(i + 1) + ". iteration. Found required result."
                stop = True
                break

        if opt["similarity"] is not None:
            if similarity_check(best, opt["similarity"]):
                comment = "Terminated in " + str(i) + ". iteration. Similar results."
                stop = True
                break

        mutate_intensity = scaled_value(mutate_intensity_initial, mutate_intensity_final, i, max_iter - 1)
        pop.selection(selection, elitism, fitness_remapping=fitness_remapping)
        pop.pairing(pairing, crossover_fraction, crossover, intermediate_offset=intermediate_offset,
                    fitness_remapping=fitness_remapping)
        pop.mutations(mutation, mutate_intensity=mutate_intensity)
        pop = pop.finalize()
        best_results.append(pop.get_individuals()[0].get_fitness())
        if callback:
            percentage = i / max_iter * 100
            callback.update_progress_bar(i, percentage + 1)
            if ((i + 1) % 5) == 0:
                callback.add_console_iter(i + 1, pop, opt["find_max"])

        if opt["prints"] == 1:
            print(pop)
    # END OF ITERATIONS

    result = pop.get_individuals()[0]

    if opt["prints"] == 1:
        print(comment)
        print("\nResult:")
        print(result)

    if callback:
        callback.set_comment(comment)
        callback.print_result(result, opt["find_max"])
    x = [i for i in range(len(best_results))]
    pyplot.plot(x,best_results)
    pyplot.show()
    return result


def invert_function(axis):
    global ga_function
    return -ga_function(axis)


def similarity_check(subject, criteria):
    similarity = 0
    for i in range(len(subject) - 2, 0, -1):
        if subject[i] != subject[i + 1]:
            return False

        similarity += 1
        if similarity >= criteria:
            return True

    return False


def scaled_value(a, b, it, last):
    return a + ((b - a) * (it / last))
