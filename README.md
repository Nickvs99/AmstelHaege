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
The code was written in [Python 3.7.3](https://www.python.org/downloads/). The necessary plugin to successfully run this code can be found in requirements.txt

### Running the algorithm
There are two files which can run algorithms. 

The first is the main file, This can run one algorithm for starting the algorithm and then a hillclimber. After running a plot will appear of the area after running the algorithms with the best score.

The best_result.py can run multiple iterations of algorithms. This works the same way as the main.py. This will also give the best score, average score and average time of one iteration of the area's

There are a couple of variables to set before running the files. These's variables are defined at the top of the files. beneath you will find the name, properties and valid input of the variables

Houses: The amount of houses placed in the area.
* 20
* 40
* 60

Neighbourhood: Selects the configuration of the area.
* wijk1
* wijk2
* wijk3

ALGORITHM: Selects the algorithm to make the place houses.
* random: places houses random
* greedy: Tries to place the houses one by one on every place and picks the best spot
* greedy_random: Tries to place the houses one by one a 100 times and picks the best spot
* evolution:

HILLCLIMBER: Selects a algorithm to hillclimb on a algorithm run by ALGORITHM variable


