import random
import time


def randChar():
    c = random.choice([i for i in range(64, 90)])
    if c == 64:
        return chr(32)
    if random.random() > 0.5:
        return chr(c + 32)
    return chr(c)

class DNA:

    def __init__(self, length):
        self.genes = []
        self.fitness = 0

        for i in range(length):
            self.genes.append(randChar())


    def fitness_points(self, target):
        score = 0

        for i in range(len(self.genes)):
            if(self.genes[i] == target[i]):
                score += 1

        self.fitness = score / len(target)


    def crossover(self, partner):
        midpointA = len(self.genes) // 2
        child = DNA(len(self.genes))
        child.genes.clear()

        for i in range(int(midpointA)):
            child.genes.append(self.genes[i])

        for i in range(int(midpointA), len(self.genes)):
            child.genes.append(partner.genes[i])

        return child

    def mutate(self, rate):
        for i in range(len(self.genes)):
            if random.random() < rate:
                self.genes[i] = randChar()



class Population:

    def __init__(self, target, mutation, max):
        self.population = []
        self.mating_pool = []
        self.mutation_rate = mutation
        self.target = target
        self.average_fitness = 0

        for i in range(max):
            self.population.append(DNA(len(target)))

    def calculate_fitness(self):
        length = len(self.population)
        fit = 0

        for i in range(length):
            self.population[i].fitness_points(self.target)
            fit += self.population[i].fitness

        fit /= len(self.population)
        self.average_fitness = fit

    def naturalSelection(self):
        self.mating_pool.clear()
        max = 0
        index = 0
        for i in range(len(self.population)):
            if self.population[i].fitness > max:
                max = self.population[i].fitness
                index = i

        print(''.join(self.population[index].genes))

        for i in range(len(self.population)):
            probability = (self.population[i].fitness / max) * len(self.target)

            for j in range(int(probability)):
                self.mating_pool.append(self.population[i])

        # for i in range(len(self.population)):
        #     print(self.population[i].genes)


    def generate(self):
        length = len(self.population)

        self.population.clear()

        for i in range(length):
            partnerA = random.choice(self.mating_pool)
            partnerB = random.choice(self.mating_pool)
            child = partnerA.crossover(partnerB)
            child.mutate(self.mutation_rate)
            self.population.append(child)

    def evaluate(self):
        for i in range(len(self.population)):
            # print("Fitness : " + str(self.population[i].fitness))
            if self.population[i].fitness == 1:
                return 1
            else:
                continue
        return 0

    def display(self):
        for i in range(len(self.population)):
            print(''.join(self.population[i].genes))


def procedure():
    check = 0
    generation = 0
    target = "To be or not to be"
    population = Population(target, 0.01, 1000)
    millis = int(time.time() * 1000)

    while (not check == 1):
        generation += 1
        population.calculate_fitness()
        population.naturalSelection()
        check = population.evaluate()
        population.generate()

        if check:
            print("Matched ! ")
            print("Evovled : " + str(target))
            print("Total Generations : " + str(generation))

    print("Total time : " + str(int(time.time() * 1000) - millis))

if __name__ == "__main__":
    procedure()