import pandas as pd
import numpy as np
import os
import random

def EvoluationarySearch(inputFile, budget):
    df = pd.read_csv(inputFile)
    labels = df.columns[:-1]
    performanceColumn = df.columns[-1]
    minList = []
    maxList = []

    # Sort out the maximum and minimum of the columns
    for i in range(len(labels)):
        minList.append(df[labels[i]].min())
        maxList.append(df[labels[i]].max())

    # Determine if we are looking at a maximisation or minimisation problem
    name = os.path.basename(inputFile).split('.')[0]
    if name.lower() == "---":
        max = True
        worstFitness = df[performanceColumn].min() / 2
    else:
        max = False
        worstFitness = df[performanceColumn].max() * 2

    # Hyperparameter of the size of the population set here.
    # Generations depends on popSize and budget to allow a fair comparison
    # between Random search baseline and this evolutionary approach
    popSize = 8
    numberOfOffspring = popSize / 2
    pop = []
    fitness = []
    generations = int(((budget-popSize) // numberOfOffspring))

    # Generate Initial Population - pseudo-random approach
    choiceList = np.array_split(list(range(8)) * len(labels), len(labels))
    values = [[]] * len(labels)
    intervals = [0] * len(labels)
    for i in range(popSize):
        while True:
            config = []
            reset = choiceList.copy()
            for j in range(len(labels)):
                if i == 0:
                    values[j] = df[labels[j]].unique()
                    intervals[j] = (maxList[j]-minList[j])/popSize
                
                choice = random.choice(choiceList[j])

                valChoice = (random.uniform((minList[j] + intervals[j]*choice), (minList[j] + (intervals[j]+1)*choice)))

                option = min(values[j], key=lambda x:abs(x-valChoice))

                choiceList[j] = np.delete(choiceList[j], np.where(choiceList[j] == choice))
                config.append(int(option))
                
            if config not in pop:
                choiceList[j] = np.delete(choiceList[j], np.where(choiceList[j] == choice))
                break
            else:
                # If already inside population we reset 
                choiceList = reset

        # Check fitness of each configuration
        for x in df.itertuples():
            eq = True
            for j in range(0, len(config)):
                if x[j+1] != config[j]:
                    eq = False
                    break
            if eq:
                fitness.append(x[len(x)-1])
                break
        if not eq:
            fitness.append(worstFitness)
        pop.append(config)

    # Sort the population based on fitness and whether we are trying to
    # maximise or minimise the performance metric
    if not max:
        fitness, pop = zip(*sorted(zip(fitness, pop), key=lambda x: x[0]))
    else:
        fitness, pop = zip(*sorted(zip(fitness, pop), key=lambda x: x[0], reverse=True))
    bestConfig = pop[0]
    bestPerform = fitness[0]

    # Set up for the EA loop
    crossoverProb = 0.85
    mutationProb = 1/len(labels)
    for _ in range(generations):
        parentOrder = list(range(popSize))
        random.shuffle(parentOrder)
        parents = []

        # Tournament selection for parents based on order as 
        # population is sorted
        for i in range(0, len(parentOrder), 2):
            if parentOrder[i] < parentOrder[i+1]:
                parents.append(parentOrder[i])
            else: 
                parents.append(parentOrder[i+1])

        # Crossover - uniform
        offspring = []
        for i in range(0, len(parents), 2):
            parent1 = pop[parents[i]].copy()
            parent2 = pop[parents[i+1]].copy()
            if random.random() < crossoverProb:
                offspring1 = []
                offspring2 = []
                for j in range(len(parent1)):
                    if (random.random() < 0.5):
                        offspring1.append(parent1[j])
                        offspring2.append(parent2[j])
                    else:
                        offspring2.append(parent1[j])
                        offspring1.append(parent2[j])
                offspring.append(offspring1)
                offspring.append(offspring2)
            else:
                offspring.append(parent1)
                offspring.append(parent2)

        # Mutation - Uniform
        for i in range(len(offspring)):
            offs = offspring[i]
            for j in range(0,len(offs)):
                if random.random() < mutationProb:
                    change = offs[j]
                    while change == offs[j]:
                        change = (int(np.random.choice(df[labels[j]].unique())))
                    offs[j] = change
        
        # Add together offspring and old population, remove worst performance congigs
        # and if best config beats best performance, it is best performance
        pop = list(pop)
        fitness = list(fitness)
        pop += offspring

        popDict = [pop[0].copy()]
        fitnessDict = [fitness[0]]
        for i in range(1, len(pop)):
            # Here check if configaurtion already seen in the population/offspring
            if pop[i] in popDict:
                continue
            else:
                # if not already seen, check its performance
                popDict.append(pop[i].copy())
                if i>=popSize:
                    config = pop[i].copy()
                    for x in df.itertuples():
                        eq = True
                        for j in range(0, len(config)):
                            if x[j+1] != config[j]:
                                eq = False
                                break
                        if eq:
                            fitnessDict.append(x[len(x)-1])
                            break
                    if not eq:
                        fitnessDict.append(worstFitness)
                else:
                    fitnessDict.append(fitness[i])

            if len(popDict) < popSize:
                # if the population is now below the set size, we randomly 
                # generate new configurations and join them to the population
                config = []
                for j in range(len(labels)):
                    config.append(int(np.random.choice(df[labels[j]].unique())))
                
                for x in df.itertuples():
                    eq = True
                    for j in range(0, len(config)):
                        if x[j+1] != config[j]:
                            eq = False
                            break
                    if eq:
                        fitnessDict.append(x[len(x)-1])
                        break
                if not eq:
                    fitnessDict.append(worstFitness)
                popDict.append(config)

        pop = popDict
        fitness = fitnessDict

        if not max:
            fitness, pop = zip(*sorted(zip(fitness, pop), key=lambda x: x[0]))
            if fitness[0] < bestPerform:
                bestPerform = fitness[0]
                bestConfig = pop[0]
        else:
            fitness, pop = zip(*sorted(zip(fitness, pop), key=lambda x: x[0], reverse=True))
            if fitness[0] > bestPerform:
                bestPerform = fitness[0]
                bestConfig = pop[0]


        fitness = fitness[0:popSize]
        pop = pop[0:popSize]
 
    return bestConfig, bestPerform

def main():
    datasets_folder = "datasets"
    budget = 100

    results = {}
    for file_name in os.listdir(datasets_folder):
        if file_name.endswith("Apache.csv"):
            file_path = os.path.join(datasets_folder, file_name)
            best_solution, best_performance = EvoluationarySearch(file_path, budget)
            results[file_name] = {
                "Best Solution": best_solution,
                "Best Performance": best_performance
            }

    # Print the results
    for system, result in results.items():
        print(f"System: {system}")
        print(f"  Best Solution:    [{', '.join(map(str, result['Best Solution']))}]")
        print(f"  Best Performance: {result['Best Performance']}")

if __name__ == "__main__":
    main()
