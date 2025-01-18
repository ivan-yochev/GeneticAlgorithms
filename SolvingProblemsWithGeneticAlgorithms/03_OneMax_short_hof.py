from deap import base
from deap import creator
from deap import tools
from deap import algorithms

import random
import numpy

import matplotlib.pyplot as plt
import seaborn as sns

# problem constants:
ONE_MAX_LENGTH = 100  # length of bit string to be optimized

# Genetic Algorithm constants:
POPULATION_SIZE = 200
P_CROSSOVER = 0.9  # probability for crossover
P_MUTATION = 0.1   # probability for mutating an individual
MAX_GENERATIONS = 50
HALL_OF_FAME_SIZE = 10


# set the random seed:
RANDOM_SEED = 42
random.seed(RANDOM_SEED)

toolbox = base.Toolbox()

# create an operator that randomly returns 0 or 1:
toolbox.register("zeroOrOne", random.randint, 0, 1)

# define a single objective, maximizing fitness strategy:
creator.create("FitnessMax", base.Fitness, weights=(1.0,))

# create the Individual class based on list:
creator.create("Individual", list, fitness=creator.FitnessMax)

# create the individual operator to fill up an Individual instance:
toolbox.register("individualCreator", tools.initRepeat, creator.Individual, toolbox.zeroOrOne, ONE_MAX_LENGTH)

# create the population operator to generate a list of individuals:
toolbox.register("populationCreator", tools.initRepeat, list, toolbox.individualCreator)


# fitness calculation:
# compute the number of '1's in the individual
def oneMaxFitness(individual):
    return sum(individual),  # return a tuple


toolbox.register("evaluate", oneMaxFitness)

# genetic operators:

# Tournament selection with tournament size of 3:
toolbox.register("select", tools.selTournament, tournsize=3)

# Single-point crossover:
toolbox.register("mate", tools.cxOnePoint)

# Flip-bit mutation:
# indpb: Independent probability for each attribute to be flipped
toolbox.register("mutate", tools.mutFlipBit, indpb=1.0/ONE_MAX_LENGTH)


# Genetic Algorithm flow:
def main():

    # create initial population (generation 0):
    population = toolbox.populationCreator(n=POPULATION_SIZE)

    # prepare the statistics object:
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("max", numpy.max)
    stats.register("avg", numpy.mean)

    # define the hall-of-fame object:
    hof = tools.HallOfFame(HALL_OF_FAME_SIZE)

    # perform the Genetic Algorithm flow with hof feature added:
    population, logbook = algorithms.eaSimple(population, toolbox, cxpb=P_CROSSOVER, mutpb=P_MUTATION,
                                              ngen=MAX_GENERATIONS, stats=stats, halloffame=hof, verbose=True)

    # print Hall of Fame info:
    print("Hall of Fame Individuals = ", *hof.items, sep="\n")
    print("Best Ever Individual = ", hof.items[0])

    # extract statistics:
    maxFitnessValues, meanFitnessValues = logbook.select("max", "avg")

    # plot statistics:
    sns.set_style("whitegrid")
    plt.plot(maxFitnessValues, color='red')
    plt.plot(meanFitnessValues, color='green')
    plt.xlabel('Generation')
    plt.ylabel('Max / Average Fitness')
    plt.title('Max and Average Fitness over Generations')

    plt.show()


if __name__ == "__main__":
    main()


# OneMax HOF

# Добавяне на функцията "Зала на славата" (Hall of Fame)

# Една допълнителна характеристика на вградения метод algorithms.eaSimple е възможността да се използва зала на славата 
# (Hall of Fame, HOF).

# Класът HallOfFame, имплементиран в модула tools, може да се използва, за да задържа най-добрите индивиди, които някога са съществували
# в популацията по време на еволюцията.

# Какво прави Hall of Fame?
# Запазва най-добрите индивиди: Дори ако тези индивиди са изгубени в резултат на селекция, кръстосване или мутация, те ще бъдат запазени.
# Постоянно сортиране: Залата на славата е сортирана така, че първият елемент винаги е индивидът с най-добрата стойност на годността, 
# наблюдавана по време на изпълнението.

# Започваме, като дефинираме константа за броя индивиди, които искаме да запазим в залата на славата. Ще добавим този ред към
# секцията за дефиниране на константи:

# HALL_OF_FAME_SIZE = 10

# Точно преди да извикаме алгоритъма eaSimple, ще създадем обект HallOfFame с този размер:

# hof = tools.HallOfFame(HALL_OF_FAME_SIZE)

# Обектът HallOfFame се изпраща като аргумент на алгоритъма eaSimple, който го актуализира вътрешно по време на изпълнението на потока
# на генетичния алгоритъм:

# population, logbook = algorithms.eaSimple(
#     population, toolbox,
#     cxpb=P_CROSSOVER,
#     mutpb=P_MUTATION,
#     ngen=MAX_GENERATIONS,
#     stats=stats,
#     halloffame=hof,
#     verbose=True
# )

# Когато алгоритъмът приключи, можем да използваме атрибута items на обекта HallOfFame, за да получим списък с индивидите, 
# които са включени в залата на славата:

# print("Hall of Fame Individuals = ", *hof.items, sep="\n")
# print("Best Ever Individual = ", hof.items[0])

# Резултатът от отпечатването изглежда по следния начин:

# Най-добрият индивид се състои от всички единици (1s).
# След него са различни индивиди, които имат стойности 0 на различни места.

# Най-добрият индивид е същият, който беше отпечатан първи преди това:

# Best Ever Individual = [1, 1, 1, 1, ..., 0, ..., 1]

# Това показва, че залата на славата успешно запазва най-добрия индивид, наблюдаван по време на изпълнението на алгоритъма.

# Оттук нататък ще използваме тези функции – обекта за статистика и logbook, вградения алгоритъм eaSimple и HallOfFame – във
# всички програми, които създаваме.

# Сега, след като научихме как да използваме вградените алгоритми, ще експериментираме с тях, за да открием разликите между 
# тях и да намерим най-добрия алгоритъм за различни приложения.