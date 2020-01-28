""" 
Creates an heatmap from the data in SA-output

Used for visualising the results for different cooling functions from evolution.
"""

import numpy as np
import matplotlib.pyplot as plt
import os

for filename in os.listdir("SA-output"):

    with open(f"SA-output/{filename}") as f:

        # Get the data from the csv file
        alphas = []
        betas = []
        generations = {}
        max_values = {}
        first_line = True
        for line in f:

            if first_line:
                first_line = False
                cooling_function = line
                continue

            data_line = line.split(",")

            alpha = float(data_line[0])
            beta = float(data_line[1])
            generation = float(data_line[2])
            max_value = float(data_line[3])

            if alpha not in generations:
                generations[alpha] = {}
                max_values[alpha] = {}

            generations[alpha][beta] = generation
            max_values[alpha][beta] = max_value

        # Parse the data from the dictionary to the list
        # Now every data point will be in the same order
        generations_list2d = []
        worths_list2d = []
        alphas = []
        betas = []
        for alpha in generations.keys():
            row1 = []
            row2 = []
            for beta in generations[alpha].keys():
                row1.append(generations[alpha][beta])
                row2.append(max_values[alpha][beta])

                if beta not in betas:
                    betas.append(beta)

            if alpha not in alphas:
                alphas.append(alpha)

            generations_list2d.append(row1)
            worths_list2d.append(row2)
        
        # Plot heatmaps
        plt.subplot(121)
        plt.title("Area worth")
        plt.xlabel("beta-values")
        plt.ylabel("alpha-values")
        plt.contourf(betas,alphas , worths_list2d)
        plt.colorbar()

        plt.subplot(122)
        plt.title("Generations")
        plt.xlabel("beta-values")
        plt.ylabel("alpha-values")
        plt.contourf(betas,alphas , generations_list2d)
        plt.colorbar()
        
        plt.suptitle(f"Cooling function: {cooling_function}")

        plt.show()



