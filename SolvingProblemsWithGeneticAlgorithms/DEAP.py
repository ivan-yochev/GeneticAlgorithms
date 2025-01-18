# Импортиране на необходимите модули от библиотеката DEAP
# DEAP е библиотека за еволюционни алгоритми, която предоставя инструменти за създаване на персонализирани генетични алгоритми.
from deap import base, creator, tools, algorithms
import random

# OneMax проблемът цели да се максимизира броят на единици в даден двоичен масив.
# Например, за двоичен масив [1, 0, 1, 1], резултатът е 3 (три единици).

# 1. Дефиниране на типа на индивидите и популацията
# Създаваме фитнес функция за максимизация (weights=(1.0,))
# "weights" указва посоката на оптимизация. Положителна стойност (+1.0) означава максимизация.
# base.Fitness е базов клас в DEAP, който се използва за създаване на персонализирани фитнес функции.
# Атрибутът weights дефинира целта на оптимизацията: положителните стойности водят до максимизация, а отрицателните до минимизация.
# Тук weights=(1.0,) показва, че имаме едноцелево оптимизиране, където максимизираме резултата.
creator.create("FitnessMax", base.Fitness, weights=(1.0,))

# Създаваме клас "Individual", който наследява от list и има фитнес атрибут от тип FitnessMax
# Индивидите са базирани на list, защото всеки индивид представлява подреден набор от гени (в случая, двоични стойности),
# които могат лесно да бъдат достъпвани, модифицирани и оценявани.
# Атрибутът fitness позволява асоциирането на фитнес стойност с всеки индивид, което е от съществено значение за
# еволюционния процес. Това асоцииране улеснява изчисляването и съхранението на фитнес стойностите, без да се
# налага повторно изчисление при всяка итерация.
creator.create("Individual", list, fitness=creator.FitnessMax)

# 2. Инициализация на основните компоненти на алгоритъма
# Създаваме контейнер за всички елементи на еволюционния алгоритъм.
toolbox = base.Toolbox()

# Дефинираме как се създава двоичен ген (0 или 1).
# random.randint е функция, която генерира произволно цяло число в зададен интервал [a, b].
# В този контекст тя е използвана за генериране на двоични стойности (0 или 1),
# които представляват гени в индивида. Двоичният тип е избран заради простотата на представяне
# и лесното манипулиране в задачи като OneMax, където броят на единиците е целта.
# Това също така позволява на алгоритъма да изследва различни комбинации от гени чрез мутация и кросоувър.
toolbox.register("attr_bool", random.randint, 0, 1)

# Дефинираме как се създава индивид. Индивидът е списък от 100 бита (гени).
# "tools.initRepeat" е функция, която позволява създаване на обект чрез повторно извикване на друга функция.
# В случая, тя създава списък (list) от фиксирана дължина (n=100), като всеки елемент се генерира от "toolbox.attr_bool".
# Това е подходящо за създаване на индивиди, тъй като гените в индивида трябва да имат еднакъв тип и фиксиран брой.
# Аргументите на initRepeat са:
# - контейнер (creator.Individual): структурата, която ще се създава;
# - функция (toolbox.attr_bool): генераторът за всеки елемент;
# - брой повторения (n=100): дължината на списъка.
# Функцията връща списък, който представлява индивид с предварително дефинирани свойства.
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=100)

# Дефинираме как се създава популация. Популацията е списък от индивиди.
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# 3. Дефиниране на фитнес функцията
# Фитнес функцията измерва качеството на даден индивид. За OneMax това е просто броят на единиците в индивида.
def evalOneMax(individual):
    return sum(individual),  # Връщаме резултата като кортеж, защото DEAP изисква фитнес стойностите да са итеративни обекти.

# Регистрираме фитнес функцията в toolbox.
toolbox.register("evaluate", evalOneMax)

# Дефинираме операторите за селекция, кросоувър и мутация.
# Селекцията използва турнирна селекция с размер 3.
toolbox.register("select", tools.selTournament, tournsize=3)

# Кросоувърът (кръстосване) използва двуточков метод.
toolbox.register("mate", tools.cxTwoPoint)

# Мутацията инвертира бита с вероятност 0.05.
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)

# 4. Основен цикъл на генетичния алгоритъм
# Създаваме начална популация от 300 индивида.
population = toolbox.population(n=300)

# Дефинираме вероятности за операторите на еволюция.
CXPB, MUTPB, NGEN = 0.5, 0.2, 40
# CXPB: Вероятност за кросоувър
# MUTPB: Вероятност за мутация
# NGEN: Брой поколения

# Статистика: Събираме информация за минималната, средната и максималната фитнес стойност в популацията.
# tools.Statistics е инструмент в DEAP за изчисляване на статистики върху дадена характеристика на индивидите.
# Тук използваме анонимна функция (lambda), за да извлечем фитнес стойността на всеки индивид.
# Това е необходимо, защото фитнес стойностите са обвити в кортежи, а ние искаме да обработим само числовите стойности.
# Статистика: Събираме информация за минималната, средната и максималната фитнес стойност в популацията.
stats = tools.Statistics(lambda ind: ind.fitness.values[0])  # Извличаме само първия (единствен) елемент на фитнес стойностите.
stats.register("min", min)
stats.register("avg", lambda x: sum(x) / len(x))
stats.register("max", max)

# Еволюционният процес (генетичен алгоритъм)
population, logbook = algorithms.eaSimple(
    population, toolbox,
    cxpb=CXPB, mutpb=MUTPB,
    ngen=NGEN, stats=stats,
    verbose=True
)

# Най-добрият индивид след еволюцията
best_individual = tools.selBest(population, k=1)[0]
print("Best individual is:", best_individual)
print("Fitness:", best_individual.fitness.values)
