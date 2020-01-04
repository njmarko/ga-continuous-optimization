from src.model.population2 import Population

ga_function = None


def ga(fnc, axis=2, options=None):
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
        "mutate_fraction": 0.8,
        "elitism": 0.2
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
    mutate_fraction = opt["mutate_fraction"]
    elitism = opt["elitism"]
    intermediate_offset = opt["intermediate_offset"]

    average = []
    best = []

    if opt["find_max"] == 1:
        global ga_function
        ga_function = fnc
        fnc = invert_function

    pop = Population(pop_size, axis, lower_bound, upper_bound, fnc)
    if options["prints"] == 1:
        print(pop)

    stop = False
    for i in range(max_iter):
        best.append(pop.get_min())

        if opt["average_result"] is not None:
            average.append(pop.get_average())
            if average[-1] < opt["average_result"]:
                if opt["prints"] == 1:
                    print("Terminated in " + str(i) + ". iteration. Found average result.")

                stop = True
                break

        if opt["best_result"] is not None:
            if best[-1] < opt["best_result"]:
                if opt["prints"] == 1:
                    print("Terminated in " + str(i) + ". iteration. Found required result.")

                stop = True
                break

        if opt["similarity"] is not None:
            if similarity_check(best, opt["similarity"]):
                if opt["prints"] == 1:
                    print("Terminated in " + str(i) + ". iteration. Similar results.")
                stop = True
                break

        pop.selection(selection, elitism)
        pop.pairing(pairing, crossover_fraction, crossover, intermediate_offset=intermediate_offset)
        pop.mutations(mutation)
        pop = pop.finalize()
        # pop = pop.selection(selection, elitism)
        # pop.pairing(pairing, crossover_fraction, crossover, elitism)
        # pop.mutations(mutate_fraction, mutation, elitism)

        if opt["prints"] == 1:
            print(pop)

    result = pop.get_individuals()[0]
    if opt["prints"] == 1:
        if not stop:
            print("End of iterations")
        print("\nResult:")
        print(result)

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
