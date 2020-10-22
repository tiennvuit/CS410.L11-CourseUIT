# Usage
"""
	python visualize.py -func 1MAX -val MRPS

"""


import argparse
import os
from matplotlib import pyplot as plt
import numpy as np
import math


# Load data from directory
def load_data_from_directory(path):

	entire_data = dict()
	subpaths = os.listdir(path)

	for subpath in subpaths:

		data = []
		problem_sizes = []
		
		file_paths = os.listdir(os.path.join(path, subpath))		
		for file in file_paths:

			# Get the problem size via file name 
			pro_size = int(file.split(".")[0])
			problem_sizes.append(pro_size)
			
			# Read data from the file
			with open(os.path.join(path, subpath, file), 'rb') as f:
				data_pro_size = np.load(f)

			data.append(data_pro_size)

		entire_data[subpath] = data

	return entire_data, problem_sizes


def process_data(entire_data):

	processed_data = dict()

	for crossover_way, data in entire_data.items():
		
		MRPS_mean_values = []
		MRPS_standard_deviations = []
		mean_evaluations = []
		standard_deviation_evaluations = []

		# Loop for each hypothesis data problem size
		for data_pro_size in data:

			mean_MRPS, mean_eval = np.mean(data_pro_size, axis=0)
			std_MRPS, std_eval = np.std(data_pro_size, axis=0)

			MRPS_mean_values.append(mean_MRPS)
			mean_evaluations.append(mean_eval)
			MRPS_standard_deviations.append(std_MRPS)
			standard_deviation_evaluations.append(std_eval)

		processed_data[crossover_way] = {'MRPS_mean_values': MRPS_mean_values, 
										'MRPS_standard_deviations': MRPS_standard_deviations, 
										'mean_evaluations': mean_evaluations, 
										'standard_deviation_evaluations': standard_deviation_evaluations}
	return processed_data


def print_infor_table(problem_sizes, data: dict):

	print("-"*104)
	print("|{:^20}|{:^40}|{:^40}|".format(" ", "sGA-1X", "sGA-UX"))
	print("-"*104)
	print("|{:^20}|{:^19}|{:^20}|{:^19}|{:^20}|".format("Problem size", "MRPS", "# Evaluations", "MRPS", "# Evaluations"))
	print("-"*104)
	for i, problem_size in enumerate(problem_sizes):

		print(r"|{:^20}|{:^19}|{:^20}|{:^19}|{:^20}|".format(problem_size, 
						str(round(data['1X']['MRPS_mean_values'][i], 2)) + '+-' + str(round(data['1X']['MRPS_standard_deviations'][i], 2)), 
						str(round(data['1X']['mean_evaluations'][i], 2)) + '+-' + str(round(data['1X']['standard_deviation_evaluations'][i], 2)), 
						str(round(data['UX']['MRPS_mean_values'][i], 2)) + '+-' + str(round(data['UX']['MRPS_standard_deviations'][i], 2)), 
						str(round(data['UX']['mean_evaluations'][i], 2)) + '+-' + str(round(data['UX']['standard_deviation_evaluations'][i], 2))))
		print("-"*104)

	print("-"*104)



def visualize_data(processed_data, problem_sizes, value, function, saving_path):

	plt.style.use('ggplot')
	fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(9, 6))
	
	i = 0
	for crossover_way, data in processed_data.items():
		# print('{}\n{}'.format(crossover_way, data))
		# input()
		if value == 'MRPS':
			#ax.plot(np.log2(problem_sizes), np.log2(data['MRPS_mean_values']), label=crossover_way)
			ax.errorbar(problem_sizes, data['MRPS_mean_values'], 
						data['MRPS_standard_deviations'], uplims=True, lolims=True,
						marker=i, linestyle='solid', label=crossover_way)
			for x, y in zip(problem_sizes, data['MRPS_mean_values']):
				label = "{:.2f}".format(y)
				plt.annotate(label, # this is the text
							(x,y), # this is the point to label
			            	textcoords="offset points", # how to position the text
			                 xytext=(0,10), # distance from text to points (x,y)
			                 ha='left') # horizontal alignment can be left, right or center

		elif value == 'evaluations':
			#ax.plot(np.log2(problem_sizes), np.log2(data['mean_evaluations']), label=crossover_way)
			ax.errorbar(problem_sizes, data['mean_evaluations'], 
						data['standard_deviation_evaluations'], uplims=True, lolims=True,
						marker='o', linestyle='solid', label=crossover_way)

			for x, y in zip(problem_sizes, data['mean_evaluations']):
				label = "{:.2f}".format(y)
				plt.annotate(label, # this is the text
			                 (x,y), # this is the point to label
			                 textcoords="offset points", # how to position the text
			                 xytext=(0,10), # distance from text to points (x,y)
			                 ha='left') # horizontal alignment can be left, right or center			
		i += 1

	print_infor_table(problem_sizes, processed_data)

	ax.set_title(r"BIỂU ĐỒ THỂ HIỆN GIÁ TRỊ {} CẦN TỐI ƯU HÀM {}".format(value, function), fontsize=14)
	ax.set_xlabel(r'PROBLEM SIZE', fontsize=12)
	ax.set_ylabel(r'{}'.format(value.upper()), fontsize=12)
	#ax.set_xticks(problem_sizes)
	
	plt.xscale('linear')
	plt.yscale('log')

	plt.legend(loc='best')
	plt.show()

	# Save plot to disk
	fig.savefig(saving_path)
	print("Saved the plot to {}.".format(saving_path))


def main(args):

	saving_directory = os.path.join('../figure', args['function'])
	if not os.path.exists(saving_directory):
		os.mkdir(saving_directory)

	saving_path = os.path.join(saving_directory, args['value'] + '.png')

	# print Information before run
	print("\n\n", "-"*15, "THE PLOTTING DATA INFORAMTION", "-"*15)
	print('-'*62)
	print("|- {:25} | {:<30}|".format("The optimized function ", args['function']))
	print('-'*62)
	print("|- {:25} | {:<30}|".format("The saving path", saving_path))
	

	# Load data from directory
	data_path = os.path.join('../hypothesis', args['function'])
	data, problem_sizes = load_data_from_directory(path=data_path)

	# process data
	processed_data = process_data(data)

	# Visualize data
	visualize_data(processed_data=processed_data, problem_sizes=problem_sizes, value=args['value'], function=args['function'], saving_path=saving_path)



if __name__ == '__main__':
	# Get arguments from bash command
	parser = argparse.ArgumentParser(description='Plot grath to visualize results for sGA')
	parser.add_argument('--function', '-func', choices=['1MAX', 'TRAP5'], required=True
						,help='The function need to be optimized')
	parser.add_argument('--value', '-val', choices=['MRPS', 'evaluations'], required=True
						,help='The value need plotting.')

	args = vars(parser.parse_args())
	main(args)