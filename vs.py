from lab3solution import random_search
from main import EvoluationarySearch
import pandas as pd
import os
import scipy
import matplotlib.pyplot as plt

def main():
    datasets_folder = "datasets"
    output_folder = "search_results"
    os.makedirs(output_folder, exist_ok=True)
    budget = 100
    results = {}
    for file_name in os.listdir(datasets_folder):
        if file_name.endswith(".csv"):
            baselinetotal = 0
            evototal = 0
            file_path = os.path.join(datasets_folder, file_name)
            evoList = []
            baselineList = []
            testNum = 30
            for i in range(testNum):
                baseline_solution, baseline_performance = random_search(file_path, budget)
                evo_solution, evo_performance = EvoluationarySearch(file_path, budget)
                baselinetotal += baseline_performance
                evototal += evo_performance
                evoList.append(evo_performance)
                baselineList.append(baseline_performance)

            evoList.sort()
            baselineList.sort()

            output_image = os.path.join("boxPlotFolder", f"{file_name}_visualization.png")
            plt.boxplot([evoList, baselineList], labels=["evolutionary", "baseline"])
            plt.legend()
            os.makedirs("boxPlotFolder", exist_ok=True)
            plt.savefig(output_image)
            plt.show()

            levelOfConfidence = 0.05
            statistic, pvalue = scipy.stats.ranksums(evoList, baselineList)
            if (pvalue <= levelOfConfidence):
                reject = "yes"
            else:
                reject = "no"

            
            results[file_name] = {
                "median evo solution":  evoList[round((testNum + 1)/2)],
                "median baseline solution": baselineList[round((testNum + 1)/2)],
                "1st quartile evo": evoList[round((testNum + 1)/4)],
                "1st quartile baseline": baselineList[round((testNum + 1)/4)],
                "3rd quartile evo": evoList[3 * round((testNum + 1)/4)],
                "3rd quartile baseline": baselineList[3 * round((testNum + 1)/4)],
                "p-value": pvalue,
                "reject H0": (pvalue <= levelOfConfidence)
            }

    for system, result in results.items():
        print(f"System: {system}")
        print(f"  Median evo solution: {result['median evo solution']}")
        print(f"  Median baseline solution: {result['median baseline solution']}")
        print(f"  1st quartile evo solution: {result['1st quartile evo']}")
        print(f"  1st quartile basline solution: {result['1st quartile baseline']}")
        print(f"  3rd  quartile evo solution: {result['3rd quartile evo']}")
        print(f"  3rd quartile baseline solution: {result['3rd quartile baseline']}")
        print(f"  P-value: {result['p-value']}")
        print(f"  Do we reject H0: {reject}")

if __name__ == "__main__":
    main()