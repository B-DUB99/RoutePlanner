# Python modules
import sqlite3


class data_retriever:

	def __init__(self):
		self.connection = None
		self.cursor = None

	# use to connect to the database and create a cursor object
	def connect(self):
		try:
			self.connection = sqlite3.connect('../db/routeplanning.db')
			self.cursor = self.connection.cursor()
			print('Successful connection, cursor created\n')
			return 0

		except Exception as e:
			print(f'Error: {e}')
			return -1

    def close(self):
        try:
            connection.close()
        except:
            print("Close Failed")
            return -1

	def get_closest_node(self, user_marker):
		return

	def get_exit_nodes(self, way_id):
		return

	def get_nodes(self, way_id):
		return

	def get_way(self, node_id):
		return

	def get_way_info(self, way_id):
		return

	def get_node_info(self, node_id):
		return
