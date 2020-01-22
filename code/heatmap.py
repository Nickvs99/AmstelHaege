""" 
Creates an heatmap

Used for visualising the SA variables.

"""

import numpy as np
import matplotlib.pyplot as plt

with open("SA-output/evolution3.csv") as f:

    alphas = []
    betas = []
    generations = {}
    max_values = {}

    first_line = True
    for line in f:

        if first_line:
            first_line = False
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
    

    plt.subplot(121)
    plt.title("worths")
    plt.xlabel("beta-values")
    plt.ylabel("alpha-values")
    plt.contourf(betas,alphas , worths_list2d)
    plt.colorbar()

    plt.subplot(122)
    plt.title("generations")
    plt.xlabel("beta-values")
    plt.ylabel("alpha-values")
    plt.contourf(betas,alphas , generations_list2d)
    plt.colorbar()
    
    plt.show()



