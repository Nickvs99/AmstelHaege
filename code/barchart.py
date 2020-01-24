"""
Creates a barchart for the results
"""

import matplotlib.pyplot as plt
import numpy as np

def plot_barchart():
    
    neighbourhoods = ["Wijk 1", "Wijk 2", "Wijk 3"]
    houses = [20,40,60]

    # Initialize dictionary, with the following structure
    # dict = {
    #   Wijk 1: {
    #       20: {}
    #       40: {}
    #       ...
    #   },
    #   Wijk 2: {
    #       20: {}
    #       40: {}
    #       ...
    #   }
    #   ...
    # }
    results = {}
    for neighbourhood in neighbourhoods:
        for house in houses:

            if neighbourhood not in results:
                results[neighbourhood] = {}

            if house not in results[neighbourhood]:
                results[neighbourhood][house] = {}
            
    # Add data to results dict
    with open("Results/Results.csv") as f:
        
        first_line = True

        for row in f:
            if first_line:
                first_line = False
                continue

            data_split = row.strip("\n").split(",")

            algorithm = data_split[0]
            neighbourhood = data_split[1]
            houses = int(data_split[2])
            worth = int(data_split[4])
            stddev = float(data_split[6])
            
        
            results[neighbourhood][houses][algorithm] =  [worth, stddev]

    # Plot all charts
    plot_counter = 1
    for neighbourhood in results.keys():
        for house in results[neighbourhood].keys():
            
            algorithms = list(results[neighbourhood][house].keys())
            worths = []
            stddevs = []
            for worth, stddev in results[neighbourhood][house].values():
                worths.append(worth)
                stddevs.append(stddev)

            x_pos = np.arange(len(algorithms))
            plt.subplot(3, 3, plot_counter)
            plt.tight_layout()
            fig, ax = plt.gcf(), plt.gca()
            plt.title(f"{neighbourhood}, {house} houses")
            ax.set_xticks(x_pos)
            ax.set_xticklabels(algorithms)
            ax.yaxis.grid(True)
            ax.set_ylim(get_min_y(worths), get_max_y(worths))
            plt.bar(x_pos, worths, yerr = stddevs, alpha=0.5,  ecolor='black', capsize=10)

            plot_counter += 1
    plt.show()

def get_min_y(worths):
    """ Returns the minimum y value for the plot. """
    
    return min(worths) - 1000000

def get_max_y(worths):
    """ Returns the maximum y value for the plot. """

    return max(worths) + 1000000

if __name__ == "__main__":
    plot_barchart()