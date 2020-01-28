# AmstelHaege

## Made by Nick van Santen, Hidde van Oijen en Pranto Bishas - Team Simcity


### The case
Amstelhaege is a new residetial area that needs a lay-out. The objective is to get a so high as possible worth for the whole area. The size of the Area is 160 x 180 meters. The area has places with water. The water in the area has three configurations. There are three types of houses. Each with a different size, worth and mandatory free space. For every extra meter free space a percentage of the worth of the house is added to the worth of the house. The free space stops if it hits another house. The free space is not effected by the border of the area or water.

| Houses        | Size            | Mandatory free space  | Worth         | Extra worth for extra meter free space |
| ------------- |-----------------|-----------------------|---------------|----------------------------------------|
| Family house  | 8 x 8 meter     | 2 meter               | € 285.000,-   | 3%                                     |
| Bungalow      | 11 x 7 meter    | 3 meter               | € 399.000,-   | 4%                                     |
| Mansion       | 12 x 10 meter   | 6 meter               | € 610.000,-   | 6%                                     |

#### Area:

### Requirements:
The code was written in [Python 3.7.3](https://www.python.org/downloads/). The necessary plugin to successfully run this code can be found in requirements.txt. The plugins can be installed by running pip install -r requirements.txt in the main folder.

### Running the algorithm
The code can be runned by running main.py in the code file. 

When the code is runned the code asks for user input. First it ask for which neighbourhood you want to use.
The user can choose between:
* wijk1
* wijk2
* wijk3

When done the code asks for how many houses the user wants to place. Here the user needs to input a digit.

After the code asks for a algorithm that places houses.
The algorithms to choose from are explained beneath.
* random: places houses random
* greedy: Tries to place the houses one by one on every place and picks the best spot
* greedy_random: Tries to place the houses one by one a 100 times and picks the best spot
* evolution: Select the best-fit individuals for reproduction based on their fitness value. Breed new individuals through mutations to give birth to offspring. Evaluate the individual fitness of new individuals. Replace least-fit population with new individuals.

After this the code asks for default or custom settings.

Now the code asks for a alogrithm that replaces/turns the houses to create better values.
The algorithms are explained beneath.
* hillclimber_random: tries every house an x amount of times and places it in the best position. It does that until no further improvement
* hillclimber_random_random: tries to place a random house on a random location and places it when it scores better. It does this an x amount of times.
* hillclimber_steps: Checks the x amount of meter in every direction for each house and places the house in the best location.
* simulated_annealing: Tries to place a random house on a random location for an x amount of times. If better it places the house. If not it places the house by chance. The chance decreases over the amount of iterations.

After this the code asks for default or custom settings.
* Default setting: can be found in settings.
* Custom settings: The code asks for a parameter. The user then needs to input a value for that parameter.


