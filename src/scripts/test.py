# Python Packages
import multiprocessing
import os
import random
import sys
import logging
import time


# Local Imports
from .data_retriever import data_retriever
from .gpx_export import GPX_export
from .pathfinder import Pathfinder

# from . import views as Views


class MarkdownColoredFormatter(logging.Formatter):
	COLORS = {
		'DEBUG': 'Green',
		'INFO': 'Black',
		'WARNING': 'Orange',
		'ERROR': 'Red',
		'CRITICAL': '#31;47',  # Dark-Blue
	}

	def format(self, record):
		log_color = self.COLORS.get(record.levelname, '0')
		message = super().format(record)
		return f'<font color="{log_color}">{message}</font>'


# Configure the logging module with a custom MarkdownColoredFormatter
logging.basicConfig(level=logging.DEBUG)  # Set the root logger level
# Create a console handler with a MarkdownColoredFormatter
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

formatter = MarkdownColoredFormatter(
	"%(asctime)s - %(levelname)s - %(message)s",
	datefmt=None,
)

console_handler.setFormatter(formatter)

# Create a Markdown-formatted file handler and set the level to DEBUG
file_handler = logging.FileHandler('test_files/output/main_test_logger.md')
file_handler.setLevel(logging.DEBUG)

# Create a Markdown formatter and set it for the file handler
file_formatter = MarkdownColoredFormatter(
	'%(asctime)s - %(levelname)s - %(message)s<br>',
	datefmt=None,
)
file_handler.setFormatter(file_formatter)


def generate_folder_structure(root_path, ignore_folders, output_file='test_files/output/Project_Structure.md'):
	if ignore_folders is None:
		ignore_folders = set()

	with open(output_file, "w") as file:
		file.write("# Folder Structure\n\n")
		generate_folder_structure_recursive(root_path, file, 0, ignore_folders)


def convert_size(size_bytes):
	# Convert file size to a human-readable format
	for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
		if size_bytes < 1024.0:
			return f"{size_bytes:.2f} {unit}"
		size_bytes /= 1024.0


def generate_folder_structure_recursive(folder_path, file, depth, ignore_folders):
	indent = "  " * depth
	folder_name = os.path.basename(folder_path)

	if folder_name in ignore_folders:
		return

	file.write(f"{indent}- {folder_name}/\n")

	try:
		entries = os.listdir(folder_path)
	except OSError:
		return

	for entry in entries:
		entry_path = os.path.join(folder_path, entry)

		# get file size
		try:
			file_size = convert_size(os.path.getsize(entry_path))
		except OSError:
			file_size = 0

		if os.path.isdir(entry_path):
			generate_folder_structure_recursive(entry_path, file, depth + 1, ignore_folders)
		else:
			file.write(f"{indent}  - {entry}: {file_size}\n")


def helper_get_closest_node(i, transport, risk, location):
	database_connection = data_retriever()
	database_connection.connect()
	result = database_connection.get_closest_nodes(location, transport, risk)
	database_connection.close()
	return i, transport, risk, location, result


class Test:
	def __init__(self):
		# Create an instance-level logger
		self.logger = logging.getLogger(__name__)

		# Add the console handler to the logger
		self.logger.addHandler(console_handler)

		# Add the file handler to the logger
		self.logger.addHandler(file_handler)

		# initialize variables
		self.timeout = 20 		# seconds
		self.number_of_tests = 2
		self._amenenity_types = ["Grocery",
								 "Books",
								 "Cafe",
								 "Drink",
								 "Food",
								 "Treats",
								 "Businesses",
								 "Community_Hubs",
								 "Pharmacy",
								 "Bike_Repair",
								 "Bike_Shops",
								 "Bathrooms,_Drinking_Fountains",
								 "Bike_Parking",
								 "Worlds_of_Wonder",
								 "Art",
								 "Sculptures"]
		self._north_bound = 42.369062
		self._south_bound = 42.157
		self._west_bound = -85.6995747
		self._east_bound = -85.531
		self._transportation_types = ["bike", "walk"]
		self._risk_factor_list = [1, 2, 3, 4]
		self.location_list = []
		self._passed_tests = []
		self._failed_tests = []

		# initialize imported modules
		self.data_retriever = data_retriever()
		self.gpx_export = GPX_export(None)
		self.pathdinder = Pathfinder(None, None, None, None)
		# self.pathfinder = pathfinder.Pathfinder(None, None, None, None)
		# self.views = views.views()

		# call test functions
		self.test_database()
		self.test_gpx_export()



	# TEST FUNCTIONS
	# generate folder structure
	ignore_folders = {'.git', '.idea', '__pycache__'}
	generate_folder_structure("../", ignore_folders, "test_files/output/Project_Structure.md")

	# START OF DATABASE TESTS (using data_retriever.py)
	def test_database(self):
		# self.logger.debug('This is a debug message')
		# self.logger.info('This is an info message')
		# self.logger.warning('This is a warning message')
		# self.logger.error('This is an error message')
		# self.logger.critical('This is a critical message')

		# check if database exists in db folder
		try:
			assert os.path.exists('db/routeplanning.db')
			self.logger.info("Database exists")
		except:
			self.logger.error("Database does not exist")
			assert False, self.error("Database does not exist")

		# try to connect to database
		try:
			self.data_retriever.connect()
			self.logger.info("Database connection successful")
		except:
			self.logger.error("Database connection failed")
			assert False, self.error("Database connection failed")

		# try for each amenity type to get amenities from database
		for amen_type in self._amenenity_types:
			if len(self.data_retriever.get_amenities(amen_type)) > 0:
				self.logger.info(f"Database get_amenities successful for {amen_type}")
			else:
				self.logger.error(f"Database get_amenities failed for {amen_type}")
				assert True, self.error(f"Database get_amenities failed for {amen_type}")



		# try to get_closest_node from database while testing random nodes
		with multiprocessing.Pool(processes=len(self._transportation_types) * len(self._risk_factor_list)) as pool:
			processes = []

			for i in range(self.number_of_tests):
				location = [0, random.uniform(self._south_bound, self._north_bound),
							random.uniform(self._west_bound, self._east_bound), 0]

				for transport in self._transportation_types:
					for risk in self._risk_factor_list:
						# Use pool.apply_async to run the helper_get_closest_node function in parallel
						processes.append(pool.apply_async(helper_get_closest_node, (i, transport, risk, location)))

			# try to Collect results immediately after submitting tasks and then wait for the remaining tasks to complete
			if self.number_of_tests == 1:
				results = [process.get(timeout=self.timeout * 2) for process in processes]
			else:
				results = [process.get(timeout=self.timeout * self.number_of_tests) for process in processes]


		# Handle the results as needed
		for result in results:
			try:
				# Access the information from the result tuple
				i, transport, risk, location, closest_nodes = result
				# Process the result and associated information
				self.logger.info(
					f"Database get_closest_nodes successful for {i}, transport: {transport}, risk:{risk}, location: {location}")
			except multiprocessing.TimeoutError:
				i, transport, risk, location, closest_nodes = result
				self.logger.error(
					f"Database get_closest_nodes for {i} timed out after {self.timeout} s, transport: {transport}, risk:{risk}, location: {location}")
				assert True, self.error(
					f"Database get_closest_nodes for {i} timed out after {self.timeout} s, transport: {transport}, risk:{risk}, location: {location}")


		# test get_node_info
		# open file to get a list of all node ids
		with open('test_files/input/nodes.csv', 'r') as f:
			next(f)		# skip header
			node_ids = f.readlines()

		for i in range(self.number_of_tests):
			# pick a random node id
			node_id = random.choice(node_ids).strip()
			try:
				if len(self.data_retriever.get_node_info(node_id)) > 0:
					self.logger.info(f"Database get_node_info successful for {node_id}")
			except Exception as e:
				self.logger.error(f"Database get_node_info failed with {e}, for {node_id}")
				assert True, self.error(f"Database get_node_info failed with {e}, for {node_id}")


		# test get_way
		with open('test_files/input/nodes.csv', 'r') as f:
			next(f)		# skip header
			node_ids = f.readlines()

		for i in range(self.number_of_tests):
			# pick a random node id
			node_id = random.choice(node_ids).strip()
			# add a bunch of try excepts to catch errors for all tests! (and log them)

			try:
				if len(self.data_retriever.get_way(node_id)) > 0:
					self.logger.info(f"Database get_way successful for {node_id}")
			except Exception as e:
				self.logger.error(f"Database get_way failed with {e}, for {node_id}")
				assert True, self.error(f"Database get_way failed with {e}, for {node_id}")



		# test get_way_info
		with open('test_files/input/nodes.csv', 'r') as f:
			next(f)		# skip header
			node_ids = f.readlines()

		for i in range(self.number_of_tests):

			node_id = random.choice(node_ids).strip()
			way_id = self.data_retriever.get_way(node_id)
			try:
				if len(self.data_retriever.get_way_info(way_id)) > 0:
					self.logger.info(f"Database get_way_info successful for {way_id}")
				else:
					self.logger.error(f"Database get_way_info failed for {way_id}")
					assert True, self.error(f"Database get_way_info failed for {way_id}")
			except Exception as e:
				self.logger.error(f"Database get_way failed with {e}, for {way_id}")
				assert True, self.error(f"Database get_way failed with {e}, for {way_id}")


		# test get_node_neighbors
		with open('test_files/input/nodes.csv', 'r') as f:
			next(f)		# skip header
			node_ids = f.readlines()

		for i in range(self.number_of_tests):
			node_id = random.choice(node_ids).strip()

			try:
				if len(self.data_retriever.get_node_neighbors(node_id)) > 0:
					self.logger.info(f"Database get_node_neighbors successful for {node_id}")
			except Exception as e:
				self.logger.error(f"Database get_node_neighbors failed with {e}, for {node_id}")
				assert True, self.error(f"Database get_node_neighbors failed with {e}, for {node_id}")


		# test get_node_coords
		with open('test_files/input/nodes.csv', 'r') as f:
			next(f)		# skip header
			node_ids = f.readlines()

		for i in range(self.number_of_tests):
			node_id = random.choice(node_ids).strip()
			try:
				if len(self.data_retriever.get_node_coords(node_id)) > 0:
					self.logger.info(f"Database get_node_coords successful for {node_id}")
			except Exception as e:
				self.logger.error(f"Database get_node_coords failed with {e}, for {node_id}")
				assert True, self.error(f"Database get_node_coords failed with {e}, for {node_id}")


		# test get_walking_neighbors
		with open('test_files/input/nodes.csv', 'r') as f:
			next(f)		# skip header
			node_ids = f.readlines()

		for i in range(self.number_of_tests):
			node_id = random.choice(node_ids).strip()
			try:
				if len(self.data_retriever.get_walking_neighbors(node_id)) > 0:
					self.logger.info(f"Database get_walking_neighbors successful for {node_id}")
			except Exception as e:
				self.logger.error(f"Database get_walking_neighbors failed with {e}, for {node_id}")
				assert True, self.error(f"Database get_walking_neighbors failed with {e}, for {node_id}")


		# test get_biking_neighbors
		with open('test_files/input/nodes.csv', 'r') as f:
			next(f)		# skip header
			node_ids = f.readlines()

		for i in range(self.number_of_tests):
			for j in range(len(self._risk_factor_list)):
				node_id = random.choice(node_ids).strip()
				try:
					if len(self.data_retriever.get_biking_neighbors(node_id, self._risk_factor_list[j])) > 0:
						self.logger.info(f"Database get_biking_neighbors successful for {node_id}")
					assert True, self.error(f"Database get_biking_neighbors failed for {node_id}")
				except Exception as e:
					self.logger.error(f"Database get_biking_neighbors failed with {e}, for {node_id}")
					assert True, self.error(f"Database get_biking_neighbors failed with {e}, for {node_id}")


		# Test _is_node_walkable
		with open('test_files/input/nodes.csv', 'r') as f:
			next(f)		# skip header
			node_ids = f.readlines()

		for i in range(self.number_of_tests):
			node_id = random.choice(node_ids).strip()
			try:
				if self.data_retriever._is_node_walkable(node_id):
					self.logger.info(f"Database _is_node_walkable successful for {node_id}")
			except Exception as e:
				self.logger.error(f"Database _is_node_walkable failed with {e}, for {node_id}")
				assert True, self.error(f"Database _is_node_walkable failed with {e}, for {node_id}")


		# Test _is_node_bikeable (written as _is_node_bikable in data_retriever.py)
		with open('test_files/input/nodes.csv', 'r') as f:
			next(f)		# skip header
			node_ids = f.readlines()

		for i in range(self.number_of_tests):
			node_id = random.choice(node_ids).strip()
			try:
				if self.data_retriever._is_node_bikable(node_id):
					self.logger.info(f"Database _is_node_bikeable successful for {node_id}")
			except Exception as e:
				self.logger.error(f"Database _is_node_bikeable failed with {e}, for {node_id}")
				assert True, self.error(f"Database _is_node_bikeable failed with {e}, for {node_id}")




	# START OF GPX EXPORT TESTS (using gpx_export.py)
	def test_gpx_export(self):
		# test parse_string_to_list
		for i in range(self.number_of_tests):
			# generate random path
			path = []
			for j in range(random.randint(1, 10)):
				path.append([random.uniform(self._south_bound, self._north_bound),
							 random.uniform(self._west_bound, self._east_bound)])

			# convert path to string
			path_string = str(path)

			# try to parse string to list
			try:
				self.gpx_export.parse_string_to_list(path_string)
				self.logger.info(f"GPX_export parse_string_to_list successful for {len(path)}")
			except Exception as e:
				self.logger.error(f"GPX_export parse_string_to_list failed with {e}, for {len(path)}")
				assert True, self.error(f"GPX_export parse_string_to_list failed with {e}, for {len(path)}")


		# test export
		for i in range(self.number_of_tests):
			# generate random path
			path = []
			for j in range(random.randint(1, 10)):
				path.append([random.uniform(self._south_bound, self._north_bound),
							 random.uniform(self._west_bound, self._east_bound)])

			# convert path to string
			path_string = str(path)

			# try to export gpx file
			try:
				self.gpx_export.export(path_string)
				self.logger.info(f"GPX_export export successful for {len(path)}")
			except Exception as e:
				self.logger.error(f"GPX_export export failed with {e}, for {len(path)}")
				assert True, self.error(f"GPX_export export failed with {e}, for {len(path)}")

		# try to close database
		try:
			self.data_retriever.close()
			self.logger.info("Database close successful")
		except:
			self.logger.error("Database close failed")
			assert False, self.error("Database close failed")

		sys.exit(0)


	# START OF PATHFINDER TESTS (using pathfinder.py)
	def test_pathfinder(self):
		"""
		@BDUBget_q(node_list)
		node_list is a list of Node objects (the class above Pathfinder)
		it returns the node (Node object) in the list with the smallest f value (the f value is just the h value + the g value)

		nodify(node_list, parent)
		node_list is a list of nodes returned from the dataretriever after get_node_neighbors call
		parent is a Node object (the class above Pathfinder)
		turns each node in the node list into a Node object and returns the list

		is_in(node, node_list)
		node is a Node object
		node_list is a list of Node objects
		if node is in node list and nodes f is greater than the one in the list return true
		else return false

		denodify(node)
		node is the last node in the completed path
		goes back through each of the parents adding them to the list (this gives the route)
		reverses the path list

		astar()
		doesnt return anything but it sets self.path and self.latlng

		assemble_lat_lng()
		for each node (from the database) in self.path it adds the lat and lng to self.lat_lng

		find_next_best_user_node(user_node)
		user_node start or end spots from the map
		returns the closest node in the database to user_node

		calculate_distance_between_nodes(node1, node2)
		node1 and node2 are nodes from the database
		returns the distance between the two nodes in meters

		return_path()
		closes the data retriever
		returns self.lat_lng
		:return:
		"""
		raise NotImplementedError

		# Test get_q
		# Test nodify
		# Test is_in
		# Test denodify
		# Test astar
		# Test assemble_lat_lng
		# Test find_next_best_user_node
		# Test calculate_distance_between_nodes
		# Test return_path








	def results(self):
		raise NotImplementedError

	def error(self, error_msg=None):
		if error_msg:
			print("\n\nERROR: " + error_msg)
		else:
			print("\n\nERROR: An unknown error has occurred")
		return




