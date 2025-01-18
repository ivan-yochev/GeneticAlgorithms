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

    # perform the Genetic Algorithm flow:
    population, logbook = algorithms.eaSimple(population, toolbox, cxpb=P_CROSSOVER, mutpb=P_MUTATION, ngen=MAX_GENERATIONS,
                                   stats=stats, verbose=True)


    # Genetic Algorithm is done - extract statistics:
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



# Използване на вградени алгоритми

# Рамката DEAP предоставя няколко вградени еволюционни алгоритми в модула algorithms. Един от тях, eaSimple, имплементира потока на
# генетичния алгоритъм, който използвахме, и може да замени голяма част от кода в основния метод.

# Други полезни обекти в DEAP:
# Statistics:

# Обект, който се използва за събиране на статистики за популацията по време на изпълнението на алгоритъма.
# Logbook:

# Обект за съхраняване и отпечатване на информация за изпълнението, като например максималната и средната годност през поколенията.
# Има се предвид : 02_OneMax_short.py

# The Statistics object

# Обектът Statistics

# Първата промяна, която ще направим, е свързана със събирането на статистики. За тази цел ще се възползваме от класа tools.Statistics, 
# предоставен от DEAP. Тази помощна функция ни позволява да създадем статистически обект, използвайки аргумент key, който е функция,
# приложима върху данните, за които се изчисляват статистики.

# 1. Определяне на ключова функция:
# Тъй като данните, които планираме да предоставим, са популацията за всяко поколение, ще зададем key на функция, която извлича 
# стойностите за годност от всеки индивид.

# stats = tools.Statistics(lambda ind: ind.fitness.values)

# Обяснение:
# tools.Statistics:

# Създава обект за събиране на статистика.
# lambda ind: ind.fitness.values:

# Анонимна функция (lambda), която извлича стойностите на годността (fitness.values) за всеки индивид в популацията.
# С този обект ще можем лесно да изчисляваме статистики като максимална, средна и минимална годност за всяко поколение.

# Регистриране на функции за статистически изчисления

# Сега можем да регистрираме различни функции, които ще бъдат прилагани върху стойностите на годността на всяка стъпка. В този пример
# използваме само функциите numpy.max и numpy.mean, но можем да регистрираме и други функции като numpy.min или numpy.std.

# stats.register("max", numpy.max)  # Регистрира максималната стойност
# stats.register("avg", numpy.mean) # Регистрира средната стойност

# Обяснение:
# stats.register:

# Позволява да регистрираме функция за изчисляване на статистики върху извлечените стойности (годност в този случай).
# Функции:

# numpy.max: Изчислява максималната стойност.
# numpy.mean: Изчислява средната стойност.

# Алгоритъмът

# Сега е време за изпълнение на реалния поток на генетичния алгоритъм. Това се реализира чрез едно единствено извикване на метода
# algorithms.eaSimple, който е един от вградените еволюционни алгоритми, предоставени от модула algorithms на DEAP.

# population, logbook = algorithms.eaSimple(
#     population,
#     toolbox,
#     cxpb=P_CROSSOVER,      # Вероятност за кръстосване
#     mutpb=P_MUTATION,      # Вероятност за мутация
#     ngen=MAX_GENERATIONS,  # Брой поколения за изпълнение
#     stats=stats,           # Обектът за статистика
#     verbose=True           # Печат на информация за всяко поколение
# )

# Обяснение на параметрите:
# population:
# Текущата популация, върху която се изпълнява алгоритъмът.
# toolbox:
# Съдържа регистрираните оператори (evaluate, select, mate, mutate).
# cxpb (Crossover Probability):
# Вероятност за прилагане на кръстосване между индивидите.
# mutpb (Mutation Probability):
# Вероятност за прилагане на мутация върху индивидите.
# ngen (Number of Generations):
# Условие за спиране, задаващо броя на поколенията, които алгоритъмът ще изпълни.
# stats:
# Обектът stats за събиране на статистики, регистриран по-рано.
# verbose:
# Ако е True, алгоритъмът ще отпечатва информация за всяко поколение (например максимална и средна годност).
# Важно уточнение:
# Методът algorithms.eaSimple изисква преди това да сме регистрирали операторите (evaluate, select, mate, mutate) в toolbox.
# Условието за спиране се задава чрез параметъра ngen, който указва броя поколения, за които алгоритъмът ще работи.
# Резултати:
# population: Върнатата популация след изпълнението на алгоритъма.
# logbook: Обект, съдържащ събраните статистики и информация за всяко поколение.

# Logbook (дневник)

# След приключването на потока, алгоритъмът връща два обекта:

# population: Последната популация след изпълнението на алгоритъма.
# logbook: Обект, съдържащ събраните статистики по време на изпълнението.
# Извличане на статистики от logbook:
# Можем да извлечем желаните статистики от logbook, използвайки метода select(), за да ги използваме за визуализация, както 
# направихме преди.

# maxFitnessValues, meanFitnessValues = logbook.select("max", "avg")

# Обяснение:
# logbook.select("max", "avg"):

# Извлича стойностите за максималната ("max") и средната ("avg") годност, събрани за всяко поколение.
# maxFitnessValues:

# Списък със стойностите за максималната годност през поколенията.
# meanFitnessValues:

# Списък със стойностите за средната годност през поколенията.

# Стартитаме програмата: 

# Автоматично отпечатване на резултатите

# Тези отпечатвания се генерират автоматично от метода algorithms.eaSimple, в съответствие с начина, по който дефинирахме обекта за 
# статистика, изпратен към него, и поради факта, че аргументът verbose беше зададен на True.

# Разлики с предишната програма:
# Отпечатване за поколение 0:

# Тук има изход за поколение 0, което не беше включено в предишната програма.
# Продължителност на генетичния поток:

# В тази версия потокът продължава до 50-то поколение, тъй като това беше единственото условие за спиране.
# В предишната програма потокът спря на 40-то поколение, защото допълнителното условие за спиране – достигане на най-доброто решение 
# (познато предварително) – беше изпълнено.