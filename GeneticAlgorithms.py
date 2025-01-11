# Hands-On  Genetic Algorithms with Python by  Eyal Wirsansky

# What are genetic algorithms?
# Genetic algorithms are a family of search algorithms that are inspired by the principles of evolution in 
# nature. By imitating the process of natural selection and reproduction, genetic algorithms can produce 
# high-quality solutions for various problems involving search, optimization, and learning. At the same 
# time, their analogy to natural evolution allows genetic algorithms to overcome some of the hurdles 
# that are encountered by traditional search and optimization algorithms, especially for problems with 
# a large number of parameters and complex mathematical representations.

# The principle of variation: The traits (attributes) of individual specimens belonging to a 
# population may vary. As a result, the specimens differ from each other to some degree, for 
# example, in their behavior or appearance.
#  • The principle of inheritance: Some traits are consistently passed on from specimens to their 
# offspring. As a result, offspring resemble their parents more than they resemble unrelated specimens.
#  • The principle of selection: Populations typically struggle for resources within their given 
# environment. The specimens possessing traits that are better adapted to the environment will 
# be more successful at surviving and will also contribute more offspring to the next generation.

# Генетичните алгоритми поддържат набор от решения за даден пробле, наречен individuals. Тези кандидати се оценявят 
# итеративно и най-добрите от тях се избират за създаване на следващо решение.

# Genotype - Генотип
#  В природата размножаването, размножаването и мутацията се улесняват чрез генотипа – колекция от гени 
# които са групирани в хромозоми. Ако два екземпляра се размножават, за да създадат потомство, всяка хромозома от 
# потомството ще носи комбинация от гени и от двамата родители. Имитиране на тази концепция, в случай на генетични 
# алгоритми, всеки индивид е представен от хромозома, представляваща колекция от гени. За 
# Например, една хромозома може да бъде изразена като двоичен низ, където всеки бит представлява един ген

# Genotype
#  In nature, breeding, reproduction, and mutation are facilitated via the genotype – a collection of genes 
# that are grouped into chromosomes. If two specimens breed to create offspring, each chromosome of 
# the offspring will carry a mix of genes from both parents. Mimicking this concept, in the case of genetic 
# algorithms, each individual is represented by a chromosome representing a collection of genes. For 
# example, a chromosome can be expressed as a binary string, where each bit represents a single gene:

# Population
#  At any point in time, genetic algorithms maintain a population of individuals – a collection of candidate 
# solutions for the problem at hand. Since each individual is represented by some chromosome, this 
# population of individuals can be seen as a collection of such chromosomes:
# The population continually represents the current generation and evolves when the current generation 
# is replaced by a new one.

#  Fitness function
#  At each iteration of the algorithm, the individuals are evaluated using a fitness function (also called the 
# target function). This is the function we seek to optimize or the problem we are attempting to solve.
#  Individuals who achieve a better fitness score represent better solutions and are more likely to 
# be chosen to reproduce and be represented in the next generation. Over time, the quality of the 
# solutions improves, the fitness values increase, and the process can stop once a solution is found with 
# a satisfactory fitness value

# Selection
#  After calculating the fitness of every individual in the population, a selection process is used to 
# determine which of the individuals in the population will get to reproduce and create the offspring 
# that will form the next generation.
#  T
#  his selection process is based on the fitness score of the individuals. Those with higher score values 
# are more likely to be chosen and pass their genetic material to the next generation.
#  Individuals with low fitness values can still be chosen but with a lower probability. This way, their 
# genetic material is not completely excluded, maintaining genetic diversity.

 Crossover
 To create a pair of new individuals, two parents are usually chosen from the current generation, 
and parts of their chromosomes are interchanged (crossed over) to create two new chromosomes 
representing the offspring. This operation is called crossover or recombination:

 Mutation
 The purpose of the mutation operator is to refresh the population, introduce new patterns into the 
chromosomes, and encourage search in uncharted areas of the solution space periodically and randomly.
 A mutation may manifest itself as a random change in a gene. Mutations are implemented as random 
changes to one or more of the chromosome values; for example, flipping a bit in a binary string: (10101010 --- 10111010)