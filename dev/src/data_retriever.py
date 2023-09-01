import sqlite3

class data_retriever:

    connection

    def __init__(self):
        try:
            connection = sqlite3.connect('../db/routeplanning.db')
            print('Successful connection')
            return 0
        except Exception as e:
            print(f'Error: {e}')
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



