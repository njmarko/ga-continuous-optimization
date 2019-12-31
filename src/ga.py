from src.model.population import Population

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
        "similarity": 50
    }
    opt.update(options)
    pop_size = opt["pop_size"]
    max_iter = opt["max_iter"]
    lower_bound = opt["lower_bound"]
    upper_bound = opt["upper_bound"]

    average = []
    best = []

    if opt["find_max"] is 1:
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
                print("Terminated in " + str(i) + ". iteration. Found average result.")

                stop = True
                break

        if opt["best_result"] is not None:
            if best[-1] < opt["best_result"]:
                print("Terminated in " + str(i) + ". iteration. Found required result.")

                stop = True
                break

        if opt["similarity"] is not None:
            if similarity_check(best, opt["similarity"]):
                print("Terminated in " + str(i) + ". iteration. Similar results.")
                stop = True
                break

        pop = pop.selection()
        pop.pairing()
        pop.mutations()

        if opt["prints"] == 1:
            print(pop)

    if not stop:
        print("End of iterations")

    result = pop.get_individuals()[0]
    print("\nResult:")
    print(result)


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
