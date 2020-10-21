# Usage
"""
	python visualize.py -func 1MAX -crossover 1X

"""


import argparse
import os
from matplotlib import pyplot as plt
import numpy as np
import math

VALUE_PLOT = {
	'MRPS': 'MRPS_mean_values',
	'eval': 'mean_evaluations'
}


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


def visualize_data(processed_data, problem_sizes, value, function, saving_path):

	fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(9, 6))
	
	for crossover_way, data in processed_data.items():

		if value == 'MRPS':
			#ax.plot(np.log2(problem_sizes), np.log2(data['MRPS_mean_values']), label=crossover_way)
			ax.errorbar(np.log2(problem_sizes), np.log2(data['MRPS_mean_values']), 
						np.log10(data['MRPS_standard_deviations']), uplims=True, lolims=True,
						marker='x', linestyle='dashed', label=crossover_way)
		elif value == 'evaluations':
			#ax.plot(np.log2(problem_sizes), np.log2(data['mean_evaluations']), label=crossover_way)
			ax.errorbar(np.log2(problem_sizes), np.log2(data['mean_evaluations']), 
						np.log10(data['standard_deviation_evaluations']), uplims=True, lolims=True,
						marker='o', linestyle='dashdot', label=crossover_way)
	
	ax.set_title(r"BIỂU ĐỒ THỂ HIỆN GIÁ TRỊ {} CẦN TỐI ƯU HÀM {}".format(value, function), fontsize=14)
	ax.set_xlabel(r'PROBLEM SIZE', fontsize=12)
	ax.set_ylabel(r'{}'.format(value.upper()), fontsize=12)
	ax.set_xticks(np.log2(problem_sizes))
	
	plt.legend(loc='best')
	plt.show()

	# Save plot to disk
	fig.savefig(saving_path)
	print("Saved the plot to {}.".format(saving_path))


def main(args):

	saving_directory = os.path.join('../figure', args['function'])
	if not os.path.exists(saving_directory):
		os.midir(saving_directory)

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