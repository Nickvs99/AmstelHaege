# AmstelHaege

## Made by Nick van Santen, Hidde van Oijen en Pranto Bishas - Team Simcity


### The case
Amstelhaege is a new residetial area that needs a lay-out. The objective is to get a so high as possible worth for the whole area. The size of the area is 160 x 180 meters. The area has places with water. The water in the area has three configurations. There are three types of houses. Each with a different size, worth and mandatory free space. For every extra meter of free space a percentage of the worth of the house is added to the worth of the house. The free space stops if it hits another house. The free space is not effected by the border of the area or water.

| Houses        | Size            | Mandatory free space  | Worth         | Extra worth for extra meter free space |
| ------------- |-----------------|-----------------------|---------------|----------------------------------------|
| Family house  | 8 x 8 meter     | 2 meter               | € 285.000,-   | 3%                                     |
| Bungalow      | 11 x 7 meter    | 3 meter               | € 399.000,-   | 4%                                     |
| Mansion       | 12 x 10 meter   | 6 meter               | € 610.000,-   | 6%                                     |

#### Area:
* Wijk 1:

![alt text](https://github.com/Nickvs99/AmstelHaege/blob/master/Images/Wijk1.png "Wijk 1")

* Wijk 2:

![alt text](https://github.com/Nickvs99/AmstelHaege/blob/master/Images/Wijk2.png "Wijk 2")

* Wijk 3:

![alt text](https://github.com/Nickvs99/AmstelHaege/blob/master/Images/Wijk3.png "Wijk 3")
### Requirements:
The code was written in [Python 3.7.3](https://www.python.org/downloads/). The necessary plugin to successfully run this code can be found in requirements.txt. The plugins can be installed by running the following command in the main folder. 
```
pip install -r requirements.txt
```

### Running the algorithm
The code can be runned by running: 
```
python code/main.py
```

When the code is runned the code asks for user input. First it ask for which neighbourhood you want to use.
The user can choose between:
* wijk1
* wijk2
* wijk3

When done the code asks for how many houses the user wants to place. Here the user needs to input a digit.

After the code asks for a algorithm that places houses.
The algorithms to choose from are explained beneath.
* random: places houses random
* greedy: Loops over all possible coordinates. It picks the coordinate which adds the most value to the area. Repeat for all houses.
* greedy_random: Tries to place the houses one by one a n times and picks the best spot.
* evolution: Select the best-fit individuals for reproduction based on their fitness value. Breed new individuals through mutations to give birth to offspring. Evaluate the individual fitness of new individuals. Replace least-fit population with new individuals.

After this the code asks for default or custom settings.
* Default setting: can be found in code/settings.
* Custom settings: The code asks for a parameter. The user then needs to input a value for that parameter.

Now the code asks for a alogrithm that should improve on the obtained area.
The algorithms are:
* hillclimber_random: tries every house an x amount of times on different coordinates and places it in the best position. It does that until no further improvements are found.
* hillclimber_random_random: tries to place a random house on a random location and places it when it scores better. It does this an x amount of times.
* hillclimber_steps: Checks for x meters in every direction for each house and places the house in the best location. Ideal for fine-tuning the solution.
* simulated_annealing: Tries to place a random house on a random location for an x amount of times. If better it places the house. If not it places the house by chance. The chance decreases over the amount of iterations.

After this, the program will once again ask for default or custom settings.


