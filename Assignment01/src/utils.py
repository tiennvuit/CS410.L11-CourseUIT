import numpy as np
import numpy.random as random


def initialize_population(N: int, l: int, distribution: dict):
    """
    - Description: Khởi tạo quần thể với N cá thể
    
    - Arguments: 
        + N (int): số lượng cá thể khởi tạo ban đầu
        + l (int): kích thước vấn đề (problem size), chiều dài của mỗi cá thể
        + distribution (dictionary): phân phối xác suất khởi tạo, ví dụ: {0: [0, 0.2), 1: [0.2, 0.5), 2: [0.5, 1)}
    
    - Return values:
        + population (ndarray): danh sách các các thể được khởi tạo ban đầu
    """

    population = []
    for i in range(N):     # Loop through each individual
        
        # Initalize individual with default l zero values
        individual = np.zeros(l, dtype=np.int32)

        for j in range(l):    # Loop though each variable of the individual    
            # Create a random trial to determine the value of variable.
            random_value = random.random()
            for key, value in distribution.items():
                # print(value)
                # print(random_value)
                if random_value >= value[0] and random_value < value[1]:
                    individual[j] = key
                    break
                    
        # Add the individual to population
        population.append(individual)

    return np.array(population)


def evaluation(individual: np.ndarray, _type="1MAX", k=5):
    """
    - Decsription: Đánh giá độ thích nghi của một cá thể theo hàm OneMax

    - Arguments:
        + individual (np.ndarray): cá thể cần đánh giá
    
    - Return values:
        + fitness (float): độ thích nghi của cá thể.
    """
    fitness = 0

    if _type=="1MAX":
        fitness = np.sum(individual)

    elif _type=="TRAP5":
        for start_trap in range(0, len(individual), k):
            one_bits = np.sum(individual[start_trap:start_trap+k])
            if one_bits == k:
                fitness += k
            else:
                fitness += k - 1 - one_bits
    else:
        print("The invalid fucntion !")
        exit(0)

    return fitness



def average_evaluation(population: np.ndarray, optimized_function:str):
    """
    - Description: Đánh giá độ thích nghi của quần thể bằng hàm OneMax
                   Công thức của hàm OneMax: $f(x) = \sum_{i=1}^{l}x_i$

    - Arguments:
        + population: quần thể hiện tại (danh sách các cá thể)
    
    - Return values:
        + average_fitness (float): độ thích nghi trung bình tính trên toàn bộ quần thể.
    """

    sum_fitness = 0
    number_evals = 0
    # Loop though each individual and calculate the its fitness
    for individual in population:
        current_fitness = evaluation(individual, optimized_function)
        number_evals += 1
        sum_fitness += current_fitness
    
    average_fitness = sum_fitness / len(population)

    return number_evals, average_fitness


def crossover(population: np.ndarray, crossover_way='1X', threshold=None):
    """
    - Description: Thực hiện phép lai ghép giữa các cá thể bên trong quần thể

    - Arguments:
        + population (np.ndarray): quần thể hiện tại
        + crossover_way (string): Phép lai cho phép: Lai một điểm (1X), Lai hai điểm (2X), Lai đồng nhất (UX).

    - Return values:
        + crossovered_individuals (np.ndarray): các cá thể mới được lai ghép từ quần thể đầu vào. 
    """

    N = len(population)
    l = len(population[0])

    crossovered_individuals = []

    if crossover_way == '1X':
        
        for i in range(0, N-1, 2):

            parrent_individual = (population[i], population[i+1])
            
            # Generate the pivot index
            pivot_index = random.randint(0, l+1)
            
            # Concatenate two subgen from parent
            child_individual1 = np.concatenate([parrent_individual[0][0:pivot_index], parrent_individual[1][pivot_index:l]])
            child_individual2 = np.concatenate([parrent_individual[1][0:pivot_index], parrent_individual[0][pivot_index:l]])
                                               
            # Add the new childrent to list
            crossovered_individuals.append(child_individual1)
            crossovered_individuals.append(child_individual2)

    elif crossover_way == '2X':
        for i in range(0, N-1, 2):

            parrent_individual = (population[i], population[i+1])
            
            # Generate the pivot index
            pivot_indices = random.randint(0, l+1, 2)
            
            # Concatenate two subgen from parent
            child_individual1 = np.concatenate([parrent_individual[0][0:pivot_indices[0]], 
                                                parrent_individual[1][pivot_indices[0]:pivot_indices[1]], 
                                                parrent_individual[0][pivot_indices[1]:l]])
            
            child_individual2 = np.concatenate([parrent_individual[1][:pivot_indices[0]], 
                                                parrent_individual[0][pivot_indices[0]:pivot_indices[1]], 
                                                parrent_individual[1][pivot_indices[1]:]])
                                               
            # Add the new childrent to list
            crossovered_individuals.append(child_individual1)
            crossovered_individuals.append(child_individual2)

    elif crossover_way == 'UX':
        for i in range(0, N-1, 2):

            parrent_individual = (population[i], population[i+1])
            
            # Generate the pivot indices by uniform distribution
            pivot_index = random.uniform(low=0, high=1, size=l)
            
            # Concatenate two subgen from parent
            child_individual1 = parrent_individual[0].copy()   # assumpt like father
            child_individual2 = parrent_individual[1].copy()   # assumpt like mother

            for i in range(l):
                if pivot_index < threshold:               # make the crossover 
                    child_individual1[i] = parrent_individual[1][i] 
                    child_individual2[i] = parrent_individual[0][i]

            # Add the new childrent to list
            crossovered_individuals.append(child_individual1)
            crossovered_individuals.append(child_individual2)
    else:
        print("The crossover way {} is NOT INVALID".format(crossover_way))
        exit(0)

    return np.array(crossovered_individuals)



def pop_pool(population: np.ndarray, offspring: np.ndarray):
    """
    - Description: Gom nhóm hai thế hệ: cha mẹ và con cái để tiến hành chọn lọc

    - Arguments: 
        + population (np.ndarray): quần thể ở thế hệ cha mẹ
        + offspring (np.ndarray): quần thể ở thế hệ con cái được biến đổi từ thế hệ cha mẹ

    - Return values:
        + combination_population (np.array): quần thể chứa tất cả cá thể của population và offspring.
    """

    combination_population = np.concatenate([population, offspring])

    return combination_population



def tournament_selection(population: np.ndarray, tournament_size:int, optimized_function:str):
    """
    - Description: Thực hiện phép chọn lọc bằng phương pháp Tournament Selection

    - Arguments:
        + population (np.ndarray): quần thể hiện tại
        + tournament_size (int): kích thước của một bảng đấu (dùng cho phương pháp Tournament Selection)
    
    - Return values:
        + selected_individuals (np.ndarrray): new population have the size equal 1/2 the input population size after perform selection

    """

    assert ((len(population) // tournament_size) == (len(population) / tournament_size)), "The population is NOT DIVISIBLE for tournament_size !"

    # Declare the array to store the selected individuals in selection
    selected_individuals = []
    
    # Calculate the number of hold tournament selection
    times  = int(tournament_size / 2)
    
    for time in range(times): 

        # Shuffle the population
        random.shuffle(population)
        
        # Divide tournaments with the same size
        tournaments = []
        i = 0
        while i < (len(population)):
            low = i
            i = i + tournament_size
            tournaments.append((low, i-1))

        # Loop through each tournament
        for (low, high) in tournaments:

            # Select the best individual of the tournament
            index_best_individual = low
            best_fitness = evaluation(population[index_best_individual], optimized_function)
            for i in range(low, high+1):
                current_fitness = evaluation(population[i])
                if current_fitness > best_fitness:
                    index_best_individual = i
                    best_fitness = current_fitness
            
            selected_individuals.append(population[index_best_individual])

    return np.array(selected_individuals)


def check_convergence(population: np.ndarray):
    """
    - Description: Kiểm tra quần thể đã hội tụ hay chưa

    - Arguments:
        - population (np.ndarray): quần thể hiện tại

    - Return values:
        - Boolean value: True nếu quần thể đã hội tụ(tất cả các cá thể đều đạt cấu hình giống nhau)
            và được cấu hình là [1 1 ... 1], False nếu không thỏa.
    """

    N = len(population)

    for i in range(0, N-1):
        comparison = (population[i] == population[N-1])
        if not comparison.all():
            return False
    return True
