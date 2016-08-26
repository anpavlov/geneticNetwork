import random
from chromosome import Chromosome

dim = 10
chromosome_length = dim  # min is (dim - 2)

my_src = 4
my_dest = 1
my_gens = 1000
quite = True

weights = [
    [ 0      ,	10     ,	9999999,	9999999,	3      ,	14     ,	9999999,	15     ,	3      ,	14     , ],
    [ 10     ,	0      ,	9999999,	9999999,	16     ,	20     ,	8      ,	9999999,	9999999,	13     , ],
    [ 9999999,	9999999,	0      ,	2      ,	15     ,	18     ,	9999999,	9999999,	9999999,	18     , ],
    [ 9999999,	9999999,	2      ,	0      ,	5      ,	9999999,	9999999,	9999999,	6      ,	9999999, ],
    [ 3      ,	16     ,	15     ,	5      ,	0      ,	9999999,	9999999,	4      ,	16     ,	9999999, ],
    [ 14     ,	20     ,	18     ,	9999999,	9999999,	0      ,	9999999,	9999999,	9999999,	9999999, ],
    [ 9999999,	8      ,	9999999,	9999999,	9999999,	9999999,	0      ,	9999999,	9      ,	9999999, ],
    [ 15     ,	9999999,	9999999,	9999999,	4      ,	9999999,	9999999,	0      ,	9999999,	2      , ],
    [ 3      ,	9999999,	9999999,	6      ,	16     ,	9999999,	9      ,	9999999,	0      ,	8      , ],
    [ 14     ,	13     ,	18     ,	9999999,	9999999,	9999999,	9999999,	2      ,	8      ,	0      , ],
]


class GeneNetwork(object):
    def __init__(self, dim, weights, chromosome_length, source, destination):
        """

        :param dim: problem dimension
        :param weights:
        :param chromosome_length: length of chromosome
        :param source: source node
        :param destination: destination node
        :return:
        """
        if source >= dim or destination >= dim:
            raise ValueError
        self.chromosome_length = chromosome_length
        self.dim = dim
        self.weights = weights
        self.source = source
        self.destination = destination
        self.population = []
        self.population_size = 0
        # self.results = []
        self.best = None

    def start(self, gen_max, pop_size):
        """

        :param gen_max: maximum number of generations
        :param pop_size: initial population size
        :return: best solution found
        """
        self.population = []
        self.population_size = 0
        # self.results = []
        self.best = None

        gen = 1  # from first generation
        self.generate_population(pop_size)  # generate initial population
        self.population_size = pop_size
        if not quite:
            pretty_print('Initital:')
            self.print_chromosomes(self.population)

        while gen <= gen_max:
            gen += 1
            # p = 1
            new_population = list()
            for p in range(self.population_size):
                parents = random.sample(range(self.population_size), 2)
                newbie = self.crossover(self.population[parents[0]], self.population[parents[1]])
                # TODO check child?
                # newbie.mutate()
                fit = self.fitness(newbie)
                # self.results.append((newbie, fit))
                new_population.append(newbie)
                if self.best is None or self.best[1] > fit:
                    self.best = (newbie, fit)
            if not quite:
                pretty_print('%dth generation (after crossover): ' % gen)
                self.print_chromosomes(new_population)
            self.selection(self.population, new_population)
            if not quite:
                pretty_print('After selection (after crossover): ')
                self.print_chromosomes(self.population)

            mutants = []
            for chrom in self.population:
                new_v = []
                new_v.extend(chrom.get())
                new_chrom = Chromosome(new_v)
                new_chrom.mutate()
                fit = self.fitness(new_chrom)
                mutants.append(new_chrom)
                if self.best is None or self.best[1] > fit:
                    self.best = (chrom, fit)
            if not quite:
                pretty_print('%dth generation (after mutations): ' % gen)
                self.print_chromosomes(mutants)
            self.selection(self.population, mutants)
            if not quite:
                pretty_print('After selection (after mutations): ')
                self.print_chromosomes(self.population)
        return self.best

    def selection(self, prev, now):
        """

        :param prev: previous generation
        :param now: new generation
        :return:
        """
        prev.extend(now)
        # check = []
        # check.extend(prev)
        self.bubble_sort(prev)
        self.population = prev[:self.population_size]

    def bubble_sort(self, alist):
        for passnum in range(len(alist)-1,0,-1):
            for i in range(passnum):
                if self.fitness(alist[i])>self.fitness(alist[i+1]):
                    temp = alist[i]
                    alist[i] = alist[i+1]
                    alist[i+1] = temp

    def generate_population(self, n):
        """

        :param n: number of chromosomes
        :return:
        """
        chromosomes = list()
        for i in range(n):
            chromosomes.append(self._gen_chromosome())
        self.population = chromosomes

    def _gen_chromosome(self):
        """

        :return: random path from source to destination
        """
        chromosome = random.sample(list(set(range(self.dim)) - {self.source, self.destination}),
                                   self.chromosome_length - 2)
        chromosome.insert(0, self.source)
        chromosome.append(self.destination)
        return Chromosome(chromosome)

    def crossover(self, mother, father):
        """

        :param mother: first parent
        :param father: second parent
        :return: crossing over child
        """
        mother_list = mother.get()
        father_list = father.get()
        cut = random.randint(0, self.chromosome_length - 1)
        child = mother_list[0:cut] + father_list[cut:]
        return Chromosome(child)

    def fitness(self, chromosome):
        chromosome_list = chromosome.get()
        return sum([self.weights[i][j] for i, j in zip(chromosome_list[:-1], chromosome_list[1:])])

    def print_chromosomes(self, chromosomes):
        for chromosome in chromosomes:
            print str(chromosome) + ' ' + str(self.fitness(chromosome))


def pretty_print(to_print, hint=''):
    print ''
    print '=================='
    print hint + str(to_print)
    print '=================='


if __name__ == "__main__":
    gene_network = GeneNetwork(dim, weights, chromosome_length, my_src, my_dest)
    res = 100
    while res > 13:
        res = gene_network.start(my_gens, 10)  # start with 1000 generations and 10 initial chromosomes
    pretty_print(res, 'Solution: ')