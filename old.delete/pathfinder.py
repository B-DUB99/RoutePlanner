class Pathfinder:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.path = []
        self.open = []
        self.closed = []
        self.current = None
        self.path_found = False
        self.path_not_found = False

    def find_path(self):            # returns a list of coordinates in the order of the path
        # finds the path from start to end calls the other functions
        pass

    def next_nodes(self):           #
        # finds the next nodes to be checked
        pass

    def check_node(self):           # returns a boolean True or False
        # checks the node to see if it is the end node or the best node
        pass

    def find_way(self):             # returns a way_id (from database thru a node_id)
        # finds the road that the node is on
        pass

    def find_connector(self):       # takes in a way_id and returns a list of connector nodes
        # finds the connector that the node is on (returns a list of connectors associated with that one road)
        pass

