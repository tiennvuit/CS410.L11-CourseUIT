def print_information(info: dict):
    print("{:^77s}".format("INPUT INFORMATION"))
    print("-"*77)
    print("| {:50} | {:>20} |".format("The using evolutary algorithm", info['algorithm']))
    print("| {:50} | {:>20} |".format("The using solving problem", info['problem']))
    print("| {:50} | {:>20} |".format("The size of population", info['pop_size']))
    print("| {:50} | {:>20} |".format("The maximum numbers of generations", info['n_gen']))
    print("-"*77)

